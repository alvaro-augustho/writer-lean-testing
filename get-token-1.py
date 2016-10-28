from pymongo import MongoClient
from leantesting import Client as LT


client = MongoClient('localhost', 26016)
db = client.odt_prod
issues = db.dados_projetos

cabecalho = issues.find_one({'tipoDocumento': 'CONFIG_LEANTESTING'})
token = cabecalho['authenticationToken']

print(token)