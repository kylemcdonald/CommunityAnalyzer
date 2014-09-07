import time
import subprocess
import json
from subprocess import call, check_output

oauthToken = open(".oauthToken", "r").read()
owner = "openframeworks"
repo = "openFrameworks"
issueCount = 3198

remaining = 0
def rate_limit():
	global remaining
	if remaining < 1:
		response = json.loads(check_output(['curl',
			'--silent',
			'-u', oauthToken + ':x-oauth-basic',
			'https://api.github.com/rate_limit']))
		remaining = response['rate']['remaining']
		print('Remaining rate limit requests: {}'.format(remaining))
	else:
		remaining = remaining - 1
	return remaining

def cache(path):
	while rate_limit() < 1:
		print('Waiting for rate limit reset.')
		time.sleep(60)
	call(['curl',
		'--silent',
		'-u', oauthToken + ':x-oauth-basic',
		'-o', path + ".json",
		'--create-dirs',
		'https://api.github.com/' + path])
	print('Downloaded ' + path)


def run():
	for i in range(0, issueCount):
		number = i + 1
		cache("repos/{}/{}/issues/{}".format(owner, repo, number))
		cache("repos/{}/{}/issues/{}/comments".format(owner, repo, number))
		cache("repos/{}/{}/issues/{}/events".format(owner, repo, number))

run()