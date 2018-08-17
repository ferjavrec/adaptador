#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2


class Database():
	def __init__(self, db="adaptador", 
		user="tryton", passw="tryton", host="localhost"):
		self.conn = psycopg2.connect(host=host, dbname=db, user=user, password=passw)
		self.cur = self.conn.cursor()


	def Consulta(self, query):
		self.cur.execute(query)


	def GetDatos(self):
		sql = '''
			SELECT ultimo_reporte_lectura 
			FROM configuracion
			WHERE id = 0
		''' 
		self.cur.execute(sql)
		return self.cur.fetchone()


	def SetDatos(self, param_sql):
		sql = """UPDATE configuracion SET ultimo_reporte_lectura=%s
	             WHERE id = 0; """
		self.cur.execute(sql, param_sql)
		self.conn.commit()


	def Cerrar(self):
		self.cur.close()
		self.conn.close()

	