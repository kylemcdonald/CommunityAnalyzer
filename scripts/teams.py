#!/usr/bin/env python

# http://jacquev6.net/PyGithub/v1/apis.html

import argparse
import os
import pickle
from github import Github

parser = argparse.ArgumentParser(
	description='Print a list of team members for an organization.')
parser.add_argument('org')
args = parser.parse_args()

oauthToken = open('../.oauthToken', 'r').read()
github = Github(login_or_token=oauthToken, per_page=100)
organization = github.get_organization(args.org)
teams = organization.get_teams()

print('<ul>')
for team in teams:
	members = team.get_members()
	text = []
	for member in members:
		if member.name:
			text.append(u'<a href="{}">{}</a> ({})'.format(member.html_url, member.name, member.login))
		else:
			text.append(u'<a href="{}">{}</a>'.format(member.html_url, member.login))
	print(u'\t<li><b>{}</b>: {}</li>'.format(team.name, u', '.join(text)))
print('</ul>')
