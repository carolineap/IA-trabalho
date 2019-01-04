'''
	O algoritmo ao invez de separar os dataframes para representar clusters diferentes, ele cria uma nova columa 
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

def associa_cluster(lista_centroide,x) :
	global data
	#menor distancia
	min_dist = 100000
	#cluster com a menor distancia
	n_cluster = 0
	for k in range(k_num) :
		#Calculo da distancia Euclidiana
		new_dist = dist_eclid(data.iloc[x,1],data.iloc[x,2],lista_centroide[k][0],lista_centroide[k][1])
		if min_dist > new_dist:
			min_dist = new_dist
			n_cluster = k
		print(min_dist)
	return n_cluster

def main() :

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
	
	#Insere uma nova coluna chamado cluster com o valor = 0
	data['cluster'] = 0

	#Gera centroides aleatorios(Implementação de quando achava que gerava aleatoriamente o centroide primeiro em vez do cluster)
	#for i in range(k_num) :
	#	centroide = [random.uniform(data.iloc[:,1].min(),data.iloc[:,1].max()), random.uniform(data.iloc[:,2].min(),data.iloc[:,2].max())]
	#	lista_centroide[i] = centroide
		#print(centroide)	
	
	#Coloca os dataframe em ordem aleatoria
	r = data.sample(frac = 1)

	#Obtém a quantidade de objetos em cada cluster
	v = data.shape[0]/k_num

	for i in range(k_num) :
		#Modifica os valores da coluna cluster.
		r.iloc[round(v*i) : round(v*(i+1)) ,3] = i

	#Ordena o dataframe
	data = r.sort_index(axis=0)

	print("Clusters aleatórios criados")
	print(data)
	
	#Calcula os centroides dos clusters
	for k in range(k_num) :
		cluster = data.loc[data['cluster'] == k] 
		print(cluster)
		lista_centroide.append(calc_centroide(cluster))

	#print(centroide)
	print("Lista de Centoides")
	print(lista_centroide)
		
	for _ in range(num_int) :
		#Associação dos objetos ao cluster com o centroide mais proximo
		for j in range(data.shape[0]) :
			#Substitiu o numero do cluster atual com o numero do novo cluster		
			data.iat[j,3] = associa_cluster(lista_centroide,j)

		#Calcula os novos centroides
		for k in range(k_num) :
			cluster = data.loc[data['cluster'] == k] 
			print(cluster)
			lista_centroide[k] = calc_centroide(cluster)
		
		print("Cluster")
		print(data)

	#Define um color map a ser utilizado
	#obs: pode coloar o que acharem melhor, eu escolhi esse por ser diferente o 0 do 1.
	cmap = plt.cm.get_cmap('Set1', k_num)

	#Mostra o grafico, cada cluster possui uma cor diferente
	plt.ion()
	#data.plot(kind = "scatter", x = 1, y=2, color =cmap(data['cluster']))
	fig,ax = plt.subplots()
	for key,group in data.groupby('cluster'):
		ax.scatter(group.iloc[:,1],group.iloc[:,2], label=key, color = cmap(group['cluster']))
	#ax.scatter(data.iloc[:,1],data.iloc[:,2], color = cmap(data['cluster']))
	for k in range(k_num) :
		ax.plot(lista_centroide[k][0],lista_centroide[k][1],marker="X", color = cmap(k), label='Pos.Centroide' + str(k) )
	ax.legend()

	#Ordena por cluster
	data = data.sort_values(by=['cluster',data.columns[0]])

	save = data[[data.columns[0],'cluster']]
	#Escreve em um arquivo o dataframe, header = False é utilizado para tirar o nome das colunas e o index=False para tirar 
	#os numeros da indexação que fica na primeira coluna.
	save.to_csv("cluster"+arq, sep='\t', encoding='utf-8', index = False, header = False)
	
	#Utilizado apenas para não terminar a execução.
	input("Press enter to continue")

if __name__ == '__main__': main()
