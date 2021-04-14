# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
import csv
from matplotlib import pylab
import networkx_functions as nx_aux
import math
from sklearn.linear_model import LinearRegression
import scipy.stats


def plotFuncaoLinear(medias,notas,x,model):

	# Plot outputs
	plt.scatter(x, y,  color='black', s=2)
	plt.plot(x, model.predict(x), color='blue', linewidth=3)

	axes = plt.gca()
	axes.set_xlim([0,10])
	axes.set_ylim([0,10])
	plt.xticks(np.arange(0, 10, 1.0))
	plt.title("Função Linear de Predição f(x) = ax + b".decode("utf-8"))

	plt.show()



with open('imdb_mean.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
#    rows = filter(lambda x: float(x[-1]) > 0, list(reader)[1:100])
    rows = list(reader)[1:]

G = nx.Graph()

for ator in rows:
	G.add_node(ator[0], weight=float(ator[1]))



with open('output_imdb.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
#    rows = filter(lambda x: float(x[-1]) > 0, list(reader)[1:100])
    rows = list(reader)[1:]


#Fazendo parse e tratando ista de todos atores
lista_com_notas = filter(lambda x: float(x[-1])>0, rows)


#adicionando os vértices
for linha in lista_com_notas:
    cast_list = [x.strip() for x in linha[4].split(',')]
    for i in range(len(cast_list)):
        for j in range(i+1,len(cast_list)):
#           G.add_edge(cast_list[i], cast_list[j], weight=float(linha[-1]))
            G.add_edge(cast_list[i], cast_list[j])


#Utilizando a componente gigante
largest_cc = max(nx.connected_components(G), key=len)
GCC = G.subgraph(largest_cc)


###################################################################
#Obtendo uma predição através das médias dos vizinhos
###################################################################
notas=[]
medias=[]
erros=[]
for node in GCC.nodes():
	vizinhos = nx.single_source_shortest_path_length(GCC, node, cutoff=1).keys()
	nota_node = GCC.nodes[node]['weight']
	media_vizinhos = np.mean(list(map(lambda x: GCC.nodes[x]['weight'], vizinhos)))
	notas.append(nota_node)
	medias.append(media_vizinhos)
	erro = math.sqrt((nota_node-media_vizinhos)**2)
	erros.append(erro)
	#print "\n\nNó: "+str(node)
	#print "Nota do Nó: "+str(nota_node)
	#print "Média dos Vizinhos: "+str(media_vizinhos)
	#print "Erro: "+str(erro)


media_erros = np.mean(erros)
print "Correlação de Pearson: "+str(scipy.stats.pearsonr(medias,notas)[0])


print "Média dos vizinhos diretos"
print "Média de erros: "+str(media_erros)


###################################################################
#Obtendo uma predição por modelo de regressão linear simples
###################################################################

x = np.array(medias).reshape((-1, 1))
y = np.array(notas)
model = LinearRegression().fit(x,y)
coeficiente = model.coef_[0]

print "Função linear simples: "+str(coeficiente)+"x "+str(model.intercept_)
print "Erro quadrático do modelo: "+str(model.score(x, y))
print "Diferença média na predição: "+str(np.mean(map(lambda x: math.sqrt(x), (np.array(notas)-np.array(model.predict(x)))**2)))

plotFuncaoLinear(medias,notas,x,model)


# Cálculo manual baseado no coeficiente e intercept para conferÊncia
erros=[]
for node in GCC.nodes():
	vizinhos = nx.single_source_shortest_path_length(GCC, node, cutoff=1).keys()
	nota_node = float(GCC.nodes[node]['weight'])
	notas_vizinhos = list(map(lambda x: GCC.nodes[x]['weight'], vizinhos))
	media_vizinhos = np.mean(notas_vizinhos)
	valor_predito = coeficiente*media_vizinhos+model.intercept_
	erro = math.sqrt((nota_node-valor_predito)**2)
	erros.append(erro)
	#print "\n\nNó: "+str(node)
	#print "Nota do Nó: "+str(nota_node)
	#print "Média dos Vizinhos: "+str(media_vizinhos)
	#print "Valor Predito: "+str(valor_predito)
	#print "Erro "+str(erro)


media_erros = np.mean(erros)
print "Média de erros: "+str(media_erros)


###################################################################
#Obtendo uma predição por modelo de regressão linear (múltiplos valores - de n níveis de vizinhos)
###################################################################

profundidade = 2
#x = [[] for i in range(profundidade)]
x = []
for node in GCC.nodes():
	notas_n_vizinhos = nx.single_source_shortest_path_length(GCC, node, cutoff=profundidade)
	notas_n_vizinhos = {k:v for k,v in notas_n_vizinhos.iteritems() if k not in [node]}
	res = {}
	for i, v in notas_n_vizinhos.items():
		res[v] = [i] if v not in res.keys() else res[v] + [i]
	m = map(lambda x: np.mean(map(lambda node: GCC.nodes[node]['weight'],x)), res.values())
	x.append(m)
	#map(lambda e: x[m.index(e)].append(e), m)


model = LinearRegression().fit(np.array(x),np.array(y))


print "Função linear multivariável (n vizinhos)"
print "Coeficientes: "+str(model.coef_)
print "Intercept: "+str(model.intercept_)
print "Erro quadrático do modelo: "+str(model.score(x, y))
print "Diferença média na predição: "+str(np.mean(map(lambda x: math.sqrt(x), (np.array(notas)-np.array(model.predict(x)))**2)))