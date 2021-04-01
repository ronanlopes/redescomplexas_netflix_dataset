# -*- coding: utf-8 -*-
from igraph import *
import csv

with open('netflix_titles.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    rows = list(reader)

#Fazendo parse e tratando ista de todos atores
lista_atores = [ [x.strip() for x in x[4].split(',')] for x in rows]
flat_list = [item for sublist in lista_atores for item in sublist]
atores = sorted(set(list(filter(None, flat_list))))


#inicializando Grafo
g = Graph()
g.add_vertices(len(atores))
g.vs["name"]=atores


#adicionando os vértices

for linha in rows:
	cast_list = [x.strip() for x in linha[4].split(',')]
	for i in range(len(cast_list)):
		for j in range(i+1,len(cast_list)):
			g.add_edge(cast_list[i],cast_list[j])




visual_style = {}
visual_style["layout"]="kk"
visual_style["vertex_label"]=g.vs["name"]

plot(g, **visual_style)

