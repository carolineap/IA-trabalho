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
from scipy.spatial.distance import squareform, pdist
from scipy.spatial import distance_matrix

#dataframe
data = None
#Quantidade de clusters
k_Min = 0
k_Max = 0

#Acha a distância média entre os objetos do cluster
def min_value_matrix(matrix) :
	
	aux = np.tril(matrix, -1) #pega apenas o triangulo inferior da matriz
	index = np.where( aux==np.min(aux[np.nonzero(aux)])) #indices do menor valor da matriz (exceto zero)
	#print(index)

	row = index[0][0]
	column = index[1][0]

	dist_min = matrix[row][column]

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
	data['cluster'] = range(qtd)

	
	#Lista usada para armazenar o numero do cluster e a quais objetos estão inclusos no cluster
	clusters = [[] for _ in range(qtd)]

	#Lista usado para montar o histograma
	dend = []

	#Insere na matriz os valores das distancias
	for x in range(qtd):
		clusters[x].append(x)
		clusters[x].append(x)

	#dist_matrix = squareform(pdist(data.iloc[:, 1:]))
	dist_matrix = distance_matrix(data.iloc[:, 1:], data.iloc[:, 1:])


	#a = ssd.squareform(dist_matrix) 

	#Iterador necessário para a construção do dendograma
	j = qtd
	
	#Por segurança
	if k_Max == qtd:
		save = data[[data.columns[0], 'cluster']]
		#Escreve em um arquivo o dataframe, header = False é utilizado para tirar o nome das colunas e o index=False para tirar 
		#os numeros da indexação que fica na primeira coluna.
		save.to_csv("cluster-k=9" + "-" + arq, sep='\t', encoding='utf-8', index = False, header = False)

	#Iterador necessário para gerar as partições resultantes
	k = qtd - 1



	for i in range(qtd-1):


		dist_min, cluster_1, cluster_2 = min_value_matrix(dist_matrix)

		print("Iteration number " + str(i))	


		#Insere na matrix de dendrograma o merge realizado
		dend.append([clusters[cluster_1][0], clusters[cluster_2][0], dist_min, len(clusters[cluster_1]) + len(clusters[cluster_2]) - 2])
		
		

		data['cluster'] = data['cluster'].replace(clusters[cluster_1][0], j)
		data['cluster'] = data['cluster'].replace(clusters[cluster_2][0], j)



		#print(data['cluster'])

		if (k >= k_Min and k <= k_Max):
			
			save = data
			
			print(save)


			save = save.sort_values(by=['cluster', save.columns[0]])
			save['cluster'] = pd.factorize(save['cluster'])[0]
			#Escreve em um arquivo o dataframe, header = False é utilizado para tirar o nome das colunas e o index=False para tirar 
			#os numeros da indexação que fica na primeira coluna.
			save[[save.columns[0], 'cluster']].to_csv("cluster-k=" + str(k) + "-" + arq, sep='\t', encoding='utf-8', index = False, header = False)


			#Define um color map a ser utilizado
			#obs: pode coloar o que acharem melhor, eu escolhi esse por ser diferente o 0 do 1.
			cmap = plt.cm.get_cmap('Set1', k)

			print(save)

			#data.plot(kind = "scatter", x = 1, y=2, color =cmap(data['cluster']))
			fig, ax = plt.subplots()
			for key, group in save.groupby('cluster'):
				print(key)
				ax.scatter(group.iloc[:,1], group.iloc[:,2], label=key, color = cmap(group['cluster']))


			#ax.scatter(data.iloc[:,1],data.iloc[:,2], color = cmap(data['cluster']))
			#for i in range(data['cluster']) :
			#	ax.plot(0, ,marker="X", color = cmap(k), label='Pos.Centroide' + str(k) )
			ax.legend()


			plt.show()



		#Realiza a atualização da matrix utilizando a operação abaixo:
		#dist[a,b][c] = mean(dist[a][c] + dist[b][c])
		for x in range(len(dist_matrix[cluster_1])):
			if x != cluster_1:
				dist_matrix[cluster_1][x] = (dist_matrix[cluster_1][x] + dist_matrix[cluster_2][x])/2
				dist_matrix[x][cluster_1] = dist_matrix[cluster_1][x]



		#Faz o merge dos clusters
		clusters[cluster_1][0] = j
		del clusters[cluster_2][0]
		clusters[cluster_1].extend(clusters[cluster_2])
		del clusters[cluster_2]
		

		k -= 1

		j += 1

		dist_matrix = np.delete(dist_matrix,cluster_2, 0)
		dist_matrix = np.delete(dist_matrix,cluster_2, 1)

		


	#dend = linkage(a, 'average')
	print(dend)
	dn = dendrogram(dend, labels = list(data.loc[:, data.columns[0]]))
	plt.show()


if __name__ == '__main__': main()