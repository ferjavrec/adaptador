#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2018 GENEOS http://www.geneos.com.ar/"
__license__ = "GPL 3.0"
__version__ = "1.00"

from rest_chasqui import Adapter_Chasqui
import json
import logging

logger = logging.getLogger('__chasqui2odoo__')
logging.basicConfig(level=logging.INFO)


def Login(adapter, param, debug=False):
	logger.info('>>> enviando login en servidor Chasqui ...')
	error = False
	if debug:
		logger.info('>>> Parametros Enviados: %s', str(param))
	resp = adapter.service('logIn', param)
	if debug:
		logger.info('Codigo respuesta servidor: %s', str(resp.status_code))
		logger.info('Mensaje respuesta servidor: %s', str(resp.content))

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		datos = resp.json()
		if debug:
			logger.info('logueo OK')
			logger.info('>>> Datos Recibidos: %s', datos)
		token=datos['token']
	else:
		error=True

	if error:
		return -1
	else:
		return token



def Logout(adapter, email, token, debug=False):
	logger.info('>>> enviando logout en servidor Chasqui ...')
	param = {}
	param['email'] = email
	param['token'] = token
	error = False
	if debug:
		logger.info('>>> Parametros Enviados: %s', str(param))
	resp = adapter.service('logOut', param)
	if debug:
		logger.info('Codigo respuesta servidor: %s', str(resp.status_code))
		logger.info('Mensaje respuesta servidor: %s', str(resp.content))

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		if debug:
			logger.info('logout OK')
	else:
		error=True
	return error



def Syncro(adapter, modo, idvendedor, token, debug=False):
	logger.info('>>> enviando sincronizacion en servidor Chasqui ...')
	param = {}
	param['idVendedor'] = idvendedor
	param['token'] = token
	ret = False
	if debug:
		logger.info('>>> Parametros Enviados: %s', str(param))
	if modo=='start':
		resp = adapter.service('comenzarSincronizacion', param)
	else:
		resp = adapter.service('finalizarSincronizacion', param)
	
	if debug:
		logger.info('Codigo respuesta servidor: %s', str(resp.status_code))
		logger.info('Mensaje respuesta servidor: %s', str(resp.content))

	if (resp) and (resp.status_code==200):
		#llegaron los datos bien
		ret=True
		if debug:
			if modo=='start':
				logger.info('INICIO Sincronizacion OK')
			else:
				logger.info('FIN Sincronizacion OK')
	return ret
