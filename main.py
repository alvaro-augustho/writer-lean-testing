from libs import mongo, lt_client, issues

def main():

    lt = lt_client.get_lt_client()
    cabecalho = mongo.get_cabecalho()
    issues_collection = mongo.get_collection()

    for issue in issues_collection.find({'tipoDocumento':'ISSUE_INTEGRACAO'}):
        if not issue['externalId']:
            issues.create_issue(lt, issues_collection, issue)
        if issue['toUpdate']:
            issues.update_issue(lt, issues_collection, issue)

if __name__ == "__main__":
    main()