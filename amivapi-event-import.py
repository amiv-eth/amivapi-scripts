#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Sandro Lutz <code@temparus.ch>

import argparse
import requests
import csv
from email.utils import parseaddr

parser = argparse.ArgumentParser(prog='amivapi-event-import.py',
          description='Import members from CSV file into the AMIVAPI')
parser.add_argument('api_domain', nargs=1, default='api.amiv.ethz.ch', help='Domain under which the AMIVAPI is accessible')
parser.add_argument('api_token', nargs=1, default='root', help='authorization token for the AMIVAPI')
parser.add_argument('event_name', nargs=1, default='Unknown event', help='Event Name')
parser.add_argument('file', nargs=1, type=argparse.FileType('r'),
                   default='participants.csv', help='file to import from')
args = parser.parse_args()

host = 'https://' + ''.join(args.api_domain)
headers = {'Authorization': ''.join(args.api_token)}

legiList = list()
nethzList = list()
emailList = list()

failedList = list()

def findUserByLegi(legi):
  items = requests.get(host + '/users?where={"legi":"' + legi + '"}', headers=headers).json()['_items']
  if len(items) != 1:
    legiList.append(legi)
    raise Exception('User with legi ' + legi + ' not found!')
  return items[0]

def findUserByNethz(nethz):
  items = requests.get(host + '/users?where={"nethz":"' + nethz + '"}', headers=headers).json()['_items']
  if len(items) != 1:
    nethzList.append(nethz)
    raise Exception('User with nethz ' + nethz + ' not found!')
  return items[0]

def findUserByEmail(email):
  items = requests.get(host + '/users?where={"email":"' + email + '"}', headers=headers).json()['_items']
  if len(items) != 1:
    emailList.append(email)
    raise Exception('User with email ' + email + ' not found!')
  return items[0]

def findUserByName(firstname, lastname):
  items = requests.get(host + '/users?where={"firstname":"' + firstname + '","lastname":"' + lastname + '"}', headers=headers).json()['_items']
  if len(items) != 1:
    raise Exception('User ' + firstname + ' ' + lastname + ' not found!')
  return items[0]

def findUser(firstname, lastname, email, legi):
  # print('firstname: ' + firstname + ' | lastname: ' + lastname + ' | email: ' + email + ' | legi: ' + legi)
  if legi != None and len(legi) > 0:
    legi = legi.replace('-','')
    try:
      # print('check legi...')
      return findUserByLegi(legi)
    except Exception as e:
      print(e)
      pass
  
  if email != None:
    parsedEmail = email.split('@', 1)
    # print(parsedEmail)
    if parsedEmail[1] in ['student.ethz.ch', 'ethz.ch']:
      try:
        # print('check nethz...')
        return findUserByNethz(parsedEmail[0])
      except:
        pass

    try:
      # print('check email...')
      return findUserByEmail(email)
    except:
      pass

  try:
    print('check name...')
    return findUserByName(firstname, lastname)
  except:
    pass

  raise Exception('Could not find user!')

def addSignup(event, user):
  data = {
    'event': event,
    'user': user['_id']
  }
  response = requests.post(host + '/eventsignups', headers=headers, data=data)
  if response.status_code != 201:
    failedList.append(user['nethz'])

# Create Event
# data = {
#   "title_de": args.event_name,
#   "title_en": args.event_name,
#   "description_de": "Importierter Event",
#   "description_en": "Imported event",
#   "time_start": "2018-04-10T15:16:11Z",
#   "time_end": "2018-04-10T15:16:11Z",
#   "time_advertising_start": "2018-04-10T15:16:11Z",
#   "time_advertising_end": "2018-04-20T15:16:11Z",
#   "priority": 5,
#   "spots": 0,
#   "allow_email_signup": True,
#   "selection_strategy": "fcfs"
# }

# event = requests.post(host + '/events', headers=headers, data=data).json()

event = '5acf559044a1a1000103d95e'

# Read participants import file
if (type(args.file) is list):
  reader = csv.DictReader(args.file[-1])
else:
  reader = csv.DictReader(args.file)

unknownUsers = list()

for row in reader:
  try:
    print('------------------------------------')
    user = findUser(row['FIRSTNAME'], row['NAME'], row['EMAIL'], row['LEGI'])

    print('Found user ' + user['nethz'])
    addSignup(event, user)
  except Exception as e:
    print(e)
    unknownUsers.append(row)

print('----------------------------------------')
print('========================================')
print(str(len(unknownUsers)) + ' unknown Users')
print('----------------------------------------')
print(str(len(legiList)) + ' legiList')
print(str(len(nethzList)) + ' nethzList')
print(str(len(emailList)) + ' emailList')
print(str(len(failedList)) + ' failedList')

print(' '.join(nethzList))
print(' '.join(legiList))
print(' '.join(emailList))
print('***********************')
print(' '.join(failedList))

