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
from rest_chasqui import Adapter_Chasqui
from xml_rpc import Modelo
from datetime import datetime, timedelta
from config import config
from servicios import *
import database
import json
import logging

logger = logging.getLogger('__chasqui2odoo__')
logging.basicConfig(level=logging.INFO)

dirx = os.path.dirname(__file__)
path_config = os.path.join(dirx, 'configuracion.conf')	


def ActualizarDomicilio(adapter, id_domicilio, id_cliente_odoo, token, debug=False):
	param = {}
	param['id'] = id_domicilio
	param['token'] = token

	if debug:
		logger.info('>>> Parametros enviados: %s', str(param))
	resp = adapter.datosDireccion(param)
	if debug:
		logger.info('>>> Codigo respuesta servidor: %s', str(resp.status_code))
	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			logger.info('>>> Datos Recibidos: %s', datos)
				
		calle = datos['calle']
		altura = datos['altura']
		localidad = datos['localidad']
		codigopostal = datos['codigoPostal']
		id_domicilio = datos['id_Domicilio']
	
		if debug:
			logger.info('calle: %s', calle)
			logger.info('altura: %s', altura)		
			logger.info('localidad: %s', localidad)
			logger.info('codigo Postal: %s', codigopostal)
			logger.info('id_domicilio: %s', str(id_domicilio))


		#editamos el cliente en la tabla res_partner
		#agregar al modelo res_partner el campo
		# x_iddomicilio de tipo integer
		vals = {}
		vals['street'] = calle + ' ' + str(altura)
		vals['zip'] = codigopostal
		vals['city'] = localidad
		vals['x_iddomicilio'] = int(id_domicilio)
		clientedomicilio = Modelo()
		retorno = clientedomicilio.update('res.partner', id_cliente_odoo, vals)
		if debug:
			logger.info('ID cliente: %s', str(retorno))

		return retorno
	else:
		#si hay error retorna -1
		return -1


def GetIdDomicilio(id_cliente):
	cliente = Modelo()
	filtro = [['id', '=', id_cliente]]
	fields = ['x_iddomicilio']
	ret = cliente.search('res.partner', filtro, fields)
	if ret and ret[0]:
		return ret[0]['x_iddomicilio']
	else:
		return False


def GetIdCliente(email):
	cliente = Modelo()
	filtro = [['email', '=', email]]
	fields = ['id']
	return cliente.search('res.partner', filtro, fields)
		

def AgregarCliente(adapter, email, token, debug=False):
	param = {}
	param['id'] = email
	param['token'] = token

	if debug:
		logger.info('>>> Parametros enviados: %s', str(param))
	resp = adapter.datosCliente(param)
	if debug:
		logger.info('>>> Codigo respuesta servidor: %s', str(resp.status_code))
	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			logger.info('>>> Datos Recibidos: %s', datos)
		apellido = datos['apellido']
		nombre = datos['nombre']
		email = datos['email']
		telefonoMovil = datos['telefonoMovil']
		telefonoFijo = datos['telefonoFijo']
		id_cliente = datos['id']
		direcciones = datos['direcciones']
		
		if direcciones and direcciones[0]:
			calle = direcciones[0]['calle']
		else:
			calle = 's/d'	
		if direcciones and direcciones[0]:
			localidad = direcciones[0]['localidad']
		else:
			localidad = 's/d'
		if direcciones and direcciones[0]:
			codigoPostal = direcciones[0]['codigoPostal']
		else:
			codigoPostal = 's/d'
		if direcciones and direcciones[0]:
			altura = direcciones[0]['altura']
		else:
			altura = 's/d'
		if direcciones and direcciones[0]:
			id_domicilio = direcciones[0]['id_Domicilio']
		else:
			id_domicilio = 0	

		if debug:
			logger.info('apellido: %s', apellido)
			logger.info('nombre: %s', nombre)
			logger.info('email: %s', email)
			logger.info('telefonoMovil: %s', telefonoMovil)
			logger.info('telefonoFijo: %s', telefonoFijo)
			logger.info('id_Cliente: %s', id_cliente)
			logger.info('id_Domicilio: %s', id_domicilio)
			logger.info('direcciones: %s', direcciones)


		#agregamos el cliente a la tabla res_partner
		#agregar al modelo res_partner el campo
		# x_iddomicilio de tipo integer
		vals = {}
		vals['name'] = apellido + ', ' + nombre
		vals['company_id'] = 1
		vals['street'] = calle + ' ' + str(altura)
		vals['zip'] = codigoPostal
		vals['city'] = localidad
		vals['email'] = email
		vals['phone'] = telefonoFijo
		vals['mobile'] = telefonoMovil
		vals['x_iddomicilio'] = int(id_domicilio)  #este campo es personalizado
		clientenew = Modelo()
		retorno = clientenew.create('res.partner', vals)

		if debug:
			logger.info('ID cliente: %s', str(retorno))

		return retorno
	else:
		#si hay error retorna -1
		return -1


