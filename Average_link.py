'''
	O algoritmo ao invez de separar os dataframes para representar clusters diferentes, ele cria uma nova coluna 
	chamada 'cluster' sendo que cada número representa um cluster diferente.

'''

import pandas as pd
import numpy as np
import math
import random
#from pandas.plotting import lag_plot

#printar no terminal do linux
import matplotlib.pyplot as plt
import scipy as sp  # SciPy (signal and image processing library)
import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
from pylab import *              # Matplotlib's pylab interface
from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.spatial.distance as ssd

#dataframe
data = None
#Quantidade de clusters
k_Min = 0
k_Max = 0

#Acha a distância média entre os objetos do cluster
def min_value_matrix(matrix) :
	dist_min = 10000

	row = 0
	column = 0

	for x in range(len(matrix)) :
		for y in range(x):
			if dist_min > matrix[x][y] and matrix[x][y] > 0:
				dist_min = matrix[x][y]
				row = x
				column = y

	if row > column:
		return(dist_min, column, row)
	else:
		return(dist_min, row, column)	
				
def dist_euclid(x1,y1,x2,y2) :
	return (((x1 - x2) ** 2) + ((y1 - y2) ** 2 )) ** (1/2)

def print_matrix(matrix) :
	for a in matrix:
		print(a)

def main() :

	global data, k_Min, k_Max

	entrada = input("Insira o nome do arquivo, e o intervalo do número de clustes (k min e k max) separados por um espaço:\n")

	#Recebe a entrada na ordem : Nome do arquivo, k-min e k-max
	arq, k_Min, k_Max = entrada.split(" ")

	#Converte as variaves de str para int
	k_Max = int(k_Max)
	k_Min = int(k_Min)

	#Lê o arquivo dado e cria uma dataframe com ele
	data = pd.read_csv('datasets/' + arq, delimiter = "\t")

	#Pega a quantidade de objetos existentes
	qtd = data.shape[0]

	#Insere uma nova coluna chamado cluster com o valor = 0
	data['cluster'] = range(1, qtd + 1)

	#Matriz usada para armazenar as distancias de cada cluster
	dist_matrix = [ [] for _ in range(qtd)]

	#Lista usada para armazenar o numero do cluster e a quais objetos estão inclusos no cluster
	clusters = [[] for _ in range(qtd)]

	#Lista usado para montar o histograma
	dend = []

	#Insere na matriz os valores das distancias
	for x in range(qtd):
		for y in range(qtd):
			dist_matrix[x].append(dist_euclid(data.iloc[x,1], data.iloc[x,2], data.iloc[y,1], data.iloc[y,2]))		
		
		#É usado duas vezes pois a primeira represenda o numero do cluster e a partir do segundo os objetos dentro
		clusters[x].append(x)
		clusters[x].append(x)


	#a = ssd.squareform(dist_matrix) 

	#Transforma o list em array
	dist_matrix = np.array([np.array(i) for i in dist_matrix])

	#Iterador necessário para a construção do dendograma
	j = qtd

	#Iterador necessário para gerar as partições resultantes
	k = qtd


	for i in range(qtd-1):


		dist_min, cluster_1, cluster_2 = min_value_matrix(dist_matrix)

		#Insere na matrix de dendrograma o merge realizado
		dend.append([clusters[cluster_1][0], clusters[cluster_2][0], dist_min, len(clusters[cluster_1]) + len(clusters[cluster_2])])
		

		#Realiza a atualização da matrix utilizando a operação abaixo:
		#dist[a,b][c] = mean(dist[a][c] + dist[b][c])
		for x in range(len(dist_matrix[cluster_1])):
			if x != cluster_1:
				dist_matrix[cluster_1][x] = (dist_matrix[cluster_1][x] + dist_matrix[cluster_2][x])/2
				dist_matrix[x][cluster_1] = dist_matrix[cluster_1][x]


		dist_matrix[cluster_1][cluster_2] = 0

		# # old_cluster = data.iloc[cluster_2]['cluster']
		# data.at[cluster_2] = data.iloc[cluster_1]['cluster']

		#Faz o merge dos clusters
		clusters[cluster_1][0] = j
		del clusters[cluster_2][0]
		clusters[cluster_1].extend(clusters[cluster_2])
		#del clusters[cluster_2]
		clusters[cluster_2] = -1

		# for i in range(len(clusters[cluster_1])):
		# 	old_cluster = data.iloc[cluster_2]['cluster']
		# 	if i > 0:
		# 		data.at[clusters[cluster_1][i], 'cluster'] = data.iloc[cluster_1]['cluster']

		# data = data.sort_values(by=['cluster',data.columns[0]])

		# for i in range(len(data['cluster'])):
		# 	if data.iloc[i]['cluster'] >= old_cluster:
		# 		data.at[i, 'cluster'] = data.iloc[i]['cluster'] - 1

		if (k >= k_Min and k <= k_Max):
			save = data[[data.columns[0],'cluster']]
			#Escreve em um arquivo o dataframe, header = False é utilizado para tirar o nome das colunas e o index=False para tirar 
			#os numeros da indexação que fica na primeira coluna.
			save.to_csv("cluster"+ arq +"-k=" + str(k), sep='\t', encoding='utf-8', index = False, header = False)


		k -= 1

		j += 1

		dist_matrix[:, cluster_2] = -1;
		dist_matrix[cluster_2, :] = -1

	#dend = linkage(a, 'average')
	
	dn = dendrogram(dend, labels = list(data.loc[:, data.columns[0]]))
	plt.show()


if __name__ == '__main__': main()