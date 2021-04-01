# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
import csv
from matplotlib import pylab

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

    pos_communities = _position_communities(g, partition, scale=3.)

    pos_nodes = _position_nodes(g, partition, scale=1.)

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


def plot_degree_histogram(g, normalized=True):
    aux_y = nx.degree_histogram(g)
    aux_x = np.arange(0,len(aux_y)).tolist()
    n_nodes = g.number_of_nodes()
    if normalized:
        for i in range(len(aux_y)):
            aux_y[i] = float(aux_y[i])/n_nodes


    plt.title('\nDistribuição de Graus da Rede'.decode('utf-8'))
    plt.xlabel('Grau (log)'.decode('utf-8'))
    plt.ylabel('Probabilidade'.decode('utf-8'))
    plt.xscale("log")
    #plt.yscale("log")
    plt.plot(aux_x, aux_y, 'o')
    plt.show()



def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)
    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig



#g = nx.karate_club_graph()



with open('netflix_titles.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
#    rows = filter(lambda x: float(x[-1]) > 0, list(reader)[1:100])
    rows = list(reader)[1:]



G = nx.Graph()

#adicionando os vértices
for linha in rows:
    cast_list = [x.strip() for x in linha[4].split(',')]
    for i in range(len(cast_list)):
        for j in range(i+1,len(cast_list)):
#           G.add_edge(cast_list[i], cast_list[j], weight=float(linha[-1]))
            G.add_edge(cast_list[i], cast_list[j])






largest_cc = max(nx.connected_components(G), key=len)
G = G.subgraph(largest_cc)



partition = community_louvain.best_partition(G)
#pos=nx.spring_layout(G)
pos = community_layout(G, partition)


nx.draw(G, pos, node_color=list(partition.values())); plt.show()



nx.write_gexf(G, "test.gexf")