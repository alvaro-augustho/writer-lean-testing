import requests
import os

def delete_attachments(LT, issues, issue, list_attachments):

    for att in list_attachments:
        att_id = att['id']

        for att in issue['externalAttachments']:
            if att_id in att:
                external_att_id = att[att_id]
                LT.attachments.delete(external_att_id)

                issues.update_one(
                    {
                        'issuekey': issue['issuekey']
                    },
                    {
                        '$pull': {'externalAttachments': {att_id: external_att_id}}

                    }, upsert=False)
                break


def create_attachments(LT, issues, issue, bug_id, list_attachments):

	for att in list_attachments:

		file = open(att['filename'], 'wb')
		url = att['url']
		user, password = 'odt', 'B%$12.)pl'
		resp = requests.get(url, auth=(user, password))
		file.write(bytes(resp.content));

		newAttachment = LT.bugs.find(bug_id).attachments.upload('./'+att['filename'])

		os.remove('./'+att['filename'])

		issues.update_one(
			{
				'issuekey': issue['issuekey']
			},
			{
				'$push': { 'externalAttachments': {att['id']: newAttachment.data['id'] } }

			}, upsert=False)