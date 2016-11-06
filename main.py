import issues
import lt_client
import mongo

def main():

    lt = lt_client.get_lt_client()
    cabecalho = mongo.get_cabecalho()
    lt.attachToken(cabecalho['authenticationToken'])
    issues_collection = mongo.get_collection()

    i = 0
    for issue in issues_collection.find({'tipoDocumento':'ISSUE_INTEGRACAO'}):
        if not issue['externalId']:
            issues.create_issue(lt, issues_collection, issue)
        if issue['toUpdate']:
            issues.update_issue(lt, issues_collection, issue)

            i+=1
            if i == 5:
                break

if __name__ == "__main__":
    main()