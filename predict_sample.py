# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
import csv
from matplotlib import pylab
import networkx_functions as nx_aux

cast_list = ['Will Smith - 6.93', 'Adam Sandler - 6.00', 'Mila Kunis - 6.26', 'Keanu Reeves 6.25', 'Rodrigo Santoro - 5.45', 'Carrie Fisher 7.0']

G = nx.Graph()
G.add_nodes_from(cast_list)

for i in range(len(cast_list)):
    for j in range(i+1,len(cast_list)):
        G.add_edge(cast_list[i], cast_list[j])



nx.draw(G, with_labels=True, font_weight='bold')

plt.show()