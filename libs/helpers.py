import re

from libs import constants


def get_platform(platform):
    device_type = constants.device_type_map[platform]
    device_model = constants.device_model_map[platform]
    device_os = constants.device_os_map[platform]

    platform = {"device_model_id": device_model, "os": device_type, "os_version_id": device_os}

    return platform

def get_component(LT, component):

	components = LT.projects.find(constants.project_id).sections.all().toArray()
	for c in components:
		if c['name'] == component:
			return c['id']

	new_section = LT.projects.find(constants.project_id).sections.create({
		'name': component
	})

	return new_section.data['id']


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

def get_reporter(LT, email_address):
	LT.attachToken(constants.tokens_map[email_address])

