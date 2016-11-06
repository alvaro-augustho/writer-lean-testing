from pymongo import MongoClient
from leantesting import Client as LT
import requests
import re


project_id = 19792
project_version_id = 26551
priority_map = {
		"Blocker": 4,
		"Critical": 4,
		"Major": 3,
		"Minor": 2,
		"Trivial": 1
	}
severity_map = {
    "Blocker": 3,
    "Critical": 3,
    "Major": 2,
    "Minor": 1,
    "Trivial": 4
}
browsers_map = {
	"Firefox": 1,
	"Chrome": 2,
	"Internet Explorer": 3,
	"Safari": 4,
	"Android browser": 5,
	"Microsoft Edge": 8,
	"Opera": 10
}
device_type_map = {
    "iPhone 4S": 5,
    "iPhone 5": 5,
    "iPhone 5S": 5,
    "iPhone 6 Plus": 5,

    "Moto G1": 1,
    "Moto G2": 1,
    "Moto G3": 1,
    "Moto E": 1,
    "Moto X": 1,

    "Galaxy S2": 1,
    "Galaxy S3": 1,
    "Galaxy S4": 1,
    "Galaxy S5": 1,
    "Galaxy S6": 1,
    "Galaxy Grand Prime Duos": 1,
    "Galaxy J5": 1,

    "Zenfone 2": 1,

    "Nexus 5": 1,

    "LG G4 Beat": 1
}

device_model_map = {
    "iPhone 4S": 3,
    "iPhone 5": 2,
    "iPhone 5S": 1783,
    "iPhone 6 Plus": 2955,

    "Moto G1": 1715,
    "Moto G2": 4489,
    "Moto G3": 6503,
    "Moto E": 4370,
    "Moto X": 248,

    "Galaxy S2": 1179,
    "Galaxy S3": 766,
    "Galaxy S4": 1194,
    "Galaxy S5": 3816,
    "Galaxy S6": 3605,
    "Galaxy Grand Prime Duos": 4219,
    "Galaxy J5": 4920,

    "Zenfone 2": 7666,

    "Nexus 5": 1781,

    "LG G4 Beat": 8119
}

device_os_map = {
    "iPhone 4S": 248,
    "iPhone 5": 266,
    "iPhone 5S": 280,
    "iPhone 6 Plus": 280,

    "Moto G1": 247,
    "Moto G2": 265,
    "Moto G3": 265,
    "Moto E": 242,
    "Moto X": 247,

    "Galaxy S2": 35,
    "Galaxy S3": 51,
    "Galaxy S4": 50,
    "Galaxy S5": 269,
    "Galaxy S6": 269,
    "Galaxy Grand Prime Duos": 228,
    "Galaxy J5": 256,

    "Zenfone 2": 275,

    "Nexus 5": 269,

    "LG G4 Beat": 265
}

def update_summary(summary):
    return summary

def update_description(description):
    return parse_description(description)

def update_priority(prioridade):
    return priority_map[prioridade], severity_map[prioridade]

def update_componente(componente):
    return get_component(componente)

def update_platform(platform):
    return get_platform(platform)

update_functions = {
    "summary": update_summary,
    "description": update_description,
    "prioridade": update_priority,
    "componente": update_componente,
    "platform": update_platform
}

def create_attachments(issue, bug_id, list_attachments):

	for att in list_attachments:
		print(att)

		file = open(att['filename'], 'wb')
		url = att['url']
		user, password = 'odt', 'B%$12.)pl'
		resp = requests.get(url, auth=(user, password))
		file.write(bytes(resp.content));


		newAttachment = LT.bugs.find(bug_id).attachments.upload('./'+att['filename'])

		issues.update_one(
			{
				'issuekey': issue['issuekey']
			},
			{
				'$push': { 'externalAttachments': {att['id']: newAttachment.data['id'] } }

			}, upsert=False)

def create_update_body(diff, original_issue):

    issue = {}

    print(diff)
    for key in diff:
        if key != "status":
            if key == "summary":
                issue["title"] = update_functions["summary"](diff[key]["object"])
                return issue
            if key == "description":
                expected, actual, steps = update_functions["description"](diff[key]["object"])
                issue["expected_results"] = expected
                issue["description"] = actual
                issue["steps"] = steps
                return issue
            if key == "prioridade":
                issue["priority_id"], issue["severity_id"] = update_functions["prioridade"](diff[key]["object"])
                return issue
            if key == "componente":
                issue["project_section_id"] = update_functions["componente"](diff[key]["object"])
                return issue
            if key == "browser_device":
                issue["platform"] = update_functions["platform"](diff[key]["add"][0]["value"])
                return issue
            if key == "attachments":
                create_attachments(original_issue, original_issue['externalId'], diff[key]["add"])
                return None


def update_issue(issue):

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




def create_issue(issue):

    summary, tags = parse_summary(issue['summary'])
    description = issue['description']

    expected, actual, steps = parse_description(description)

    priority = priority_map[issue['prioridade']]

    severity = severity_map[issue['prioridade']]

    component = get_component(issue['componente'])

    platform = get_platform(issue['browser_device'][0]['value'])

    newBug = LT.projects.find(project_id).bugs.create({
        'title': summary,
        'status_id': 1,
        'severity_id': severity,
        'project_version_id': project_version_id,
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
        create_attachments(issue, bug_id, issue['attachments'])

def get_platform(platform):
    device_type = device_type_map[platform]
    device_model = device_model_map[platform]
    device_os = device_os_map[platform]

    platform = {"device_model_id": device_model, "os": device_type, "os_version_id": device_os}

    return platform

def get_component(component):

	components = LT.projects.find(project_id).sections.all().toArray()
	for c in components:
		if c['name'] == component:
			return c['id']

	new_section = LT.projects.find(project_id).sections.create({
		'name': component
	})

	return new_section.data['id']


def map_priority(priority):
	return priority_map[priority]

def parse_summary(summary):

    tags = re.split('\[|\]', summary)[1]
    return summary, tags

def parse_description(description):

	steps_arr = []

	expected = description.split('ACTUAL:')[0].replace('EXPECTED:','')

	if description.find('STEPS') is -1:
		actual = description.split('ACTUAL:')[1].replace('ACTUAL:','')
	else:
		actual = description.split('ACTUAL:')[1].split('STEPS:')[0]
		steps = description.split('STEPS:')[1].replace('STEPS:','')
		steps_arr = steps.strip().splitlines()

	return expected, actual, steps_arr


client = MongoClient('localhost', 27017)
db = client.odt_prod
issues = db.integracao

cabecalho = issues.find_one({'tipoDocumento': 'CONFIG_INTEGRACAO'})
token = cabecalho['authenticationToken']

print(token)

LT = LT.Client()

LT.attachToken(token)
token = LT.getCurrentToken()
print('Token atual: '+token)

i = 0
for issue in issues.find({'tipoDocumento':'ISSUE_INTEGRACAO'}):
    if issue['issuekey'] == 'STWCSTWC-33':
        if not issue['externalId']:
            create_issue(issue)
        if issue['toUpdate']:
            update_issue(issue)

            i+=1
            if i == 5:
                break

