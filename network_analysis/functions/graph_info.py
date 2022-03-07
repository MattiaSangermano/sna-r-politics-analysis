import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import json
import statistics
import argparse

def graph_info(g, weighted):
    if weighted:
        weights = [int(d['weight']) for (_, _, d) in g.edges(data=True)]

        fig = plt.figure()
        counts = Counter(weights)
        weights_hist = [counts.get(i, 0) for i in range(max(counts) + 1)]
        plt.plot(range(0, len(weights_hist)), weights_hist, '.')
        plt.xlabel('Weights')
        plt.ylabel('#Nodes')
        plt.loglog()

    # Collecting some graph info
    print('Collecting some graph info...')
    graph_info = {
        'nodes': len(g.nodes),
        'edges': len(g.edges),
        'density': nx.density(g),
    }
    if weighted:
        graph_info['weights_avg'] = statistics.mean(weights)
        graph_info['weights_std'] = statistics.stdev(weights)
        return graph_info, fig 
    return graph_info
