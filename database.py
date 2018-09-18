#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2018 GENEOS http://www.geneos.com.ar/"
__license__ = "GPL 3.0"
__version__ = "1.00"

import psycopg2


class Database():
	def __init__(self, db="adaptador", 
		user="tryton", passw="tryton", host="localhost"):
		self.conn = psycopg2.connect(host=host, dbname=db, user=user, password=passw)
		self.cur = self.conn.cursor()


	def Consulta(self, query):
		self.cur.execute(query)


	def GetDatos(self, modo):
		if modo==0:
			sql = '''
				SELECT ultimo_reporte_lectura 
				FROM configuracion
				WHERE id = 0
			'''
		else:
			sql = '''
				SELECT ultimo_reporte_escritura 
				FROM configuracion
				WHERE id = 0
			'''

		self.cur.execute(sql)
		return self.cur.fetchone()


	def SetDatos(self, param_sql, modo):
		if modo==0:
			sql = '''UPDATE configuracion SET ultimo_reporte_lectura=%s
		             WHERE id = 0; '''
		else:
			sql = '''UPDATE configuracion SET ultimo_reporte_escritura=%s
		             WHERE id = 0; '''

		self.cur.execute(sql, param_sql)
		self.conn.commit()


	def Cerrar(self):
		self.cur.close()
		self.conn.close()

	