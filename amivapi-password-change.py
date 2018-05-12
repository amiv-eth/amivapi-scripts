#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Sandro Lutz <code@temparus.ch>

import argparse
import getpass
import requests
import sys

parser = argparse.ArgumentParser(prog='amivapi-password-change.py',
          description='Changes the password of a user at AMIV API')
parser.add_argument('username', nargs=1, help='Username for which to change the password')
args = parser.parse_args()

username = ''.join(args.username)

print('Changing the password for user "' + username + '"')

current_password = getpass.getpass('Current Password: ')
new_password = getpass.getpass('New Password: ')
new_password2 = getpass.getpass('Confirm New Password: ')

if (new_password != new_password2):
  print('The new passwords did not match.')
  sys.exit()

apiUrl = 'https://api.amiv.ethz.ch/'

r = requests.post(apiUrl + 'sessions?embedded={"user":1}', data={ 'username': username, 'password': current_password })
if r.status_code != 201:
  print('Authentication failed with AMIV API.')
  sys.exit()

session = r.json()
headers = { 'Authorization': session['token'], 'If-Match': session['user']['_etag'] }

r = requests.patch(apiUrl + 'users/' + session['user']['_id'], headers=headers, data={ 'password': new_password })

if r.status_code != 200:
  print('Something went wrong. Please try it again.')
else:
  print('Password for user "' + username + '" changed successfully!')
