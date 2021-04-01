# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab
from networkx.algorithms import community



with open('netflix_titles.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
#    rows = filter(lambda x: float(x[-1]) > 0, list(reader)[1:100])
    rows = list(reader)[1:]


#Fazendo parse e tratando ista de todos atores
lista_atores = [ [x.strip() for x in x[4].split(',')] for x in rows]
flat_list = [item for sublist in lista_atores for item in sublist]
atores = sorted(set(list(filter(None, flat_list))))


G = nx.Graph()


#adicionando os vértices
for linha in rows:
	cast_list = [x.strip() for x in linha[4].split(',')]
	for i in range(len(cast_list)):
		for j in range(i+1,len(cast_list)):
#			G.add_edge(cast_list[i], cast_list[j], weight=float(linha[-1]))
			G.add_edge(cast_list[i], cast_list[j])




largest_cc = max(nx.connected_components(G), key=len)
G = G.subgraph(largest_cc)

elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 7]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 7]

pos=nx.spring_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=50)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
nx.draw_networkx_edges(
    G, pos, edgelist=esmall, width=1, alpha=0.3, edge_color="b", style="dashed"
)

# labels
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
nx.draw_networkx_labels(G, pos, font_size=16, font_family="sans-serif")


ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()

plt.savefig("graph.pdf")
plt.show()
