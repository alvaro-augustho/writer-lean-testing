from libs import mongo, lt_client, issues

def main():

    lt = lt_client.get_lt_client()
    issues_collection = mongo.get_collection()

    for issue in issues_collection.find({'tipoDocumento':'ISSUE_INTEGRACAO'}):
        if not issue['externalId']:
            try:
                issues.create_issue(lt, issues_collection, issue)
            except Exception as err:
                print("Erro ao criar issue "+ issue['issuekey'] + ": ", err)

        if issue['toUpdate']:
            try:
                issues.update_issue(lt, issues_collection, issue)
            except Exception as err:
                print("Erro ao atualizar issue "+ issue['issuekey'] + ": ", err)

if __name__ == "__main__":
    main()