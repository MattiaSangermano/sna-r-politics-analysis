from os import stat
import networkx as nx
import matplotlib.pyplot as plt
import statistics
import json
import numpy as np
import powerlaw
from collections import Counter
import statistics
import argparse
from tqdm import tqdm

def degree_distribution_hist(prefix=''):
    plt.xlabel('Degree')
    plt.ylabel('#Nodes')
    plt.loglog()

def node_degree(g, directed):
    # Compute degree info
    degree_info = {}

    if not directed:
        pbar = tqdm(total=3)

        pbar.set_description("Computing degree distribution....")
        degree = g.degree()
        counts = Counter(d for n, d in degree)
        degree_hist = [counts.get(i, 0) for i in range(max(counts) + 1)]
        pbar.update(1)

        pbar.set_description("Extracting degree info...")
        degree_fig = plt.figure()
        plt.plot(range(0, len(degree_hist)), degree_hist, '.')
        degree_distribution_hist()
        degree_vec = [d[1] for d in degree]
        degree_info.update({
            'degree_avg': statistics.mean(degree_vec),
            'degree_std': statistics.stdev(degree_vec)
        })
        pbar.update(1)
        
        pbar.set_description("Power low fit...")
        xmin = min(degree_vec)
        degree = np.bincount(degree_vec)
        fit = powerlaw.Fit(np.array(degree)+1, fit_method='KS')#, xmin=xmin, xmax=max(degree)-xmin,discrete=True)

        cdf_fig = plt.figure()
        fit.plot_cdf()
        plt.xlabel('Degree')
        plt.ylabel('CDF')
        ccdf_fig = plt.figure()
        fit.plot_ccdf()
        plt.ylabel('CCDF')
        plt.xlabel('Degree')
        pbar.update(1)
        pbar.set_description("Done...")
        pbar.close()
        
        return degree_info, degree_fig, cdf_fig, ccdf_fig
    else:
        pbar = tqdm(total=3)

        pbar.set_description("Computing in-degree distribution...")
        print('Computing in-out degree...')
        # Compute in degree distribution
        in_degree = g.in_degree()
        in_counts = Counter(d for n, d in in_degree)
        in_degree_hist = [in_counts.get(i, 0) for i in range(max(in_counts) + 1)]
        in_degree_fig = plt.figure()
        plt.plot(range(0, len(in_degree_hist)), in_degree_hist, '.')
        degree_distribution_hist()
        plt.savefig(plot_dir + '/in_degree_distribution.svg')
        pbar.update(1)

        pbar.set_description("Computing out-degree distribution...")
        # Compute out degree distribution
        out_degree = g.out_degree()
        out_counts = Counter(d for n, d in out_degree)
        out_degree_hist = [out_counts.get(i, 0) for i in range(max(out_counts) + 1)]
        out_degree_fig = plt.figure()
        plt.plot(range(0, len(out_degree_hist)), out_degree_hist, '.')
        degree_distribution_hist()
        plt.savefig(plot_dir + '/out_degree_distribution.svg')
        pbar.update(1)

        pbar.set_description("Extracting degree info...")
        in_degree_vec = [d[1] for d in in_degree]
        out_degree_vec = [d[1] for d in out_degree]
        degree_info.update({
            'in_degree_avg': statistics.mean(in_degree_vec),
            'in_degree_std': statistics.stdev(in_degree_vec),
            'out_degree_avg': statistics.mean(out_degree_vec),
            'out_degree_std': statistics.stdev(out_degree_vec)
        })
        pbar.update(1)
        pbar.set_description("Done...")
        pbar.close()

        return degree_info, in_degree_fig, out_degree_fig
