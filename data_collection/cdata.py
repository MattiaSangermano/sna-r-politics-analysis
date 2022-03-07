#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
TODO: add a brief description
'''

import argparse

import os
import json

from utils.types import directory, out_file_json

parser = argparse.ArgumentParser(
    description='It creates a cleaned version of the crawled data'
)
parser.add_argument(
    '--outputFile', 
    help='output file that will contains all the submissions, default is ./data/data.json', 
    type=out_file_json,
    default='./data/data.json'
)
parser.add_argument(
    '--dataDirectory', 
    help='directory containing all the chunks crawled, default is ./data/chunks/', 
    type=directory,
    default='./data/chunks/'
)
args = parser.parse_args()

output_file = args.outputFile
data_directory = args.dataDirectory

result = {}

# For each file in the data directory open the file and read its content
for file_name in os.listdir(data_directory):
    if ".json" in file_name:
        # Load chunk content
        chunk_path = os.path.join(data_directory, file_name)
        if os.path.isfile(chunk_path):
            with open(chunk_path, 'r') as chunk_file:
                chunk_data = chunk_file.read()
            chunk = json.loads(chunk_data)

            # Goes trough each submission of a chunk
            for t3 in chunk:
                submission = chunk[t3]

                # Checks if:
                #   - The submission has been already added avoiding duplicates
                #   - Author is found correctly
                if not t3 in result and submission["author"] != None and type(submission["author"]) != int and submission["author"] != "@Error:404_not_found":
                    comments = submission["comments"]
                    delete = []

                    # Goes trough each comments of the submission
                    for t1 in comments:
                        comment = submission["comments"][t1]
                        in_author = comment["author"]
                        out_author = None
                        parent_id = comment["parent_id"]

                        # Try to find the author corresponding to the parent_id 
                        # (i.e. the post to which the comments reply to)
                        if "t3_" in parent_id:
                            out_author = chunk[parent_id]["author"]
                        elif parent_id in comments:
                            out_author = comments[parent_id]["author"]
                        
                        # Whenever the author of the comments or the author of
                        # the post which the comments reply to does not exists
                        # the comments is added to delete list and will be deleted
                        if out_author == None or type(out_author) == int or out_author == "@Error:404_not_found" or in_author == "@Error:404_not_found" or type(in_author) == int:
                            delete.append(t1)
                    for t1 in delete:
                        del submission["comments"][t1]
                    
                    result[t3] = submission

# Write the output file
with open(output_file, 'w') as outfile:
    json.dump(result, outfile, indent=1)
