#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_chasqui import Adapter_Chasqui
from xml_rpc import Modelo
from datetime import datetime, timedelta
import database
import json
 


def DatosDireccion(adapter, debug=False):
	param = {}
	param['id'] = 1

	if debug:
		print 'Parametros:', param
	resp = adapter.datosDireccion(param)
	if debug:
		print 'Codigo respuesta servidor:', resp.status_code
	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			print 'Datos recibidos:', datos
		alias = datos['alias']
		departamento = datos['departamento']
		calle = datos['calle']
		localidad = datos['localidad']
		calleAdyacente2 = datos['calleAdyacente2']
		calleAdyacente1 = datos['calleAdyacente1']
		codigoPostal = datos['codigoPostal']
		id_Domicilio = datos['id_Domicilio']
		altura = datos['altura']
		if debug:
			print 'alias:', alias
			print 'departamento:', departamento
			print 'calle:', calle
			print 'localidad:', localidad
			print 'calleAdyacente2:', calleAdyacente2
			print 'calleAdyacente1', calleAdyacente1
			print 'id_Domicilio', id_Domicilio
			print 'altura', altura



		



def NuevosPedidosColectivos(adapter, debug=False):
	param = {}
	param['idVendedor'] = idVendedor
	param['fechaInicial'] = '2017-01-25 16:10:11' #'2017-11-25 16:10:11'
	param['fechaFinal'] = '2018-07-05 00:00:00'
	
	#if debug:
	#	print 'Parametros:', param
	resp = adapter.nuevosPedidosColectivos(param)
	#if debug:
	#	print 'Codigo respuesta servidor:', resp.status_code

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			print 'Datos recibidos:', datos
		print ' '
		pedidosRX = datos['pedidosColectivos']
		cantidadpedidos = len(pedidosRX)

		if debug:
			print 'Cantidad de pedidos:', cantidadpedidos
		if cantidadpedidos>0:
			#hay pedidos nuevos
			#import pudb;pu.db
			for pedido in pedidosRX:
				aliasPuntoDeRetiro = pedido['aliasPuntoDeRetiro']
				aliasNodo = pedido['aliasNodo']
				id_Domicilio = pedido['id_Domicilio']
				emailCoordinador = pedido['emailCoordinador']
				pedidosIndividuales = pedido['pedidosIndividuales']

				print aliasPuntoDeRetiro
				print aliasNodo
				print id_Domicilio
				print emailCoordinador

				if len(pedidosIndividuales)>0:
					items_pedidos = []
					#import pudb;pu.db
					for item in pedidosIndividuales:
						clientes = item['pedidos'].keys()
						for i in clientes:
							print 'cliente: ', i
							ped = item['pedidos'][i]
							#print ped
							#print '-----------------------'
							for producto in ped:
								odoo_productoid = producto['cod_Producto']			
								id_producto = producto['id_Producto']
								precio = producto['precio']
								cantidadpedida = producto['cantidadPedida']
								print producto['cod_Producto'],id_producto, precio, cantidadpedida


					
					print ' '
						





















###################################################################
#
# Comienzo de rutinas del adaptador Chasqui <--> Odoo
#
###################################################################
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
		calle = direcciones[0]['calle']
		localidad = direcciones[0]['localidad']
		codigoPostal = direcciones[0]['codigoPostal']
		altura = direcciones[0]['altura']
		id_Domicilio = direcciones[0]['id_Domicilio']

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



def CrearPedidos(adapter, fi, ff, debug=False):
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
	'''
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
	fi='2018-06-09 16:10:11'
	ff=f_hasta.strftime('%Y-%m-%d %H:%M:%S')
	'''

	debug=True
	conection = {}
	conection['host'] = '168.181.184.203'
	conection['port'] = 8080
	idVendedor = 2

	mw = Adapter_Chasqui(conection)
	#CrearPedidos(mw, fi, ff, debug)
	

	#DatosDireccion(mw, debug)
	#AgregarCliente(mw, 'juanperez@prueba.com', debug)
	NuevosPedidosColectivos(mw, debug)

	#pruebaorden()
	
	#print GetIdProducto('lsn002')
	'''
	fer = Modelo()

	filtro = [['id', '=', 1], ['color', '=', 0]]
	fields = ['name']
	retorno = fer.search('res.partner', filtro, fields)
		
	print retorno
	'''

	#if ExisteCliente('yaninafrankel@hotmail.com'):
	#	print "sisisi"
	#else:
	#	print "noooo"































	
	'''
	datos['pedidoClienteDomicilio'][2]['cantidadesProductoResponse'][0]['id_Producto'] 

	#resp = mw.nuevosPedidosColectivos(param)
	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		cantidadpedidos = len(datos['pedidosColectivos'])
		

		for x in range(2, cantidadpedidos):
			#retorna los items
			#aliasPuntoDeRetiro
			#aliasNodo
			#pedidosIndividuales
			#id_Domicilio
			#emailCoordinador
			#print pedido 
				
			aliasPuntoDeRetiro = datos['pedidosColectivos'][x]['aliasPuntoDeRetiro']
			aliasNodo = datos['pedidosColectivos'][x]['aliasNodo']
			pedidosIndividuales = datos['pedidosColectivos'][x]['pedidosIndividuales']
			id_Domicilio = datos['pedidosColectivos'][x]['id_Domicilio']
			emailCoordinador = datos['pedidosColectivos'][x]['emailCoordinador']

			#import pudb; pu.db

			#print aliasPuntoDeRetiro
			#print aliasNodo
			#print pedidosIndividuales
			


			#print id_Domicilio
			#print emailCoordinador


			for item in pedidosIndividuales[0]['pedidos']['maradalponte@gmail.com']:
				print item


				#print datos['pedidosColectivos'][x][pedido]

				#datos['pedidosColectivos'][0]['emailCoordinador']

		#for item in datos:
		#	print item




	else:
		print 'Error en datos recibidos'

	'''