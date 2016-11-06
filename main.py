import issues

from pymongo import MongoClient
from leantesting import Client as LT

client = MongoClient('localhost', 27017)
db = client.odt_prod
issues_collection = db.integracao

cabecalho = issues_collection.find_one({'tipoDocumento': 'CONFIG_INTEGRACAO'})
token = cabecalho['authenticationToken']

LT = LT.Client()

LT.attachToken(token)
token = LT.getCurrentToken()

i = 0
for issue in issues_collection.find({'tipoDocumento':'ISSUE_INTEGRACAO'}):
    if issue['issuekey'] == 'STWCSTWC-33':
        if not issue['externalId']:
            issues.create_issue(LT, issues, issue)
        if issue['toUpdate']:
            issues.update_issue(LT, issues, issue)

            i+=1
            if i == 5:
                break