import issues

from pymongo import MongoClient
from leantesting import Client as lt

client = MongoClient('localhost', 27017)
db = client.odt_prod
issues_collection = db.integracao

cabecalho = issues_collection.find_one({'tipoDocumento': 'CONFIG_INTEGRACAO'})
token = cabecalho['authenticationToken']

lt = lt.Client()

lt.attachToken(token)
token = lt.getCurrentToken()

i = 0
for issue in issues_collection.find({'tipoDocumento':'ISSUE_INTEGRACAO'}):
    if not issue['externalId']:
        issues.create_issue(lt, issues_collection, issue)
    if issue['toUpdate']:
        issues.update_issue(lt, issues_collection, issue)

        i+=1
        if i == 5:
            break