def GetIdProducto(cod_Producto):
	producto = Modelo()
	filtro = [['default_code', '=', cod_Producto]]
	fields = ['id']
	return producto.search('product.template', filtro, fields)


def GetIdPedido(id_pedido):
	pedido = Modelo()
	filtro = [['origin', '=', id_pedido]]
	fields = ['id']
	return pedido.search('sale.order', filtro, fields)


def CrearPedidosColectivos(adapter, fi, ff, idVendedor, token, debug=False):
	logger.info('>>> Chequeando si hay pedidos Colectivos ...')
	param = {}
	param['idVendedor'] = idVendedor
	param['fechaInicial'] = fi
	param['fechaFinal'] = ff
	param['token'] = token
	error = False
	retorno=0
	
	if debug:
		logger.info('>>> Parametros enviados: %s', str(param))
	resp = adapter.nuevosPedidosColectivos(param)
	if debug:
		logger.info('>>> Codigo respuesta servidor: %s', str(resp.status_code))

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			logger.info('>>> Datos Recibidos: %s', datos)
		pedidosRX = datos['pedidosColectivos']
		cantidadpedidos = len(pedidosRX)

		if debug:
			logger.info('>>> Cantidad de Pedido Recibidos: %s', str(cantidadpedidos))
		if cantidadpedidos>0:
			#hay pedidos nuevos
			for pedido in pedidosRX:
				logger.info('>>> Agregando Pedidos Colectivos ...')
				aliasPuntoDeRetiro = pedido['aliasPuntoDeRetiro']
				aliasNodo = pedido['aliasNodo']
				id_domicilio = pedido['id_Domicilio']
				emailCoordinador = pedido['emailCoordinador']
				pedidosIndividuales = pedido['pedidosIndividuales']

				#chequeamos si existe el cliente coordinador a recibir el pedido
				#si no existe lo creamos
				cliente_coodinador = GetIdCliente(emailCoordinador)
				if not cliente_coodinador:
					#si no existe lo creamos
					agregarcliente = AgregarCliente(adapter, emailCoordinador, token, debug)
					if agregarcliente!=-1:
						odoo_clienteid_coordinador = agregarcliente		
						if debug:
							logger.info('>>> El cliente coordinador se creo correctamente: %s', emailCoordinador)
					else:
						if debug:
							logger.warning('>>> Error al crear el cliente coordinador: %s', emailCoordinador)
						error=True
				else:
					odoo_clienteid_coordinador = int(cliente_coodinador[0]['id'])


				#chequeamos la direccion del cliente coordinador y si es distinta la editamos
				ret = GetIdDomicilio(odoo_clienteid_coordinador)
				if ret!=id_domicilio:
					ActualizarDomicilio(adapter, id_domicilio, odoo_clienteid_coordinador, token, debug)
					if debug:
						logger.info('>>> Actualizando el domicilio del cliente coordinador: %s', emailCoordinador)

				if debug:
					logger.info('aliasPuntoDeRetiro: %s', aliasPuntoDeRetiro)
					logger.info('aliasNodo: %s', aliasNodo)
					logger.info('id_Domicilio: %s', id_domicilio)
					logger.info('emailCoordinador: %s', emailCoordinador)

				
				if len(pedidosIndividuales)>0:
					items_pedidos = []
					for item in pedidosIndividuales:
						clientes = item['pedidos'].keys()
						for i in clientes:
							if debug:
								logger.info('Cliente: %s', i)

							#chequeamos si existe el cliente
							#si no existe lo creamos
							cliente_id = GetIdCliente(i)
							if not cliente_id:
								#si no existe lo creamos
								agregarcliente = AgregarCliente(adapter, i, token, debug)
								if agregarcliente!=-1:
									odoo_clienteid = agregarcliente		
									if debug:
										logger.info('>>> El cliente se creo correctamente: %s', i)
								else:
									if debug:
										logger.warning('>>> Error al crear el cliente: %s', i)
									error=True
							else:
								odoo_clienteid = int(cliente_id[0]['id'])

							#creamos la orden de venta
							logger.info('>>> Agregando pedidos colectivos nuevos ...')
							vals = {
								'origin': 'Pedido Colectivo',
								'partner_id': odoo_clienteid, 
								'pricelist_id': 1,  
								'partner_invoice_id': odoo_clienteid,
								'partner_shipping_id': odoo_clienteid_coordinador,
								'state': 'progress',
							}

							items_prod = []
							for producto in item['pedidos'][i]:
								odoo_productoid = GetIdProducto(producto['cod_Producto'])[0]['id']			
								id_producto = producto['id_Producto']
								precio = producto['precio']
								cantidadpedida = producto['cantidadPedida']

								items_prod.append((0, 0, {
										'product_id': odoo_productoid,
										'product_uom_qty': cantidadpedida,
										'qty_delivered': cantidadpedida,
										'price_unit': precio
										}))
							vals['order_line'] = items_prod

							saleorder = Modelo()
							retorno = saleorder.create('sale.order', vals)			

							if debug:
								logger.info('Productos: %s', str(items_prod))

				else:
					return 0
	else:
		error=True

	if error:
		return -1
	else:
		return retorno



