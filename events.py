import json
import dateutil.parser

data = json.load(open('data/merged.json'))
# need to rewrite this part if we want to use this script again
# first = dateutil.parser.parse(data[0]['created_at'])
secondsPerDay = 60 * 60 * 24

events = []

for issue in data:
	created_at = dateutil.parser.parse(issue['created_at'])
	age = (created_at - first).total_seconds() / secondsPerDay
	events.append({
		'id': issue[id],
		'time': age,
		'event': 'created'
	})

	if issue['closed_at'] is not None:
		closed_at = dateutil.parser.parse(issue['closed_at'])
		duration = (closed_at - created_at).total_seconds() / secondsPerDay

with open('data/events.json', 'w') as out:
	json.dump(events, out, indent=2)