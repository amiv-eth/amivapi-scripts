#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Sandro Lutz <code@temparus.ch>

import argparse
import requests
import csv
from email.utils import parseaddr

parser = argparse.ArgumentParser(prog='amivapi-eventsignup-automation.py',
          description='Automatically create eventsignups for an event in the AMIVAPI')
parser.add_argument('api_domain', nargs=1, default='api.amiv.ethz.ch', help='Domain under which the AMIVAPI is accessible')
parser.add_argument('api_token', nargs=1, default='root', help='authorization token for the AMIVAPI')
parser.add_argument('event_id', nargs=1, default='Unknown event', help='Event ID')
args = parser.parse_args()

host = 'https://' + ''.join(args.api_domain)
headers = {'Authorization': ''.join(args.api_token)}

failedList = list()

def processApiUserResponse(response):
  for user in response['_items']:
    data = {
      'event': args.event_id,
      'user': user['_id']
    }
    response2 = requests.post(host + '/eventsignups', headers=headers, data=data)
    if response2.status_code != 201:
      print('failure (' + str(response2.status_code) + '): ' + user['nethz'])
      failedList.append(user['nethz'])

  if 'next' in response['_links']:
    response3 = requests.get(host + '/' + response['_links']['next']['href'], headers=headers).json()
    processApiUserResponse(response3)

print('----------------------------------------')
print('Starting automated process')

response = requests.get(host + '/users?where={"legi":{"$regex":"^18[0-9]*"}}', headers=headers).json()
processApiUserResponse(response)

print('========================================')
print(str(len(failedList)) + ' failed signups')
print('----------------------------------------')
