import networkx as nx
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from community import community_louvain
import community

def create_graph(nome_arquivo, nome_arquivo_rel):

    grafo_list = [{"id": 0, "nome": "0", "apelido": "0", "cidade": "0"}]

    arquivo = open(nome_arquivo, 'r')
    arquivo.readline()

    for linha in arquivo:
        new_node = {}

        linha = linha.replace("\n", "")

        id_str = linha.split()[0]
        id = int(id_str)

        nome = linha[linha.find('{')+1:linha.find('}')].strip()

        apelido = linha[linha.find('[')+1:linha.find(']')].strip()

        cidade = re.findall(r'\((.*?)\)', linha)[0].strip()

        new_node["id"] = id
        new_node["nome"] = nome
        new_node["apelido"] = apelido
        new_node["cidade"] = cidade

        grafo_list.append(new_node)

    arquivo.close()

    g = nx.Graph()

    for new_node in grafo_list:
        
        id = new_node['id']
        nome = new_node['nome']
        apelido = new_node['apelido']
        cidade = new_node['cidade']

        
        g.add_node(id, nome=nome, apelido=apelido, cidade=cidade)

    aresta_list = []

    arquivo_rel = open(nome_arquivo_rel, 'r')

    for linha in arquivo_rel:
        node_1, node_2, peso = linha.replace("\n", "").split()

        aresta_list.append({"node_1": int(node_1), "node_2": int(node_2), "peso": int(peso)})

    for aresta in aresta_list:
        node_1 = aresta['node_1']
        node_2 = aresta['node_2']
        peso = aresta['peso']
        
        g.add_edge(node_1, node_2, weight=peso)

    return g

def remove_node(remove_id, nome_arquivo, nome_arquivo_rel):

    grafo_list = [{"id": 0, "nome": "0", "apelido": "0", "cidade": "0"}]

    arquivo = open(nome_arquivo, 'r')
    arquivo.readline()

    for linha in arquivo:
        new_node = {}

        linha = linha.replace("\n", "")

        id_str = linha.split()[0]
        id = int(id_str)

        nome = linha[linha.find('{')+1:linha.find('}')].strip()

        apelido = linha[linha.find('[')+1:linha.find(']')].strip()

        cidade = re.findall(r'\((.*?)\)', linha)[0].strip()

        new_node["id"] = id
        new_node["nome"] = nome
        new_node["apelido"] = apelido
        new_node["cidade"] = cidade

        grafo_list.append(new_node)

    arquivo.close()

    g = nx.Graph()

    for new_node in grafo_list:
        
        id = new_node['id']
        nome = new_node['nome']
        apelido = new_node['apelido']
        cidade = new_node['cidade']

        
        g.add_node(id, nome=nome, apelido=apelido, cidade=cidade)

    aresta_list = []

    arquivo_rel = open(nome_arquivo_rel, 'r')

    for linha in arquivo_rel:
        node_1, node_2, peso = linha.replace("\n", "").split()

        aresta_list.append({"node_1": int(node_1), "node_2": int(node_2), "peso": int(peso)})

    for aresta in aresta_list:
        node_1 = aresta['node_1']
        node_2 = aresta['node_2']
        peso = aresta['peso']


        if node_1 != remove_id and node_2 != remove_id:
            g.add_edge(node_1, node_2, weight=peso)

    return g

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

    nx.draw(g, pos, node_color=list(partition.values()), alpha=0.5, with_labels=False, node_size=20,); plt.show()
    return

def plot_greedy_modularity_communities(g):
    # Definir layout (posicionamento dos nós)
    pos = nx.spring_layout(g)

    # Detectar as comunidades no g (usando um algoritmo de detecção de comunidades)
    comunidades = nx.community.greedy_modularity_communities(g)

    # Criar um dicionário que mapeia cada nó a sua comunidade
    comunidade_dict = {}
    for i, comunidade in enumerate(comunidades):
        for node in comunidade:
            comunidade_dict[node] = i

    cores = ['red', 'blue', 'green', 'yellow', 'purple', 'pink', 'brown', 'orange']  
    nx.draw_networkx_nodes(g, pos, nodelist=comunidade_dict.keys(),
                        node_color=[cores[comunidade_dict[node]] for node in comunidade_dict],
                        node_size=10, alpha=0.5)

    nx.draw_networkx_edges(g, pos, alpha=0.1)

    plt.axis('off')

    return plt.show()

def plot_best_partition_communities(g):
    # Definir layout (posicionamento dos nós)
    pos = nx.spring_layout(g)

    # Executar o algoritmo de detecção de comunidades (Louvain)
    particionamento = community.best_partition(g)

    # Obter o número de comunidades
    comunidades = set(particionamento.values())
    num_comunidades = len(comunidades)

    print("Número de comunidades:", num_comunidades)

    # Plotar os nós, colorindo cada comunidade de uma cor diferente
    cores = ['red', 'blue', 'green', 'yellow', 'purple', 'pink', 'brown', 'orange']  
    nx.draw_networkx_nodes(g, pos, node_size=10,
                        node_color=[cores[particionamento[node]] for node in g.nodes()],
                        alpha=0.5)

    # Plotar as arestas
    nx.draw_networkx_edges(g, pos, alpha=0.1)

    # Remover os eixos
    plt.axis('off')

    # Exibir o g
    return plt.show()

# G = nx.fast_gnp_random_graph(300, 0.75)
# plot_community(G)
