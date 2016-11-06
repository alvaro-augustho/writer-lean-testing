from libs import attachments, helpers, mappings, updaters

def create_update_body(LT, issues, diff, original_issue):

    issue = {}

    for key in diff:
        if key != "status":
            if key == "summary":
                issue["title"] = updaters.update_functions["summary"](diff[key]["object"])
                return issue
            if key == "description":
                expected, actual, steps = updaters.update_functions["description"](diff[key]["object"])
                issue["expected_results"] = expected
                issue["description"] = actual
                issue["steps"] = steps
                return issue
            if key == "prioridade":
                issue["priority_id"], issue["severity_id"] = updaters.update_functions["prioridade"](diff[key]["object"])
                return issue
            if key == "componente":
                issue["project_section_id"] = updaters.update_functions["componente"](LT, diff[key]["object"])
                return issue
            if key == "browser_device":
                issue["platform"] = updaters.update_functions["platform"](diff[key]["add"][0]["value"])
                return issue
            if key == "attachments":
                if "add" in diff[key]:
                    attachments.create_attachments(LT, issues, original_issue, original_issue['externalId'], diff[key]["add"])
                if "delete" in diff[key]:
                    attachments.delete_attachments(LT, issues, original_issue, diff[key]["delete"])
                return None


def update_issue(LT, issues, issue):

    print("Atualizando issue: " + str(issue))

    diff_list = issue['diffList']

    for x in range(len(diff_list)):
        if diff_list[x]['status'] == "to_do":
            body = create_update_body(diff_list[x], issue)
            if body != None:
                LT.bugs.update(issue['externalId'], body)

            issues.update_one(
                {
                    'issuekey': issue['issuekey']
                },
                {
                    '$set': {
                        'diffList.'+str(x)+'.status': 'done'
                    }
                }, upsert=False)

    issues.update_one(
        {
            'issuekey': issue['issuekey']
        },
        {
            '$set': {
                'toUpdate': False
            }
        }, upsert=False)

    print("Issue atualizada: " + str(issue))


def create_issue(LT, issues, issue):

    print("Criando issue: " + str(issue))

    summary, tags = helpers.parse_summary(issue['summary'])

    expected, actual, steps = updaters.update_description(issue['description'])

    priority, severity = updaters.update_priority(issue['prioridade'])

    component = updaters.update_componente(LT, issue['componente'])

    platform = updaters.update_platform(issue['browser_device'][0]['value'])

    newBug = LT.projects.find(mappings.project_id).bugs.create({
        'title': summary,
        'status_id': 1,
        'severity_id': severity,
        'project_version_id': mappings.project_version_id,
        'description': actual,
        'expected_results': expected,
        'steps': steps,
        'priority_id': priority,
        'project_section_id': component,
        'reproducibility_id': 1,
        'platform': platform
    })

    bug_id = newBug.data['id']

    issues.update_one(
		{
		'issuekey': issue['issuekey']
		},
		{
			'$set': {
				'externalId': bug_id
			}
		}, upsert=False)

    if issue['attachments'] is not None:
        attachments.create_attachments(LT, issues, issue, bug_id, issue['attachments'])

    print("Issue criada: " + str(issue))
