import json
from pprint import pprint
import dateutil.parser
import csv

data = json.load(open('data/merged.json'))
first = dateutil.parser.parse(data['1']['created_at'])
secondsPerDay = 60 * 60 * 24

# speed is something like:
# - number of comments in first N days
# - amount of time to N comments
# - reached N comments in first K days (binary series)

# instead of doing regression to get duration,
# consider classifying duration into a few bins
# one day, one week, one month, one year, unclosed

# more features to consider:
# - time until first comment
# - minimum time between comments
# - maximum time between comments
# - has multiple comments from same user (number of comments > number of users)

with open('data/flat.tab', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter='\t')
	info = [
		'body length', 'c', '',
		'label count', 'c', '',
		# 'user', 'd', '',
		'is pull request', 'd', '',
		'title length', 'c', '',

		'is milestone', 'd', '',

		# user count
		'comment count', 'c', '',
		# user count / comment count
		# comments length sum
		# comments length sum / comment count
		# comment speed

		# number of mentions
		'event count', 'c', '',
		# event speed

		'age', 'c', '',
		'duration', 'c', 'class',
	]
	writer.writerow(info[0::3])
	writer.writerow(info[1::3])
	writer.writerow(info[2::3])
	for id in data:
		issue = data[id]
		created_at = dateutil.parser.parse(issue['created_at'])
		age = (created_at - first).total_seconds() / secondsPerDay
		closed_at = None
		duration = None
		users = []
		# for comment in issue['comments']:
		# 	users += 
		if issue['closed_at'] is not None:
			closed_at = dateutil.parser.parse(issue['closed_at'])
			duration = (closed_at - created_at).total_seconds() / secondsPerDay
			writer.writerow([
				len(issue['body']),	
				len(issue['labels']),
				# issue['user'],
				issue['pull_request'],
				len(issue['title']),

				issue['milestone'] != '',

				# number of users involved
				# sum of comment lengths
				len(issue['comments']),
				# comment 1 frequency
				# comment 2 frequency
				# comment 3 frequency

				# number of mentions
				len(issue['events']),
				# event 1 frequency
				# event 2 frequency
				# event 3 frequency

				age,
				duration,
			])
