#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
TODO: add a brief description
'''

import argparse
import json
import os

from utils.types import out_file_json, in_file_json

parser = argparse.ArgumentParser(
    description='It creates the users file from the cleaned data'
)
parser.add_argument(
    '--outputFile', 
    help='output file that will contains all the users, default is ./data/users.json', 
    type=out_file_json,
    default='./data/users.json'
)
parser.add_argument(
    '--dataFile', 
    help='file that contains all the submissions, default is ./data/data.json', 
    type=in_file_json,
    default='./data/data.json'
)
args = parser.parse_args()

output_path = args.outputFile
data_path = args.dataFile

def add_author(post, users):
    try:
        if not post["author"]["id"] in users:
            users[post["author"]["id"]] = post["author"]   
    except TypeError:
        print(post["author"])

users = {}
if os.path.isfile(data_path):
    with open(data_path, 'r') as data_file:
        data = data_file.read()
    submissions = json.loads(data)

    # Goes through each submission and comments
    # in order to add their authors to the users map
    for t3 in submissions:
        add_author(submissions[t3], users)
        for t1 in submissions[t3]["comments"]:
            add_author(submissions[t3]["comments"][t1], users)

# Write the output file
with open(output_path, 'w') as output_file:
    json.dump(users, output_file, indent=1)
