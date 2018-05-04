#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Sandro Lutz <code@temparus.ch>

import argparse
import requests
import csv

parser = argparse.ArgumentParser(prog='amivapi-member-import.py',
          description='Import members from CSV file into the AMIVAPI')
parser.add_argument('api_domain', nargs=1, default='api.amiv.ethz.ch', help='Domain under which the AMIVAPI is accessible')
parser.add_argument('api_token', nargs=1, default='root', help='authorization token for the AMIVAPI')
parser.add_argument('file', nargs=1, type=argparse.FileType('r'),
                   default='members.csv', help='file to import from')
args = parser.parse_args()

# Read member import file
if (type(args.file) is list):
  reader = csv.DictReader(args.file[-1])
else:
  file = csv.DictReader(args.file)

url = 'https://' + ''.join(args.api_domain) + '/users'
headers = {'Authorization': ''.join(args.api_token)}

for row in reader:
  print('------------------------------------')
  print('Adding ' + row['firstname'] + ' ' + row['lastname'])
  r = requests.post(url, headers=headers, data=row)
  print('Response: ' + r.text)
