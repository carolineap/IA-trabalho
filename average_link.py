'''
	O algoritmo ao invez de separar os dataframes para representar clusters diferentes, ele cria uma nova coluna 
	chamada 'cluster' sendo que cada número representa um cluster diferente.

'''
import time
import pandas as pd
import numpy as np
import math
import random
#printar no terminal do linux
import matplotlib.pyplot as plt
import scipy as sp  # SciPy (signal and image processing library)
import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
from pylab import *              # Matplotlib's pylab interface
from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.spatial.distance as ssd
from scipy.spatial.distance import squareform, pdist

#dataframe
data = None
#Quantidade de clusters
k_Min = 0
k_Max = 0

#Acha a distância média entre os objetos do cluster
def min_value_matrix(matrix) :
	
	aux = np.tril(matrix, -1) #pega apenas o triângulo inferior da matriz
	index = np.where(aux == np.min(aux[np.nonzero(aux)])) #indices do menor valor da matriz (exceto zero)
	#print(index)

	row = index[0][0]
	column = index[1][0]

	dist_min = matrix[row][column]

	return(dist_min, row, column)	
				
def print_matrix(matrix) :
	for a in matrix:
		print(a)

def main() :

	start_time = time.time()

	global data, k_Min, k_Max

	entrada = input("Insira o nome do arquivo, e o intervalo do número de clustes (k min e k max) separados por um espaço:\n")

	#Recebe a entrada na ordem : Nome do arquivo, k-min e k-max
	arq, k_Min, k_Max = entrada.split(" ")

	#Converte as variaves de str para int
	k_Max = int(k_Max)
	k_Min = int(k_Min)

	#Lê o arquivo dado e cria uma dataframe com ele
	data = pd.read_csv('datasets/' + arq, delimiter = "\t")

	arq = arq.replace('.txt', '')

	#Pega a quantidade de objetos existentes
	qtd = data.shape[0]

	#Lista usada para armazenar o numero do cluster e a quais objetos estão inclusos no cluster
	clusters = [[] for _ in range(qtd)]

	#Lista usado para montar o histograma
	dend = []

	#Insere na matriz os valores das distancias
	for x in range(qtd):
		clusters[x].append(x)
		clusters[x].append(x)

	#Cria matriz de distâncias euclidianas
	dist_matrix = squareform(pdist(data.iloc[:, 1:], 'euclidean'))

	#Insere uma nova coluna chamado cluster com o valor = 0 - quant
	data['cluster'] = range(qtd)

	#Iterador necessário para a construção do dendograma
	j = qtd
	
	#Iterador necessário para gerar as partições resultantes
	k = qtd - 1

	for i in range(qtd-1):

		dist_min, cluster_1, cluster_2 = min_value_matrix(dist_matrix)

		print("Iteration number " + str(i))	


		#Insere na matrix de dendrograma o merge realizado
		dend.append([clusters[cluster_1][0], clusters[cluster_2][0], dist_min, len(clusters[cluster_1]) + len(clusters[cluster_2]) - 2])
		
		data['cluster'] = data['cluster'].replace(clusters[cluster_1][0], j)
		data['cluster'] = data['cluster'].replace(clusters[cluster_2][0], j)

		if (k >= k_Min and k <= k_Max):
			
			save = data.copy()			

			save['cluster'] = pd.factorize(save['cluster'])[0] #transforma o número de clusters entre 0 e k - 1

			#Escreve em um arquivo o dataframe, header = False é utilizado para tirar o nome das colunas e o index=False para tirar 
			#os numeros da indexação que fica na primeira coluna.
			save[[save.columns[0], 'cluster']].to_csv("results/" + arq + "/avg-" + arq + "-k=" + str(k) + ".clu", sep='\t', encoding='utf-8', index = False, header = False)

			#Define um color map a ser utilizado
			cmap = plt.get_cmap('gist_rainbow')			
			
			#gera k cores diferentes
			NUM_COLORS = k	

			#gera gráfico
			fig, ax = plt.subplots()
			ax.set_prop_cycle('color', [cmap(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
			for key, group in save.groupby('cluster'):
				ax.scatter(group.iloc[:,1], group.iloc[:,2], label=key)
			
			#insere legendas	
			box = ax.get_position()
			ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
			ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

			#exibe gráfico. programa para de executar. para continuar, basta fechar a janela de exibição do gráfico
			#plt.show()

			#Caso queria salvar o gráfico
			plt.savefig("results/" + arq + "/plots/avg-" + arq + "-k=" + str(k) + ".png")
		
		#Realiza a atualização da matrix utilizando a operação abaixo:
		#dist[a,b][c] = (dist[a][c] * size(a) + dist[b][c] * size(b))/(size(a) + size(b))
		for x in range(len(dist_matrix[cluster_1])):
			if x != cluster_1:
				dist_matrix[cluster_1][x] = (dist_matrix[cluster_1][x] * (len(clusters[cluster_1]) - 1) + dist_matrix[cluster_2][x] * (len(clusters[cluster_2]) - 1)) /(len(clusters[cluster_1]) + len(clusters[cluster_2]) - 2)
				dist_matrix[x][cluster_1] = dist_matrix[cluster_1][x]


		#Faz o merge dos clusters
		clusters[cluster_1][0] = j
		del clusters[cluster_2][0]
		clusters[cluster_1].extend(clusters[cluster_2])
		del clusters[cluster_2]
		
		k -= 1
		j += 1

		#retira linha e coluna que não são mais necessárias
		dist_matrix = np.delete(dist_matrix,cluster_2, 0)
		dist_matrix = np.delete(dist_matrix,cluster_2, 1)

	#Gera e exibe dendograma	
	#dn = dendrogram(dend, labels = list(data.loc[:, data.columns[0]]))
	#plt.show()
	print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__': main()