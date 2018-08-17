import requests
import json


#funciona bien
url = 'http://168.181.184.203:8080/chasqui-odoo/rest/admin/nuevosPedidosIndividuales'
datas = dict(idVendedor=2, fechaInicial='2015-01-09 16:10:11', fechaFinal='2018-05-22 13:31:15')
headers = {'Content-type': 'application/json'}
rsp = requests.post(url, data=json.dumps(datas), headers=headers, verify=False)


#funciona bien
#url = 'http://168.181.184.203:8080/chasqui-odoo/rest/admin/datosDireccion'
#datas = dict(id=2)
#headers = {'Content-type': 'application/json'}
#rsp = requests.post(url, data=json.dumps(datas), headers=headers, verify=False)


#url = 'http://168.181.184.203:8080/chasqui-odoo/rest/admin/datosCliente'
#datas = dict(id= "rosinaroura@gmail.com")
#headers = {'Content-type': 'application/json'}
#rsp = requests.post(url, data=json.dumps(datas), headers=headers, verify=False)





print rsp.json()
