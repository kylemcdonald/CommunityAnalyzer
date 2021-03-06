import json
from pprint import pprint
import dateutil.parser
import csv
import numpy

data = json.load(open('data/merged.json'))
first = dateutil.parser.parse(data[0]['created_at'])
secondsPerDay = 60 * 60 * 24
secondsPerWeek = secondsPerDay * 7
secondsPerMonth = secondsPerDay * 30

# more features to consider:
# - recent issue frequency (i.e., bug fix marathons)

# for each event that happens, we have a snapshot of the issue at a different state
# we can use it as a datapoint, where we save all that we know at that moment
# plus the amuont of time left to close the issue

# add liwc

with open('data/flat.tab', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter='\t')
	info = [
		# 'id', 'c', '',

		'title length', 'c', '',
		'body length', 'c', '',
		'label count', 'c', '',

		'is pull request', 'd', '',

		'has milestone', 'd', '',

		'user count', 'c', '',
		'comment count', 'c', '',
		'user comment ratio', 'c', '',
		'multiple posts', 'd', '',
		'comments length', 'c', '',
		'comments average length', 'c', '',
		'first comment frequency', 'c', '',

		'long pause frequency', 'c', '',
		'short pause frequency', 'c', '',
		'pause deviation', 'c', '',

		'event count', 'c', '',

		'age', 'c', '',
		# 'close frequency', 'c', 'class',
		'duration', 'c', '',
		'close category', 'd', 'class'
	]
	writer.writerow(info[0::3])
	writer.writerow(info[1::3])
	writer.writerow(info[2::3])

	for issue in data:
		id = issue['id']
		created_at = dateutil.parser.parse(issue['created_at'])
		age = (created_at - first).total_seconds() / secondsPerDay
		closed_at = None
		duration = None
		closeCategory = 'Long'
		if issue['closed_at'] is not None:
			closed_at = dateutil.parser.parse(issue['closed_at'])
			duration = (closed_at - created_at).total_seconds()
			if duration < secondsPerMonth:
				closeCategory = 'Short'
		else:
			duration = float("inf")
		closeFrequency = float(secondsPerDay) / duration

		commentCount = len(issue['comments'])
		users = set()
		commentsLength = 0
		commentTimes = [created_at]
		for comment in issue['comments']:
			users.add(comment['user'])
			commentsLength += len(comment['body'])
			commentTimes.append(dateutil.parser.parse(comment['created_at']))
		userCount = len(users)
		commentUserRatio = 1
		commentsLengthAverage = 0
		firstCommentFrequency = 0
		longestPauseFrequency = 0
		shortestPauseFrequency = 0
		pauseDeviation = 0
		if commentCount > 0:
			commentUserRatio = float(userCount) / commentCount
			commentsLengthAverage = float(commentsLength) / commentCount 
			firstCommentTime = dateutil.parser.parse(issue['comments'][0]['created_at'])
			firstCommentDuration = (firstCommentTime - created_at).total_seconds()
			firstCommentFrequency = float(secondsPerDay) / firstCommentDuration
			commentPauses = [b - a for a, b in zip(commentTimes[:-1], commentTimes[1:])]
			commentPauses = [(x.total_seconds() + 1) / float(secondsPerDay) for x in commentPauses]
			longestPause = max(commentPauses)
			shortestPause = min(commentPauses)
			longestPauseFrequency = 1 / longestPause
			shortestPauseFrequency = 1 / shortestPause
			pauseDeviation = numpy.std(commentPauses)

		writer.writerow([
			# id,

			len(issue['title']),
			len(issue['body']),	
			len(issue['labels']),

			issue['pull_request'],

			issue['milestone'] != '',

			userCount,
			commentCount,
			commentUserRatio,
			commentCount > userCount,
			commentsLength,
			commentsLengthAverage,
			firstCommentFrequency,

			longestPauseFrequency,
			shortestPauseFrequency,
			pauseDeviation,

			len(issue['events']),

			age,
			# closeFrequency,
			duration,
			closeCategory
		])
