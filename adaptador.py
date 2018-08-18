#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2018 GENEOS http://www.geneos.com.ar/"
__license__ = "GPL 3.0"
__version__ = "1.00"

from rest_chasqui import Adapter_Chasqui
from xml_rpc import Modelo
from datetime import datetime, timedelta
import database
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
		
def GetIdCliente(email):
	cliente = Modelo()
	filtro = [['email', '=', email]]
	fields = ['id']
	return cliente.search('res.partner', filtro, fields)
		

def AgregarCliente(adapter, email, debug=False):
	param = {}
	param['id'] = email

	if debug:
		print 'Parametros:', param
	resp = adapter.datosCliente(param)
	if debug:
		print 'Codigo respuesta servidor:', resp.status_code
	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			print 'Datos recibidos:', datos
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
			id_Domicilio = direcciones[0]['id_Domicilio']
		else:
			id_Domicilio = -1	

		if debug:
			print 'apellido:', apellido
			print 'nombre:', nombre
			print 'email:', email
			print 'telefonoMovil:', telefonoMovil
			print 'telefonoFijo:', telefonoFijo
			print 'id_Cliente:', id_cliente
			print 'direcciones', direcciones

		#agregamos el cliente a la tabla res_partner
		vals = {}
		vals['name'] = apellido + ', ' + nombre
		vals['company_id'] = 1
		vals['street'] = calle + ' ' + str(altura)
		vals['zip'] = codigoPostal
		vals['city'] = localidad
		vals['email'] = email
		vals['phone'] = telefonoFijo
		vals['mobile'] = telefonoMovil
		clientenew = Modelo()
		retorno = clientenew.create('res.partner', vals)

		if debug:
			print 'ID', retorno

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


def CrearPedidosColectivos(adapter, fi, ff, debug=False):
	logger.info('>>> Chequeando si hay pedidos Colectivos ...')
	param = {}
	param['idVendedor'] = idVendedor
	param['fechaInicial'] = fi
	param['fechaFinal'] = ff
	error = False
	
	if debug:
		print 'Parametros:', param
	resp = adapter.nuevosPedidosColectivos(param)
	if debug:
		print 'Codigo respuesta servidor:', resp.status_code

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			print 'Datos recibidos:', datos
		pedidosRX = datos['pedidosColectivos']
		cantidadpedidos = len(pedidosRX)

		if debug:
			print 'Cantidad de pedidos:', cantidadpedidos
		if cantidadpedidos>0:
			#hay pedidos nuevos
			logger.info('>>> Agregando Pedidos Colectivos ...')
			for pedido in pedidosRX:
				aliasPuntoDeRetiro = pedido['aliasPuntoDeRetiro']
				aliasNodo = pedido['aliasNodo']
				id_Domicilio = pedido['id_Domicilio']
				emailCoordinador = pedido['emailCoordinador']
				pedidosIndividuales = pedido['pedidosIndividuales']

				#chequeamos si existe el cliente coordinador a recibir el pedido
				#si no existe lo creamos
				cliente_coodinador = GetIdCliente(emailCoordinador)
				if not cliente_coodinador:
					#si no existe lo creamos
					agregarcliente = AgregarCliente(adapter, emailCoordinador, debug)
					if agregarcliente!=-1:
						odoo_clienteid_coordinador = agregarcliente		
						if debug:
							print "el cliente coordinador se creo correctamente", emailCoordinador
					else:
						if debug:
							print "error al crear el cliente coordinador", emailCoordinador
						error=True
				else:
					odoo_clienteid_coordinador = int(cliente_coodinador[0]['id'])

				if debug:
					print aliasPuntoDeRetiro
					print aliasNodo
					print id_Domicilio
					print emailCoordinador

				
				if len(pedidosIndividuales)>0:
					items_pedidos = []
					for item in pedidosIndividuales:
						clientes = item['pedidos'].keys()
						for i in clientes:
							if debug:
								print 'cliente: ', i

							#chequeamos si existe el cliente
							#si no existe lo creamos
							cliente_id = GetIdCliente(i)
							if not cliente_id:
								#si no existe lo creamos
								agregarcliente = AgregarCliente(adapter, i, debug)
								if agregarcliente!=-1:
									odoo_clienteid = agregarcliente		
									if debug:
										print "el cliente se creo correctamente", i
								else:
									if debug:
										print "error al crear el cliente", i
									error=True
							else:
								odoo_clienteid = int(cliente_id[0]['id'])

							#creamos la orden de venta
							vals = {
								'origin': 'Pedido Colectivo',
								'partner_id': odoo_clienteid, 
								'pricelist_id': 1,  
								'partner_invoice_id': odoo_clienteid,
								'partner_shipping_id': odoo_clienteid_coordinador
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
								print '-------------------------------------------'
								print 'productos', items_prod
								print '-------------------------------------------'

				else:
					return 0
	else:
		error=True

	if error:
		return -1
	else:
		return retorno



def CrearPedidos(adapter, fi, ff, debug=False):
	logger.info('>>> Chequeando si hay pedidos ...')
	param = {}
	param['idVendedor'] = idVendedor
	param['fechaInicial'] = fi
	param['fechaFinal'] = ff
	error = False
	
	if debug:
		print 'Parametros:', param
	resp = adapter.nuevosPedidosIndividuales(param)
	if debug:
		print 'Codigo respuesta servidor:', resp.status_code

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			print 'Datos recibidos:', datos
		
		pedidoRX = datos['pedidoClienteDomicilio']
		cantidadpedidos = len(pedidoRX)

		if debug:
			print 'Cantidad de pedidos:', cantidadpedidos

		if cantidadpedidos>0:
			#hay pedidos nuevos
			logger.info('>>> Agregando pedidos nuevos ...')
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
					agregarcliente = AgregarCliente(adapter, id_cliente, debug)
					if agregarcliente!=-1:
						odoo_clienteid = agregarcliente		
						if debug:
							print "el cliente se creo correctamente!"
					else:
						if debug:
							print "error al crear el cliente!"
						error=True
				else:
					odoo_clienteid = int(existecliente[0]['id'])

				#chequeamos si el pedido ya existe
				if not GetIdPedido(id_pedido):
					vals = {
						'origin': str(id_pedido),
						'partner_id': odoo_clienteid, 
						'pricelist_id': 1,  
						'partner_invoice_id': odoo_clienteid,
						'partner_shipping_id': odoo_clienteid
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
						print '-------------------------------------------'
						print 'id_Pedido', id_pedido
						print 'id_Cliente', id_cliente
						print 'alias_PuntoDeRetiro', alias_puntoderetiro
						print 'id_Domicilio', id_domicilio
						print '---------'
						print 'productos', items_prod
						print '-------------------------------------------'
				else:
					if debug:
						print "error el pedido ya existe"
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
	db = database.Database()
	ultimo_update = db.GetDatos()

	if not ultimo_update[0]:
		f_hasta=datetime.now()
		f_desde=f_hasta-timedelta(hours=12)
	else:
		f_desde=ultimo_update[0]
		f_hasta=datetime.now()
	db.SetDatos([f_hasta])

	#fi=f_desde.strftime('%Y-%m-%d %H:%M:%S')
	fi='2017-01-09 16:10:11'
	ff=f_hasta.strftime('%Y-%m-%d %H:%M:%S')

	debug=False
	conection = {}
	conection['host'] = '168.181.184.203'
	conection['port'] = 8080
	idVendedor = 2

	mw = Adapter_Chasqui(conection)
	CrearPedidos(mw, fi, ff, debug)
	CrearPedidosColectivos(mw, fi, ff, debug)
