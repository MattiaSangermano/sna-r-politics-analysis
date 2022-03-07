#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
TODO: add a brief description
'''

import argparse
import os
import sys
import json
import time

from dotenv import load_dotenv
from datetime import datetime

from req.login import login
from req.submissions import submissions
from utils.types import directory, in_file_json

parser = argparse.ArgumentParser(
    description='It crawls submission and related comments from /r/politics for a given time interval'
)
parser.add_argument(
    'startingDate', 
    help='timestamp from which start crawling', 
    type=int
)
parser.add_argument(
    'endingDate', 
    help='timestamp beyond which the crawler stops', 
    type=int,
)
parser.add_argument(
    '--output-dir',    
    help='the path in which to save the output files, by default the output directory is ./data/chunks/', 
    type=directory,
    default='./data/chunks/'
)
parser.add_argument(
    '--max-iter',    
    help='maximum number of iteration of the crawler, by default (0) there is no limit on the number of iterations, each iterations is composed by 100 submissions.', 
    type=int,
    default=0
)
parser.add_argument(
    '--users-file',
    help='file containing previous users in order to improve the speed avodining retrieve the same information, default value is `./data/users.json`',
    type=in_file_json,
    default='./data/users.json'
)
args = parser.parse_args()

starting_date = args.startingDate
ending_date = args.endingDate
output_dir = args.output_dir
max_iter = args.max_iter
users_file = args.users_file

USER_AGENT = 'SNA-bgs-crawler/0.0.1'

# Reads environment variables 
load_dotenv() 

CLIENT_ID = os.environ.get('CLIENT_ID')
SECRET_TOKEN = os.environ.get('SECRET_TOKEN')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

users = {}
if(users_file != None):
    with open(users_file, 'r') as user_file:
        data = user_file.read()
        users = json.loads(data)

def save_chunk(starting_date, results, last_result):
    suffix = 'empty'
    if last_result != None:
        suffix = str(datetime.fromtimestamp(last_result['created_at']))
    prefix = str(datetime.fromtimestamp(starting_date))
    with open(output_dir + '/' + prefix + '_' + suffix + '.json', 'w') as outfile:
        json.dump(results, outfile, indent=1)

def save_users():
    if(users_file != None):
        with open(users_file, 'w') as outfile:
            json.dump(users, outfile, indent=1)

def iteration(i, st_date):
    # Authentication through OAuth
    headers = login(CLIENT_ID, SECRET_TOKEN, USERNAME, PASSWORD, USER_AGENT)
    if headers == 0:
        print('Error: Authentication failed')
        sys.exit(-1)

    it_time = time.time()
    st_date = str(st_date)

    status_code, results, last_result = submissions(st_date, headers, users)

    print('--- Iteration ' + str(i) + ' tooks %s ---' % (time.time() - it_time))
    save_chunk(int(st_date), results, last_result)
    save_users()
    
    return status_code, results, last_result


start_time = time.time()

i = 1
last_date = starting_date
status_code = 200
results = {}
while status_code == 200 and (len(results) > 0 or i == 1) and last_date > ending_date and (max_iter == 0 or i <= max_iter):
    status_code, results, last_result =  iteration(i, str(last_date))
    last_date = int(last_result['created_at']) - 1
    i += 1

print('--- Crawler ended in %s  ---' % (time.time() - start_time))
