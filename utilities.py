import networkx as nx

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from community import community_louvain

def degree(G,node = None):
    if node == None:
        return G.degree()
    
    return G.degree(node)

def clustering_coeficent(G, node = None):
    if node == None:
        return nx.clustering(G)
    
    return nx.clustering(G, node)

def view(G):
    plt.figure(1, figsize=(12, 8))          
    pos=nx.fruchterman_reingold_layout(G)      
    plt.axis('off')                         
    nx.draw_networkx_nodes(G,pos,node_size=50) 
    nx.draw_networkx_edges(G,pos,alpha=0.4)    
    plt.show() 

def plt_degree_distribution(G):
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    dmax = max(degree_sequence)

    fig = plt.figure("Degree of a random graph", figsize=(8, 8))
    axgrid = fig.add_gridspec(5, 4)

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(degree_sequence, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    plt.show()

def centrality_degree(G):
    degree = nx.degree_centrality(G)    
    return pd.DataFrame.from_dict(data=degree, orient='index')

def centrality_closeness(G):
    closeness = nx.closeness_centrality(G)
    return pd.DataFrame.from_dict(data=closeness, orient='index')

def centrality_betweenness(G):
    betweenness= nx.betweenness_centrality(G)
    return pd.DataFrame.from_dict(data=betweenness, orient='index')

def centrality_eigenvector(G):
    eigenvector = nx.eigenvector_centrality(G)
    return pd.DataFrame.from_dict(data=eigenvector, orient='index')

def centrality_pagerank(G):
    pr = nx.pagerank(G, alpha=0.9)
    return pd.DataFrame.from_dict(data=pr, orient='index')

def community_layout(g, partition):
    """
    Compute the layout for a modular graph.


    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions


    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions

    """

    pos_communities = _position_communities(g, partition, scale=3.) #3

    pos_nodes = _position_nodes(g, partition, scale=1.) #1.

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos

def _position_communities(g, partition, **kwargs):

    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos

def _find_between_community_edges(g, partition):

    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges

def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)

    return pos

def plot_community(g):
    partition = community_louvain.best_partition(g)
    pos = community_layout(g, partition)

    nx.draw(g, pos, node_color=list(partition.values())); plt.show()
    return

G = nx.fast_gnp_random_graph(40, 0.25)
plot_community(G)
