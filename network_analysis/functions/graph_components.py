import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

def build_hist(components):
    sizes_counter = {}
    sizes = [len(component) for component in components]
    for size in sizes:
        if not size in sizes_counter:
            sizes_counter[size] = 0
        sizes_counter[size] += 1
    sorted_keys = sorted(sizes_counter.keys())
    fig = plt.figure()
    plt.grid()
    plt.yscale('log')
    plt.scatter(x=[str(v) for v in sorted_keys], y=[sizes_counter[v] for v in sorted_keys]) 
    plt.plot([str(v) for v in sorted_keys], [sizes_counter[v] for v in sorted_keys]) 
    plt.ylabel('#Components')
    plt.xlabel('#Nodes')
    return fig, sizes_counter

def graph_components(G, directed=0):
    if directed:
        pbar = tqdm(total=5)
    else:
        pbar = tqdm(total=2)
    if directed:
        # Analysis of weakly connected components
        pbar.set_description("Analyzing weekly connected components...")
        weakly_components = list(nx.weakly_connected_components(G))
        weekly_components_res = build_hist(weakly_components)
        pbar.update(1)

        # Save the giant component
        pbar.set_description("Retrieving the giant weekly connected component...")
        directed_giant_component = nx.subgraph(G, max(weakly_components, key=len))
        pbar.update(1)

        # Analysis of strongly connected components
        pbar.set_description("Analyzing strongly connected components...")
        strongly_components = list(nx.strongly_connected_components(G))
        strongly_components_res = build_hist(strongly_components)
        pbar.update(1)        

        G = G.to_undirected()

    pbar.set_description("Analyzing connected components...")
    connected_components = list(nx.connected_components(G))
    connected_components_res = build_hist(connected_components)
    pbar.update(1)    

    # Save the giant component
    pbar.set_description("Retrieving the giant component...")
    giant_component = nx.subgraph(G, max(connected_components, key=len))
    pbar.update(1)    
    pbar.set_description("Done...")
    pbar.close()

    if directed:
        return giant_component, directed_giant_component, connected_components_res, weekly_components_res, strongly_components_res
    return giant_component, connected_components_res
