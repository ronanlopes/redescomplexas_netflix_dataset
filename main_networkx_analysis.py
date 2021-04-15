# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
import csv
from matplotlib import pylab
import networkx_functions as nx_aux




with open('output_imdb.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
#    rows = filter(lambda x: float(x[-1]) > 0, list(reader)[1:100])
    rows = list(reader)[1:]


#Fazendo parse e tratando ista de todos atores
lista_com_notas = filter(lambda x: float(x[-1])>0, rows)
lista_atores = [ [x.strip() for x in x[4].split(',')] for x in rows]
flat_list = [item for sublist in lista_atores for item in sublist]
atores = sorted(set(list(filter(None, flat_list))))


G = nx.Graph()

G.add_nodes_from(atores)


#adicionando os vértices
for linha in rows:
    cast_list = [x.strip() for x in linha[4].split(',')]
    for i in range(len(cast_list)):
        for j in range(i+1,len(cast_list)):
#           G.add_edge(cast_list[i], cast_list[j], weight=float(linha[-1]))
            G.add_edge(cast_list[i], cast_list[j])






largest_cc = max(nx.connected_components(G), key=len)
GCC = G.subgraph(largest_cc)


# Para obter o grafo com nós fora da componente principal
#G = G.subgraph(set(G.nodes()).difference(largest_cc))



###################################################################
#Métricas da rede e dos nós
###################################################################
nx.density(GCC)
nx.average_clustering(GCC)
triadic_closure = nx.transitivity(GCC)
nx.graph_number_of_cliques(GCC)
nx.diameter(GCC)
nx.average_shortest_path_length(GCC)
nx.number_connected_components(G)

#Medidas de centralidade
c = nx.closeness_centrality(GCC)
b = nx.betweenness_centrality(GCC)
e = nx.eigenvector_centrality(GCC)
sorted_x = sorted(c.items(), key=operator.itemgetter(1), reverse=True)[:10] #para obter a resposta ordenada pelos valores dos dicionários

###################################################################
#detecção de comunidades
###################################################################

partition = community_louvain.best_partition(GCC)
len(set(partition.values())) #número de comunidades

#Agrupando em dicionário onde chave é a comunidade e valores os vértices pertencentes
res = {}
for i, v in partition.items():
	res[v] = [i] if v not in res.keys() else res[v] + [i]

max(len(val) for val in res.values()) #número de nós da maior comunidade
min(len(val) for val in res.values()) #número de nós da menor comunidade
np.mean(list(len(val) for val in res.values())) #média

###################################################################
#Outras funções utilitárias
###################################################################

#exportar para visualizar no gephi
nx.write_gexf(G, "netflix_titles.gexf")
