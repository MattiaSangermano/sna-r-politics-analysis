#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
It uses the cralwed data and the labels in order to create the graph
on which the next phases relies on.
'''

import argparse
import json
import operator

import networkx as nx

from utils.types import in_file_json, out_file_gexf

parser = argparse.ArgumentParser(
    description='It builds the network given the crawled data'
)
parser.add_argument(
    '--usersFile', 
    help='file containing all the users crawled', 
    type=in_file_json,
    default='./data/users.json'
)
parser.add_argument(
    '--dataFile', 
    help='file containing all the data crawled', 
    type=in_file_json,
    default='./data/data.json'
)
parser.add_argument(
    '--outputFile', 
    help='output file in gexf format, default is ./data/BGS.gexf', 
    type=out_file_gexf,
    default='./data/GS.gexf'
)
parser.add_argument(
    '--geoFile', 
    help='file containing geo information, default is ./model/geo.json', 
    type=in_file_json,
    default='./data/geo.json'
)
parser.add_argument(
    '--labelsFile', 
    help='file containing labels information, default is ./data/labels.json', 
    type=in_file_json,
    default='./data/labels.json'
)
args = parser.parse_args()

users_file = args.usersFile
geo_file = args.geoFile
data_file = args.dataFile
output_file = args.outputFile
labels_file = args.labelsFile

# Reads input
users = {}
with open(users_file, 'r') as user_file:
    data = user_file.read()
    users = json.loads(data)

submissions = {}
with open(data_file, 'r') as data_file:
    data = data_file.read()
    submissions = json.loads(data)

geo_data = {}
with open(geo_file, 'r') as geo_file:
    data = geo_file.read()
    geo_data = json.loads(data)

labels_data = {}
with open(labels_file, 'r') as labels_file:
    data = labels_file.read()
    labels_data = json.loads(data)

geo_not_found = 0
labels_not_found = 0

# For each users found in the usersFile add the corresponding node
G = nx.DiGraph()
for t2 in users:
    G.add_node(t2, data=users[t2], submissions={})
    
    if t2 in labels_data:
        for key in labels_data[t2]['toxicity'].keys():
            G.nodes[t2]['labels_' + key] = labels_data[t2]['toxicity'][key]
        G.nodes[t2]['labels_political_leaning'] = labels_data[t2]['political_leaning']
        if G.nodes[t2]['labels_political_leaning'] >= 0.5:
            G.nodes[t2]['labels_political_leaning_cat'] = 'r'
        else:
            G.nodes[t2]['labels_political_leaning_cat'] = 'l'
    else:
        labels_not_found += 1

    # Geographical information
    if users[t2]["name"] in geo_data:
        countries = {}
        for val in geo_data[users[t2]["name"]]:
            key = geo_data[users[t2]["name"]][val][0]
            if not key in countries:
                countries[key] = 0
            countries[key] += 1
        G.nodes[t2]["geo"] =  max(countries.items(), key=operator.itemgetter(1))[0]
    else:
        G.nodes[t2]["geo"] = "None"
        geo_not_found += 1
    
for t3 in submissions:
    submission = submissions[t3]

    comments = submission['comments']
    if submission['author'] != '@Error:404_not_found':
        del submission['comments']

        if submission['id'] in labels_data:
            submission['labels'] = labels_data[submission['id']]
        else:
            labels_not_found += 1

        G.nodes[submission['author']['id']]['submissions'][submission['id']] = submission

    for t1 in comments:
        in_author = comments[t1]['author']['id']
        out_author = None

        parent_id = comments[t1]['parent_id']

        if 't3_' in parent_id:
            out_author = submissions[parent_id]['author']['id']
        elif parent_id in comments:
            out_author = comments[parent_id]['author']['id']

        if not out_author is None:        
            if not G.has_edge(in_author, out_author):
                G.add_edge(in_author, out_author, weight=0, comments={})

            if t1 in labels_data:
                comments[t1]['labels'] = labels_data[t1]
            else:
                labels_not_found += 1

            G.edges[(in_author, out_author)]['comments'][comments[t1]['id']] = comments[t1]
            G.edges[(in_author, out_author)]['weight'] += 1

nx.write_gexf(G, output_file)

print("Geo not found: " + str(geo_not_found))
print("Labels not found: " + str(labels_not_found))

