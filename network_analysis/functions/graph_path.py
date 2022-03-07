import networkx as nx
import json
import numpy as np

import argparse

from itertools import combinations

def graph_path(G, iterations):
    result = 0
    samples = set([])
    diameter = 0

    # Compute shortest path length
    print('Analyzing the shortest paths...')

    while len(samples) < iterations:
        i = int(np.random.randint(low = 0, high = len(G.nodes()) - 1, size=1)[0])
        j = int(np.random.randint(low = 0, high = len(G.nodes()) - 1, size=1)[0])
        if i != j and not (i, j) in samples:
            samples.update([(i, j)])

    for sample in samples:
        i, j = sample
        val = nx.shortest_path_length(G, list(G.nodes())[i], list(G.nodes())[j])
        if val > diameter:
            diameter = val
        result += val

    print('Analysis completed.')

    result = result / len(samples)
    return {
        '#samples': len(samples),
        '<d>': result,
        'diameter': diameter
    }
