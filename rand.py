from sklearn.metrics.cluster import adjusted_rand_score
import pandas as pd

def ari(real_partition, method, kmin, kmax, file):

	try:
		rand_file = open('results/' + method + '/' + file + '-ari.csv', 'w')
		rand_file.write('Número de clusters \t ARI\n')
		for i in range(kmin, kmax+1):
			data = pd.read_csv('results/' + method + '/' + file + '-k=' + str(i) + '.clu', delimiter = '\t')
			partition = data.iloc[:, 1].tolist()
			ari = adjusted_rand_score(partition, real_partition)
			rand_file.write(str(i) + '\t' + str(ari) + '\n')
		rand_file.close() 
		return 1
	except:
		return 0
 

def main():

	op = input("Digite a opção que corresponde ao arquivo desejado:\n")

	op = int(op)

	if op == 1:
		data = pd.read_csv('datasets/c2ds1-2spReal.clu', delimiter = "\t")
		real_partition = data.iloc[:, 1].tolist()
		ari(real_partition, 'single', 2, 5, 'c2ds1-2sp')
		ari(real_partition, 'average', 2, 5, 'c2ds1-2sp')
		#ari(real_partition, 'kmeans', 2, 5, 'c2ds1-2sp')
	elif op == 2:
		data = pd.read_csv('datasets/c2ds3-2gReal.clu', delimiter = "\t")
		real_partition = data.iloc[:, 1].tolist()
		ari(real_partition, 'single', 2, 5, 'c2ds3-2g')
		ari(real_partition, 'average', 2, 5, 'c2ds3-2g')
		#ari(real_partition, 'kmeans', 2, 5, 'c2ds3-2g')
	elif op == 3:
		data = pd.read_csv('datasets/monkeyReal1.clu', delimiter = "\t")
		real_partition = data.iloc[:, 1].tolist()
		ari(real_partition, 'single', 5, 12, 'monkey')
		ari(real_partition, 'average', 5, 12, 'monkey')
		#ari(real_partition, 'kmeans', 5, 12, 'monkey')

if __name__ == '__main__': main()