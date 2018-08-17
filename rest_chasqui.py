# -*- coding: utf-8 -*-
import requests
import json


class Adapter_Chasqui():

	def __init__(self, params):
		self.host = params['host']
		self.port = params['port']
		self.url = 'chasqui-odoo/rest/admin/'
		self.headers = {'Content-type': 'application/json'}


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