def CrearPedidos(adapter, fi, ff, idvendedor, token, debug=False):
	logger.info('>>> Chequeando si hay pedidos ...')
	param = {}
	param['idVendedor'] = idvendedor
	param['fechaInicial'] = fi
	param['fechaFinal'] = ff
	param['token'] = token
	error = False
	retorno=0
	
	if debug:
		logger.info('>>> Parametros Enviados: %s', str(param))
	resp = adapter.nuevosPedidosIndividuales(param)
	if debug:
		logger.info('Codigo respuesta servidor: %s', str(resp.status_code))

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			logger.info('>>> Datos Recibidos: %s', datos)
		
		pedidoRX = datos['pedidoClienteDomicilio']
		cantidadpedidos = len(pedidoRX)

		if debug:
			logger.info('>>> Cantidad de Pedido Recibidos: %s', str(cantidadpedidos))

		if cantidadpedidos>0:
			#hay pedidos nuevos
			for pedido in pedidoRX:
				id_pedido = pedido['id_Pedido']
				id_cliente = pedido['id_Cliente']
				alias_puntoderetiro = pedido['alias_PuntoDeRetiro']
				id_domicilio = pedido['id_Domicilio'] 
				productosRX = pedido['cantidadesProductoResponse']  
							
				#chequeamos si existe el cliente
				existecliente = GetIdCliente(id_cliente)
				if not existecliente:
					#si no existe lo creamos
					agregarcliente = AgregarCliente(adapter, id_cliente, token, debug)
					if agregarcliente!=-1:
						odoo_clienteid = agregarcliente		
						if debug:
							logger.info('>>> El cliente se creo correctamente: %s', id_cliente)
					else:
						if debug:
							logger.warning('>>> Error al crear el cliente: %s', id_cliente)
						error=True
				else:
					odoo_clienteid = int(existecliente[0]['id'])


				#chequeamos la direccion del cliente y si es distinta la editamos
				ret = GetIdDomicilio(odoo_clienteid)
				if ret!=id_domicilio:
					ActualizarDomicilio(adapter, id_domicilio, odoo_clienteid, token, debug)
					if debug:
						logger.info('>>> Actualizando el domicilio del cliente: %s', id_cliente)


				#chequeamos si el pedido ya existe
				if not GetIdPedido(id_pedido):
					logger.info('>>> Agregando pedidos nuevos ...')
					vals = {
						'origin': str(id_pedido),
						'partner_id': odoo_clienteid, 
						'pricelist_id': 1,  
						'partner_invoice_id': odoo_clienteid,
						'partner_shipping_id': odoo_clienteid,
						'state': 'progress',
					}
					
					items_prod = []
					for producto in productosRX:
						odoo_productoid = GetIdProducto(producto['cod_Producto'])[0]['id']			
						id_producto = producto['id_Producto']
						precio = producto['precio']
						cantidadpedida = producto['cantidadPedida']
											
						items_prod.append((0, 0, {
							'product_id': odoo_productoid,
							'product_uom_qty': cantidadpedida,
							'qty_delivered': cantidadpedida,
							'price_unit': precio
							}))
					vals['order_line'] = items_prod

					saleorder = Modelo()
					retorno = saleorder.create('sale.order', vals)			

					if debug:
						logger.info('id_pedido: %s', str(id_pedido))
						logger.info('id_cliente: %s', str(id_cliente))
						logger.info('alias_puntoderetiro: %s', str(alias_puntoderetiro))
						logger.info('id_domicilio: %s', str(id_domicilio))
						logger.info('items: %s', str(items_prod))

				else:
					if debug:
						logger.warning('>>> error el pedido ya existe')
					error=True
		else:
			return 0

	else:
		error=True

	if error:
		return -1
	else:
		return retorno




	



if __name__ == '__main__':
	debug=False
	db = database.Database()
	ultimo_update = db.GetDatos(0)

	if not ultimo_update[0]:
		f_hasta=datetime.now()
		f_desde=f_hasta-timedelta(hours=12)
	else:
		f_desde=ultimo_update[0]
		f_hasta=datetime.now()
	db.SetDatos([f_hasta],0)

	#####################################################################
	#Para produccion descomentar la siguiente linea
	fi=f_desde.strftime('%Y-%m-%d %H:%M:%S')

	#Para produccion comentar la siguiente linea
	#fi='2017-01-09 16:10:11'
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
			CrearPedidos(mw, fi, ff, idvendedor, ret_token, debug)
			CrearPedidosColectivos(mw, fi, ff, idvendedor, ret_token, debug)
		else:
			logger.warning('>>> Error al enviar el inicio de sincronizacion')

		if Syncro(mw, 'stop', idvendedor, ret_token, debug):
			Logout(mw, config.get(endpoint, 'email'), ret_token, debug)
		else:
			logger.warning('>>> Error al enviar el fin de sincronizacion')
