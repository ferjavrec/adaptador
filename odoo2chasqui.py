#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2018 GENEOS http://www.geneos.com.ar/"
__license__ = "GPL 3.0"
__version__ = "1.00"

import sys 
import os 
reload(sys)  
sys.setdefaultencoding('utf8')

from xml_rpc import Modelo
from datetime import datetime, timedelta
from config import config
from servicios import *
import database
import logging

logger = logging.getLogger('__odoo2chasqui__')
logging.basicConfig(level=logging.INFO)

dirx = os.path.dirname(__file__)
path_config = os.path.join(dirx, 'configuracion.conf')	


def GetSelloProductos(etiqueta_id):
	etiqueta = Modelo()
	filtro = [['id', '=', etiqueta_id]]
	fields = ['name']
	retorno = etiqueta.search('product.tag', filtro, fields)

	ret=None
	if retorno:
		etiq = str(retorno[0]['name']).lower().strip()
		if etiq=='agroecologico':
			ret=1
		elif etiq=='organico':
			ret=2
		elif etiq=='reciclado':
			ret=3
		elif etiq=='artesanal':
			ret=5
		elif etiq=='en red':
			ret=7
		elif etiq=='kilometro cero':
			ret=8
		else:
			ret=None
	return ret



def GetSelloProductor(category_id):
	categoria = Modelo()
	filtro = [['id', '=', category_id]]
	fields = ['name']
	retorno = categoria.search('res.partner.category', filtro, fields)

	ret=None
	if retorno:
		categ = str(retorno[0]['name']).lower().strip()
		if categ=='cooperativas':
			ret=1
		elif categ=='recuperadas':
			ret=2
		elif categ=='agricultura familiar':
			ret=3
		elif categ=='empresa social':
			ret=4
		else:
			ret=None
	return ret




def Productores(adapter, fi, ff, idvendedor, token, debug=False):
	ret = False
	logger.info('>>> Chequeando si hay productores nuevos o updates ...')
	productores = Modelo()
	filtro = [
		['write_date', '>=', fi],
		['write_date', '<=', ff],
		['supplier', '=', True]
	]
	fields = ['id','name','comment','ref','category_id']
	retorno = productores.search('res.partner', filtro, fields, None)

	if len(retorno)>0:
		if debug:			
			logger.info('respuesta odoo: %s', str(retorno))
			logger.info('cantidad de productores: %s', str(len(retorno)))
		tupla = []
		for item in retorno:
			if item['comment']:
				comentario = str(item['comment']).strip()
			else:
				comentario = ' '
			if item['ref']:
				referencia = str(item['ref']).strip()
			else:
				referencia = ' '

			sellos=[]
			for cate in item['category_id']:
				sellos.append(GetSelloProductor(cate))

			param_tupla = {}
			param_tupla['nombre'] = str(item['name']).strip()
			param_tupla['descripcionLarga'] = referencia
			param_tupla['descripcionCorta'] = comentario
			param_tupla['idSellos'] = sellos
			tupla.append(param_tupla)

		param = {}
		param['idVendedor'] = idvendedor
		param['token'] = token
		param['productores'] = tupla
	
		respuesta = adapter.actualizarProductores(param)

		if respuesta.status_code==200:
			ret = True
		else:
			ret = False
	return ret




def GetProductCateg(id_categoria):
	productcat = Modelo()
	filtro = [['id', '=', id_categoria]]
	fields = ['name']
	retorno = productcat.search('product.category', filtro, fields)
	return retorno


def GetTemplate(id_template):
	template = Modelo()
	filtro = [['id', '=', id_template]]
	fields = ['name','list_price','categ_id','tag_id']
	retorno = template.search('product.template', filtro, fields)
	return retorno



def GetProductor(id_productor):
	productor = Modelo()
	filtro = [['product_tmpl_id', '=', id_productor]]
	fields = ['name']
	retorno = productor.search('product.supplierinfo', filtro, fields)
	return retorno


def ProductosUpdate(adapter, fi, ff, idvendedor, token, debug=False):
	ret = False
	logger.info('>>> Chequeando si hay productos con updates ...')
	productos = Modelo()
	filtro = [
		['write_date', '>=', fi],
		['write_date', '<=', ff],
		['active', '=', True]
	]
	fields = ['id','default_code','list_price','categ_id','name','tag_ids','seller_id','product_variant_ids']
	retorno = productos.search('product.template', filtro, fields, None)

	if len(retorno)>0:
		if debug:			
			logger.info('respuesta odoo: %s', str(retorno))
			logger.info('cantidad de productos: %s', str(len(retorno)))
		tupla = []
		for item in retorno:
			id_producto = item['product_variant_ids']
			codigo_interno = str(item['default_code'])
			name_producto = str(item['name']).strip()
			name_productor = item['seller_id'][1]
			name_categoria = str(item['categ_id'][1]).strip()
			importe = item['list_price']

			param_tupla = {}
			param_tupla['nombreProducto'] = str(GetNameProducto(id_producto)[0]['name_template']).strip()
			param_tupla['codigoInterno'] = codigo_interno
			param_tupla['nombreProductor'] = name_productor

			sellos=[]
			for sello in item['tag_ids']:
				sellos.append(GetSelloProductos(sello))

			param_tupla['sellos'] = sellos
			param_tupla['categoria'] = name_categoria
			param_tupla['precio'] = importe
			tupla.append(param_tupla)

		param = {}
		param['idVendedor'] = idvendedor
		param['token'] = token
		param['variantes'] = tupla

		respuesta = adapter.actualizarProductos(param)

		if respuesta.status_code==200:
			ret = True
		else:
			ret = False

	return ret



