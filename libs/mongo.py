from pymongo import MongoClient

host = 'localhost'
port = 27017
collection = 'integracao'

client = MongoClient(host, port)
db = client.odt_prod
collection = db[collection]

def get_collection():
    return collection

def get_cabecalho():
    return collection.find_one({'tipoDocumento': 'CONFIG_INTEGRACAO'})