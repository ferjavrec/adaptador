#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2018 GENEOS http://www.geneos.com.ar/"
__license__ = "GPL 3.0"
__version__ = "1.00"

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

from rest_chasqui import Adapter_Chasqui
from xml_rpc import Modelo
from datetime import datetime, timedelta
from config import config
from servicios import *
import database
import json
import logging

logger = logging.getLogger('__odoo2chasqui__')
logging.basicConfig(level=logging.INFO)




def GetSelloProductos(etiqueta_id):
	etiqueta = Modelo()
	filtro = [['id', '=', etiqueta_id]]
	fields = ['name']
	retorno = etiqueta.search('product.tag', filtro, fields)

	ret=None
	if retorno:
		etiq = str(retorno[0]['name']).lower().strip()
		if etiq=='agroecología':
			ret=1
		elif etiq=='orgánico':
			ret=2
		elif etiq=='reciclado':
			ret=3
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
	
		respuesta = mw.actualizarProductores(param)

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


def Productos(adapter, fi, ff, idvendedor, token, debug=False):
	ret = False
	logger.info('>>> Chequeando si hay productos nuevos o updates ...')
	productos = Modelo()
	filtro = [
		['write_date', '>=', fi],
		['write_date', '<=', ff],
		['active', '=', True]
	]
	fields = ['id','default_code','product_tmpl_id','list_price','categ_id','name','tag_ids','seller_id']
	retorno = productos.search('product.product', filtro, fields, None)

	if len(retorno)>0:
		if debug:			
			logger.info('respuesta odoo: %s', str(retorno))
			logger.info('cantidad de productos: %s', str(len(retorno)))
		tupla = []
		for item in retorno:
			id_producto = item['id']
			codigo_interno = str(item['default_code'])
			name_producto = str(item['product_tmpl_id'][1]).strip()
			name_productor = item['seller_id'][1]
			name_categoria = str(item['categ_id'][1]).strip()
			importe = item['list_price']

			param_tupla = {}
			param_tupla['nombreProducto'] = name_producto
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

		respuesta = mw.actualizarProductos(param)

		if respuesta.status_code==200:
			ret = True
		else:
			ret = False

	return ret




if __name__ == '__main__':
	debug=False
	db = database.Database()
	ultimo_update = db.GetDatos(1)

	if not ultimo_update[0]:
		f_hasta=datetime.now()
		f_desde=f_hasta-timedelta(hours=12)
	else:
		f_desde=ultimo_update[0]
		f_hasta=datetime.now()+timedelta(hours=12) ######DESCOMENTAR timedelta(hours=12)
	db.SetDatos([f_hasta], 1)

	#####################################################################
	#Para produccion descomentar la siguiente linea
	#fi=f_desde.strftime('%Y-%m-%d %H:%M:%S')

	#Para produccion comentar la siguiente linea
	fi='2018-09-02 16:10:11'
	#####################################################################
	ff=f_hasta.strftime('%Y-%m-%d %H:%M:%S')

	config.read('configuracion.conf')
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
			Productos(mw, fi, ff, idvendedor, ret_token, debug)
		else:
			logger.warning('>>> Error al enviar el inicio de sincronizacion')

		if Syncro(mw, 'stop', idvendedor, ret_token, debug):
			Logout(mw, config.get(endpoint, 'email'), ret_token, debug)
		else:
			logger.warning('>>> Error al enviar el fin de sincronizacion')
