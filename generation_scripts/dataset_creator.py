import numpy as np
import numpy.linalg as LA
import joblib
import gc

# important: scriptul trebuie rulat din root folder! Altfel, nu găsește dosarul data

# generez matricile în fișiere diferite, cu fiecare fișier având 100 de matrice

# argumente: start, stop - fișierele de la care ar trebui să înceapă să genereze
# generate_matrices(0) generează până la matricea cu dimensiunea 100
# generate_matrices(30) generează până la matricea cu dimensiunea 3100
# generate_matrices(5,15) generează de la matricea cu dimensiunea 500 la matricea cu dimensiunea 1600

# fișierul A_matrices1 matricile cu dimensiunea de 1 la 100
# fișierul A_matrices 4 - matricile cu dimensiunile de la 401 la 500
def generate_matrices(size_start = 0, size_end=30):
    for k in range(size_start, size_end+1):

        A_matrix = []

        for i in range(k*100+1, (k+1)*100+1):
            # generează o matrice cu valori aleatorii între -10 și 10 cu dimensiunile (i, 150%*i)
            
            new_matrix = 20*(np.random.rand(i,int(np.floor(i*1.5)))-0.5)
            A_matrix.append(new_matrix)

        # scriem matricea în fișierul data/A_matrices<<k>>.pkl
        data_location = "./data/A_matrices"+str(k)+".pkl"
        joblib.dump(A_matrix, data_location)

        # ca să fiu sigur că nu rămâne în memorie, șterg obiectul și apelez garbage collector-ul
        # aparent dacă îl apelez manual, se poate defragmenta memoria, ceea ce îmbunătățește timpul de execuție
        del A_matrix
        gc.collect()


# pentru matricile de dimensiuni mai mari, stochez valorile doar în incremente de 5
# o să fie ..998,999,1000, apoi 1001,1006,1011,1016,...
def generate_matrices_5_increment(size_start = 11, size_end=30):
    for k in range(size_start, size_end+1):

        A_matrix = []

        for i in range(k*100+1, (k+1)*100+1, 5):
            # generează o matrice cu valori aleatorii între -10 și 10 cu dimensiunile (i, 150%*i)
            
            new_matrix = 20*(np.random.rand(i,int(np.floor(i*1.5)))-0.5)
            A_matrix.append(new_matrix)

        # scriem matricea în fișierul data/A_matrices<<k>>.pkl
        data_location = "./data/A_matrices"+str(k)+".pkl"
        joblib.dump(A_matrix, data_location)

        # ca să fiu sigur că nu rămâne în memorie, șterg obiectul și apelez garbage collector-ul
        # aparent dacă îl apelez manual, se poate defragmenta memoria, ceea ce îmbunătățește timpul de execuție
        del A_matrix
        gc.collect()

generate_matrices_5_increment(21,25)



