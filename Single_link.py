'''
	O algoritmo ao invez de separar os dataframes para representar clusters diferentes, ele cria uma nova columa 
	chamada 'cluster' sendo que cada numero representa um cluster diferente.

https://stackoverflow.com/questions/37712465/what-is-the-meaning-of-the-return-values-of-the-scipy-cluster-hierarchy-linkage
https://www.kaggle.com/barelydedicated/hierarchical-clustering-single-link
http://dcm.ffclrp.usp.br/~augusto/teaching/ami/AM-I-Clustering.pdf

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
from scipy.cluster.hierarchy import dendrogram

#dataframe
data = None
#Quantidade de clusters
k_Min = 0
k_Max = 0


#Acha a menor valor maior que zero de uma matrix 
def min_value_matrix(matrix) :
	dist_min = 10000
	row = 0
	column = 0

	for x in range(len(matrix)) :
		for y in range(len(matrix)) :
			if dist_min > matrix[x][y] and matrix[x][y] > 0:
				dist_min = matrix[x][y]
				row = x
				column = y
	return(dist_min,row,column)	

def dist_eclid(x1,y1,x2,y2) :
	return (((x1 - x2) ** 2) + ((y1 - y2) ** 2 )) ** (1/2)

def print_matrix(matrix) :
	for a in matrix :
		print(a)

def main() :

	global data,k_Min,k_Max

	entrada = input("Insira o nome do arquivo, numero de clusters e o numero de interações separados com um espaco:\n")

	#Recebe a entrada na ordem : Nome do arquivo, NUmero de Clusters e Numero de interações
	arq,k_Min,k_Max = entrada.split(" ")

	#Converte as variaves de str para int
	k_Max = int(k_Max)
	k_Min = int(k_Min)

	#Lê o arquivo dado e cria uma dataframe com ele
	data = pd.read_csv('datasets/' + arq, delimiter = "\t")
	
	#Insere uma nova coluna chamado cluster com o valor = 0
	data['cluster'] = 0
	#Pega a quantidade de objetos existentes
	qtd = data.shape[0]
	#Matrix usada para armazenar as distancias de cada cluster
	dist_matrix = [ [] for _ in range(qtd)]
	#Lista usada para armazenar o numero do cluster e a quais objetos estão inclusos no cluster
	clusters = [[] for _ in range(qtd)]
	#Lista usado para montar o histograma
	dend = []

	#Insere na matrix os valores das distancias
	for x in range(qtd) :
		for y in range(qtd) :
			dist_matrix[x].append(dist_eclid(data.iloc[x,1],data.iloc[x,2],data.iloc[y,1],data.iloc[y,2]))		
		#É usado duas vezes pois a primeira represenda o numero do cluster e a partir do segundo os objetos dentro
		clusters[x].append(x)
		clusters[x].append(x)

	#print(dist_matrix)
	#print(qtd)


	j = qtd

	#Transforma o list em array
	dist_matrix = np.array([np.array(i) for i in dist_matrix])
	
	for i in range(qtd-1) :
		#Procura a menor distancia na matrix de distancia
		dist_min,cluster_1,cluster_2 = min_value_matrix(dist_matrix)

		#Insere na matrix de dendrograma o merge realizado
		dend.append([clusters[cluster_1][0],clusters[cluster_2][0],dist_min,len(clusters[cluster_1]) + len(clusters[cluster_2])-2])
		
	#	print('Dendogram :')
	#	print_matrix(dend)

		#Realiza a atualização da matrix utilizando a operação abaixo:
		#dist[a,b][c] = min(dist[a][c],dist[a][b])
		for x in range(len(dist_matrix[cluster_1])) :
			if dist_matrix[cluster_1][x] > dist_matrix[cluster_2][x] :
				dist_matrix[cluster_1][x] = dist_matrix[cluster_2][x]

		#Faz o merge dos clusters
		clusters[cluster_1][0] = j
		del clusters[cluster_2][0]
		clusters[cluster_1].extend(clusters[cluster_2])
		del clusters[cluster_2]
	#	print('Clusters :')
	#	print(clusters)


		j+=1

		dist_matrix = np.delete(dist_matrix,cluster_2,0)
		dist_matrix = np.delete(dist_matrix,cluster_2,1)

	#	print('Matriz de distancia')
	#	print_matrix(dist_matrix)

	#	print(str(cluster_1) + ' ' + str(cluster_2))
		print(x)
	print(clusters)
	dn = dendrogram(dend,labels = list(data.loc[:,data.columns[0]]))
	plt.show()

	''' ---Implementação ineficiente do algoritmo ------------------------------------------------------------------------
	#Obtem a quantidade de objetos 
	v = data.shape[0]
	tam_index = v
	clust = data.iloc[:,3]
	qtd_index = v

	for i in range(v) :
		dist_min = 100000
		cluster_1 = 0
		cluster_2 = 0
		for x in range(v) :
			for y in range(x+1,v):
				new_dist = dist_eclid(data.iloc[x,1],data.iloc[x,2],data.iloc[y,1],data.iloc[y,2])
				#print(data.iloc[y,3])
				if new_dist < dist_min and data.iloc[x,3] != data.iloc[y,3]:
					print(str(x) + ' -- ' +  str(y))
					dist_min = new_dist
					cluster_1 = x
					cluster_2 = y
		old_cluster = data.iloc[cluster_2,3]
		new_cluster = data.iloc[cluster_1,3]
		for x in range(v) :
			if data.iloc[x,3] == old_cluster :
				data.iloc[x,3] = new_cluster
		
		qtd_index+=1
		print(str(cluster_1) + ' ' + str(cluster_2))
		print(data)
	print(clust)
	'''




if __name__ == '__main__': main()