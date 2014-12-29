#!/usr/bin/env python
import argparse
import os
import pickle
from github import Github

parser = argparse.ArgumentParser(
	description='Collect all issues for a repository.')
parser.add_argument('user')
parser.add_argument('repo')
args = parser.parse_args()

oauthToken = open('../.oauthToken', 'r').read()
github = Github(login_or_token=oauthToken, per_page=100)
user = github.get_user(args.user)
repo = user.get_repo(args.repo)
issues = repo.get_issues(state='all')

path = '{}/{}'.format(args.user, args.repo)

def dump(obj, path, name):
	if not os.path.exists(path):
		os.makedirs(path)
	pickle.dump(obj, open('{}/{}.pkl'.format(path, name), 'w'))

for issue in issues:
	dump(issue, path + '/issues', issue.number)