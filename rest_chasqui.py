#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2018 GENEOS http://www.geneos.com.ar/"
__license__ = "GPL 3.0"
__version__ = "1.00"

import requests
import json


class Adapter_Chasqui():

	def __init__(self, params):
		self.host = params['host']
		self.port = params['port']
		self.url = 'chasqui-odoo/rest/admin/'
		self.headers = {'Content-type': 'application/json'}


	

	def service(self, tipo, parametros):
		#
		# Parametros:
		# email=xxxxxxxxxxx@xxx.xxx, password=xxxxxxxx
		#
		try:
			ruta = self.url + str(tipo)
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None




	def nuevosPedidosIndividuales(self, parametros):
		#
		# Parametros:
		# idVendedor=2, fechaInicial='2015-01-09 16:10:11', fechaFinal='2018-05-22 13:31:15'
		#
		try:
			ruta = self.url + 'nuevosPedidosIndividuales'
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None


	def nuevosPedidosColectivos(self, parametros):
		#
		# Parametros:
		# idVendedor=2, fechaInicial='2015-01-09 16:10:11', fechaFinal='2018-05-22 13:31:15'
		#
		try:
			ruta = self.url + 'nuevosPedidosColectivos'
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None


	def datosDireccion(self, parametros):
		#
		# Parametros:
		# id=2
		#
		try:
			ruta = self.url + 'datosDireccion'
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None


	def datosCliente(self, parametros):
		#
		# Parametros:
		# id= "rosinaroura@gmail.com"
		#
		try:
			ruta = self.url + 'datosCliente'
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None


	

	def actualizarProductores(self, parametros):
		'''
		{
		   idVendedor:2,
		   token:token,
		   productores:[
		      {
		         nombre: "Central de Trabajadores Rurales",
		         descripcionLarga:"Sin descripción",
		         descripcionCorta:"Somos un proyecto autogestivo de trabajo.",
		         idSellos:[1]
		      },
		      {
		         nombre:prueba2",
		         descripcionLarga:"Sin descripción",
		         descripcionCorta:"Sin descripción",
		         idSellos:[2]
		      }
		   ]
		}
		'''
		try:
			ruta = self.url + 'actualizarProductores'
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None



	def actualizarProductos(self, parametros):
		'''
		{
		   idVendedor:2,
		   token:"",
		   variantes:[
		      {
		         nombreProducto:"Tomate"",
		         codigoInterno:"codigo0001",
		         nombreProductor:"Cooperativa la Nueva Esperanza Grisinopolli",
		         sellos:[
		            2,
		            3
		         ],
		         categoria:"Verdura",
		         precio:101.05
		      },
		      {
		         nombreProducto:"suavizante para ropa"",
		         codigoInterno:"sua01",
		         nombreProductor:"Cooperativa la Nueva Esperanza Grisinopolli",
		         sellos:[
		            1,
		            2
		         ],
		         categoria:"PANIFICADO",
		         precio:120.05
		      }
		   ]
		}
		'''
		try:
			ruta = self.url + 'actualizarProductos'
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None



	def agregarStockDeProductos(self, parametros):
		'''
		{
		   idVendedor:2,
		   token:"token",
		   productos:[
		      {
		         codigoInterno:"bur001",
		         stock:"3"
		      },
		      {
		         codigoInterno:"bur002",
		         stock:"2"
		      }
		   ]
		}
		'''
		try:
			ruta = self.url + 'agregarStockDeProductos'
			url = 'http://%s:%s/%s' % (self.host, self.port, ruta)
			return requests.post(url, data=json.dumps(parametros), 
				headers=self.headers, verify=False)
		except:
			return None