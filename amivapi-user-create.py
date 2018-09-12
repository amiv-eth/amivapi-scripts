#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Sandro Lutz <code@temparus.ch>

import argparse
import requests
import csv

parser = argparse.ArgumentParser(prog='amivapi-user-create.py',
          description='Import members from CSV file into the AMIVAPI')
parser.add_argument('api_domain', nargs=1, default='apii.amiv.ethz.ch', help='Domain under which the AMIVAPI is accessible')
parser.add_argument('api_token', nargs=1, default='root', help='authorization token for the AMIVAPI')
args = parser.parse_args()

url = 'https://' + ''.join(args.api_domain) + '/users'
headers = {'Authorization': ''.join(args.api_token)}

for i in range(1,21):
  print('------------------------------------')
  print('User:   testuser' + str(i))
  print('Passwd: test123')
  data = {
    "nethz": "testuser" + str(i),
    "firstname": "Hans",
    "lastname": "Muster",
    "membership": "regular",
    "department": "itet",
    "gender": "male",
    "password": "test123",
    "email": "hans.muster@ethz.ch",
    "send_newsletter": False
  };
  r = requests.post(url, headers=headers, data=data)
  # print('Response: ' + r.text)

