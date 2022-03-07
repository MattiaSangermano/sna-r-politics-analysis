import networkx as nx
import matplotlib.pyplot as plt
import json
import statistics
from tqdm import tqdm

def clustering_coefficient(g):
    pbar = tqdm(total=1)
    
    pbar.set_description("Computing clustering coefficient...")
    # Clustering coefficient
    clustering_coefficient = nx.clustering(g)
    clustering_coefficient_values = clustering_coefficient.values()

    fig =plt.figure()
    plt.boxplot(clustering_coefficient_values)
    plt.yscale('log')

    clustering_info = {
        'clustering_avg': statistics.mean(clustering_coefficient_values),
        'clustering_std': statistics.stdev(clustering_coefficient_values)
    }
    pbar.update(1)
    pbar.set_description("Done...")
    pbar.close()


    return clustering_info, fig
