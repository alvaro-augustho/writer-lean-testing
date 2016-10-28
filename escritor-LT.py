from pymongo import MongoClient
from leantesting import Client as LT

project_id = 19792
project_version_id = 26551
priority_map = {
		"Blocker": 1,
		"Critical": 2,
		"Major": 3,
		"Minor": 4,
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

def create_issue(issue):

	summary = issue['summary']
	description = issue['description']

	expected, actual, steps = parse_description(description)

	priority = map_priority(issue['prioridade'])
	print(priority)

	newBug = LT.projects.find(project_id).bugs.create({
		'title': summary,
		'status_id': 1,
		'severity_id': 2,
		'project_version_id': project_version_id,
		'description': actual,
		'expected_results': expected,
		'steps': steps,
		'priority_id': priority,
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



def get_component(component):

	components = LT.projects.find(project_id).sections.all().toArray()
	for c in components:
		if c['name'] == component:
			return c['id']

	new_section = LT.projects.find(project_id).sections.create({
		'name': component
	})

	return new_section['id']


def map_priority(priority):
	return priority_map[priority]

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

for issue in issues.find({'tipoDocumento':'ISSUE_INTEGRACAO'}):
	if not issue['externalId']:
		create_issue(issue)
