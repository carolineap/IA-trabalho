'''
	O algoritmo ao invez de separar os dataframes para representar clusters diferentes, ele cria uma nova columa 
	chamada 'cluster' sendo que cada número representa um cluster diferente.


'''
import time
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

#dataframe
data = None
#Quantidade de clusters
k_num = 0
#Quantidade de interações
num_int = 0

#Calcula o centroide de cada cluster gerado
def calc_centroide(cluster) :
	
	x = cluster.sum(axis=0)
	tam = cluster.shape[0]
	centroide = [x.get(1)/tam, x.get(2)/tam]

	return centroide

def dist_eclid(x1,y1,x2,y2) :
	return (((x1 - x2) ** 2) + ((y1 - y2) ** 2 )) ** (1/2)

def associa_cluster(lista_centroide, x):
	global data
	#menor distancia
	min_dist = 100000
	#cluster com a menor distancia
	n_cluster = 0
	for k in range(k_num):

		#Calculo da distancia Euclidiana
		new_dist = dist_eclid(data.iloc[x, 1], data.iloc[x, 2], lista_centroide[k][0], lista_centroide[k][1])
		
		if min_dist > new_dist:
			min_dist = new_dist
			n_cluster = k
		
	return n_cluster

def main() :

	start_time = time.time()

	global data,k_num,num_int

	#Lista com os centroides de cada cluster
	lista_centroide = [ [] for _ in range(k_num)]

	entrada = input("Insira o nome do arquivo, número de clusters e o número de iterações separados com um espaco:\n")

	#Recebe a entrada na ordem : Nome do arquivo, Número de Clusters e Número de iterações
	arq, k_num, num_int = entrada.split(" ")

	#Converte as variaves de str para int
	k_num = int(k_num)
	num_int = int(num_int)

	#Lê o arquivo dado e cria uma dataframe com ele
	data = pd.read_csv('datasets/' + arq, delimiter = "\t")

	arq = arq.replace(".txt", "")
	
	#Insere uma nova coluna chamado cluster com o valor = 0
	data['cluster'] = 0
	
	#Coloca os dataframe em ordem aleatoria
	r = data.sample(frac = 1)

	#Obtém a quantidade de objetos em cada cluster
	v = data.shape[0]/k_num

	for i in range(k_num) :
		#Modifica os valores da coluna cluster.
		r.iloc[round(v*i) : round(v*(i+1)) ,3] = i

	#Ordena o dataframe
	data = r.sort_index(axis=0)

	#print("Clusters aleatórios criados")
	#print(data)
	
	#Calcula os centroides dos clusters
	for k in range(k_num) :
		cluster = data.loc[data['cluster'] == k] 
		lista_centroide.append(calc_centroide(cluster))
		
	for i in range(num_int):

		print("Iteration " + str(i))

		#Associação dos objetos ao cluster com o centroide mais proximo
		for j in range(data.shape[0]) :
			#Substitiu o numero do cluster atual com o numero do novo cluster		
			data.iat[j, 3] = associa_cluster(lista_centroide, j)

		flag = False


		#print(data)

		#Calcula os novos centroides
		for k in range(k_num) :
			
			cluster = data.loc[data['cluster'] == k] 
			
			if cluster.empty == True:
				lista_centroide[k] = [0, 0]
			else:	
				new_centroid = calc_centroide(cluster)
				if (lista_centroide[k] != new_centroid): 
					flag = True
					lista_centroide[k] = new_centroid
 
		if (flag == False): #caso nenhum centroide tenha mudado
			break
		
		#print("Cluster")
		#print(data)

	#Define um color map a ser utilizado
	cmap = plt.get_cmap('gist_rainbow')			
	
	#gera k cores diferentes
	NUM_COLORS = k_num	

	#gera gráfico
	fig, ax = plt.subplots()
	ax.set_prop_cycle('color', [cmap(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

	for key,group in data.groupby('cluster'):
		ax.scatter(group.iloc[:,1],group.iloc[:,2], label=key)
	
	#ax.scatter(data.iloc[:,1],data.iloc[:,2], color = cmap(data['cluster']))
	for k in range(k_num) :
		ax.plot(lista_centroide[k][0],lista_centroide[k][1], marker="X", markerfacecolor='white', label='Pos.Centroide' + str(k) )
	

	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

	#Ordena por cluster
	#data = data.sort_values(by=['cluster', data.columns[0]])	

	save = data[[data.columns[0], 'cluster']]
	
	#Escreve em um arquivo o dataframe, header = False é utilizado para tirar o nome das colunas e o index=False para tirar 
	#os numeros da indexação que fica na primeira coluna.
	save.to_csv("results/" + arq + "/kmeans-" + arq + "-k=" + str(k_num) + ".clu", sep='\t', encoding='utf-8', index = False, header = False)
	
	#exibe gráfico. programa para de executar. para continuar, basta fechar a janela de exibição do gráfico
	#plt.show()

	#Caso queria salvar o gráfico
	plt.savefig("results/" + arq + "/plots/kmeans-" + arq + "-k=" + str(k_num) + ".png")
		
	print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__': main()
