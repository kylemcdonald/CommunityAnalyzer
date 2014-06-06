import time
import subprocess
from subprocess import call

oauthToken = open(".oauthToken", "r").read()
owner = "openframeworks"
repo = "openFrameworks"

def cache(path):
	call(['curl',
		'-u', oauthToken + ':x-oauth-basic',
		'-o', path + ".json",
		'--create-dirs',
		"https://api.github.com/" + path])
#	time.sleep(1)

for i in range(0, 3005):
	number = i + 1
	cache("repos/{}/{}/issues/{}".format(owner, repo, number))
	cache("repos/{}/{}/issues/{}/comments".format(owner, repo, number))
	cache("repos/{}/{}/issues/{}/events".format(owner, repo, number))