import time
import subprocess
from subprocess import call

oauthToken = open(".oauthToken", "r").read()
user = "openframeworks"
repo = "openFrameworks"

def cache(path):
	call(['curl',
		'-u', oauthToken + ':x-oauth-basic',
		'-o', path + ".json",
		'--create-dirs',
		"https://api.github.com/" + path])
	time.sleep(1)

issues = 3005
for i in range(issues):
	issue = i + 1
	path = "repos/{}/{}/issues/{}/comments".format(user, repo, issue)
	cache(path)