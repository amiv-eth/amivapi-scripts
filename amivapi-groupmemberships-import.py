#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Sandro Lutz <code@temparus.ch>

import argparse
import requests
import csv
from email.utils import parseaddr

parser = argparse.ArgumentParser(prog='amivapi-groupmemberships-import.py',
          description='Import groupmemberships from CSV file into the AMIVAPI')
parser.add_argument('api_domain', nargs=1, default='api.amiv.ethz.ch', help='Domain under which the AMIVAPI is accessible')
parser.add_argument('api_token', nargs=1, default='root', help='authorization token for the AMIVAPI')
parser.add_argument('group_id', nargs=1, default='Unknown group', help='Group ID')
parser.add_argument('file', nargs=1, type=argparse.FileType('r'),
                   default='users.csv', help='file to import from')
args = parser.parse_args()

host = 'https://' + ''.join(args.api_domain)
headers = {'Authorization': ''.join(args.api_token)}

nethzList = list()
failedList = list()

def findUser(nethz):
  items = requests.get(host + '/users?where={"nethz":"' + nethz + '"}', headers=headers).json()['_items']
  if len(items) != 1:
    raise Exception('User with nethz ' + nethz + ' not found!')
  return items[0]

def addGroupmembership(group_id, user):
  data = {
    'group': group_id,
    'user': user['_id']
  }
  response = requests.post(host + '/groupmemberships', headers=headers, data=data)
  if response.status_code != 201:
    failedList.append(user['nethz'])

# Read users from import file
if (type(args.file) is list):
  reader = csv.DictReader(args.file[-1])
else:
  reader = csv.DictReader(args.file)

unknownUsers = list()

for row in reader:
  try:
    print('------------------------------------')
    user = findUser(row['NETHZ'])

    print('Found user ' + user['nethz'])
    addGroupmembership(args.group_id, user)
  except Exception as e:
    print(e)
    unknownUsers.append(row)

print('----------------------------------------')
print('========================================')
print(str(len(unknownUsers)) + ' unknown Users')
print(str(len(failedList)) + ' failed Users')
print('----------------------------------------')