def GetStockLocation(id_location):
	location = Modelo()
	filtro = [['name', '=', id_location]]
	fields = ['id' ,'name', 'complete_name'] 
	retorno = location.search('stock.location', filtro, fields, None)
	return retorno



def GetDefaultCode(id_product):
	producto = Modelo()
	filtro = [
		['id', '=', id_product]
	]
	fields = ['default_code']
	retorno = producto.search('product.product', filtro, fields)
	return retorno


def GetNameProducto(id_product):
	producto = Modelo()
	filtro = [
		['id', '=', id_product]
	]
	fields = ['name_template']
	retorno = producto.search('product.product', filtro, fields)
	return retorno


def StockComprometido(adapter, fi, ff, idvendedor, token, debug=False):
	param_tupla = {}
	logger.info('>>> Chequeando stock comprometido sin entregar ...')

	ordenes = Modelo()
	filtro = [
		['state', 'in', ['progress', 'draft']],
		['x_origen', '=', 'chasqui'],
	]
	fields = ['order_line']
	ordenes_ids = ordenes.search('sale.order', filtro, fields, None)
	lineas = []
	if ordenes_ids:
		for i in ordenes_ids:
			lineas += i['order_line']
		ordenes_lines = Modelo()
		filtro = [
			['id', 'in', lineas]
		]
		fields = ['product_uos_qty', 'product_id']
		lineas_ids = ordenes_lines.search('sale.order.line', filtro, fields, None)

		for item in lineas_ids:
			codigo_interno = GetDefaultCode(item['product_id'][0])[0]['default_code']
			cantidad = item['product_uos_qty'] * -1

			if param_tupla.has_key(codigo_interno):
				cant = param_tupla[codigo_interno]
				param_tupla[codigo_interno] = cantidad + cant
			else:
				param_tupla[codigo_interno] = cantidad

	return param_tupla


def CheckStock(adapter, fi, ff, idvendedor, token, debug=False):
	ret = False
	logger.info('>>> Chequeando stock ...')

	location = GetStockLocation('Chasqui')
	if location:
		productos = Modelo()
		filtro = [
			['location_id', '=', location[0]['id']]
		]
		fields = ['quantity', 'product_id']
		retorno = productos.search('stock.history', filtro, fields, None)

		if debug:
			logger.info('respuesta odoo stock en deposito chasqui: %s', str(retorno))

		#consulta si hay stock pendiente de entregar en ordenes de ventas sin confirmar
		param_tupla = StockComprometido(adapter, fi, ff, idvendedor, token, debug=False)

		if debug:
			logger.info('respuesta odoo stock comprometido chasqui: %s', str(param_tupla))

		for item in retorno:
			codigo_interno = GetDefaultCode(item['product_id'][0])[0]['default_code']
			cantidad = item['quantity']

			if param_tupla.has_key(codigo_interno):
				cant = param_tupla[codigo_interno]
				param_tupla[codigo_interno] = cantidad + cant
			else:
				param_tupla[codigo_interno] = cantidad

		if debug:
			logger.info('respuesta odoo stock real chasqui: %s', str(param_tupla))

		tupla = []
		for item in param_tupla:
			dict_prod = {}
			dict_prod['codigoInterno'] = item
			dict_prod['stock'] = param_tupla[item]
			tupla.append(dict_prod)

		if len(tupla) > 0:
			logger.info('>>> Actualizando stock ...')
			param = {}
			param['idVendedor'] = idvendedor
			param['token'] = token
			param['productos'] = tupla

			respuesta = adapter.agregarStockDeProductos(param)

			if respuesta.status_code == 200:
				ret = True
			else:
				ret = False

	return ret



if __name__ == '__main__':
	debug=True
	db = database.Database()
	ultimo_update = db.GetDatos(1)

	if not ultimo_update[0]:
		f_hasta=datetime.utcnow()-timedelta(hours=3)
		f_desde=f_hasta-timedelta(hours=12)
	else:
		f_desde=ultimo_update[0]
		f_hasta=datetime.utcnow()-timedelta(hours=3)
	db.SetDatos([f_hasta], 1)

	#####################################################################
	#Para produccion descomentar la siguiente linea
	fi=f_desde.strftime('%Y-%m-%d %H:%M:%S')
	#Para produccion comentar la siguiente linea
	#fi='2018-09-02 16:10:11'
	#####################################################################
	ff=f_hasta.strftime('%Y-%m-%d %H:%M:%S')

	config.read(path_config)
	endpoint = config.get('default', 'confi_chasqui')

	conection = {}
	conection['host'] = config.get(endpoint, 'url')
	conection['port'] = config.get(endpoint, 'puerto')
	idvendedor = config.get(endpoint, 'idvendedor')
	mw = Adapter_Chasqui(conection)

	param = {}
	param['email'] = config.get(endpoint, 'email')
	param['password'] = config.get(endpoint, 'password')
	ret_token = Login(mw, param, debug)
	

	if ret_token!=-1:
		if Syncro(mw, 'start', idvendedor, ret_token, debug):
			Productores(mw, fi, ff, idvendedor, ret_token, debug)
			ProductosUpdate(mw, fi, ff, idvendedor, ret_token, debug)
			CheckStock(mw, fi, ff, idvendedor, ret_token, debug)
		else:
			logger.warning('>>> Error al enviar el inicio de sincronizacion')

		if Syncro(mw, 'stop', idvendedor, ret_token, debug):
			Logout(mw, config.get(endpoint, 'email'), ret_token, debug)
		else:
			logger.warning('>>> Error al enviar el fin de sincronizacion')
