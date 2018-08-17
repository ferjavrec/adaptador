#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
from config import config



class Modelo():
	def __init__(self):
		config.read('odoo.conf')
		endpoint = config.get('default', 'endpoint')
		self.db = config.get(endpoint, 'db')
		self.username = config.get(endpoint, 'user')
		self.password = config.get(endpoint, 'password')
		url = config.get(endpoint, 'url')
		common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
		self.uid = common.authenticate(self.db, self.username, self.password, {})
		self.models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))



	def create(self, model_name, vals):
		# Crea un nuevo registro y devuelve el id
		new_id = self.models.execute_kw(self.db, self.uid, self.password, 
			model_name, 'create', [vals])
		return new_id


	def update(self, model_name, id, vals):
		# actualiza un registro
		record = self.models.execute_kw(self.db, self.uid, self.password, 
			model_name, 'write', [[id], vals])
		return record

	
	def delete(self, model_name, id):
		#elimina un registro
		record = self.models.execute_kw(self.db, self.uid, self.password, 
			model_name, 'unlink', [[id]])
		return record


	def read(self, model_name, id, fields=[]):
		#retorna una tupla con un diccionario con los campos si fueron como parametros,
		#si no retorna todos los campos del modelo.
		#si el ID no existe retorna un booleano
		record = self.models.execute_kw(self.db, self.uid, self.password,
					model_name, 'read', [id], {'fields': fields})
		return record


	def search(self, model_name, filtro, fields, limit=1):
		#retorna una tupla con un diccionario con los campos si fueron como parametros,
		#si fields es una tupla se informan todos los campos del modelo
		#si no existen registros retorna una tupla vacia
		record = self.models.execute_kw(self.db, self.uid, self.password,
						model_name, 'search_read',
						[ filtro ],
						{'fields': fields, 'limit': limit})
		return record
