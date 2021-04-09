# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
import csv
from matplotlib import pylab
import collections


def community_layout(g, partition):
    pos_communities = _position_communities(g, partition, scale=3.)

    pos_nodes = _position_nodes(g, partition, scale=1.)

    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos

def _position_communities(g, partition, **kwargs):

    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    pos_communities = nx.spring_layout(hypergraph, **kwargs)

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

    #Para valores absolutos
    #degree_sequence = sorted([d for n, d in g.degree()], reverse=True)  # degree sequence
    #degreeCount = collections.Counter(degree_sequence)
    #aux_x, aux_y = zip(*degreeCount.items())

    #Para valores relativos
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


def generate_erdos_renyi_from_current_graph(G):
    return nx.erdos_renyi_graph(len(G.nodes()),nx.density(G))