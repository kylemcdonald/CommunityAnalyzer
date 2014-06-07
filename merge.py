import json
import re

owner = "openframeworks"
repo = "openFrameworks"

all = {}

# this is really hard, but this approach isn't bad. very similar to github's approach apparently.
replyPattern = re.compile('(\n .+? escribi|\n.+wrote|From: |\n>.+Reply to this email directly).*', re.DOTALL)
def clean(text):
	return replyPattern.sub('', text)

for i in range(0, 3005):
	id = i + 1
	issuePath = "repos/{}/{}/issues".format(owner, repo)

	issueJson = "{}/{}.json".format(issuePath, id)
	commentsJson = "{}/{}/comments.json".format(issuePath, id)
	eventsJson = "{}/{}/events.json".format(issuePath, id)

	issue = json.load(open(issueJson))
	comments = json.load(open(commentsJson))
	events = json.load(open(eventsJson))

	notFound = not 'message' in issue

	if notFound:
		labels = []
		for item in issue['labels']:
			labels.append(item['name'])

		commentsData = []
		for item in comments:
			commentsData.append({
				'user': item['user']['login'],
				'created_at': item['created_at'],
				'body': clean(item['body'])
			})

		eventsData = []
		for item in events:
			event = {
				'event': item['event'],
				'created_at': item['created_at'],
				'user': ''
			}
			if item['actor'] is not None:
				event['user'] = item['actor']['login']
			eventsData.append(event)

		milestone = ''
		if issue['milestone'] is not None:
			milestone = issue['milestone']['title']

		cur = {
			'title': issue['title'],
			'user': issue['user']['login'],
			'created_at': issue['created_at'],
			'closed_at': issue['closed_at'],
			'body': issue['body'],
			'milestone': milestone,
			'labels': labels,
			'comments': commentsData,
			'events': eventsData,
			'pull_request': 'pull_request' in issue
		}
		all[id] = cur

with open('data/merged.json', 'w') as out:
	json.dump(all, out, indent=2)