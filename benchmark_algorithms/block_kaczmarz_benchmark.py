import joblib
import timeit
import numpy.linalg as LA
import numpy as np
import block_kaczmarz
# script care face benchmark pentru funcția nativă de least squares
# mă folosesc de doi vectori: exec_times[] care stochează timpii de execuție, și row_sizes[] care stochează nr de linii pentru acel timp de execuție
# aceste două structuri vor fi stocate în dosarul benchmark
exec_times = []
row_sizes = []

tolerance = 1e-7
try:
    for k in range(15,26):

        # aici selectează ./data deoarece scriptul este executat din directorul root al proiectului
        A_location = "./data/A_matrices"+str(k)+".pkl"
        b_location = "./data/b_vectors"+str(k)+".pkl"
        x_location = "./data/x_vectors"+str(k)+".pkl"
        
        A_matrices = joblib.load(A_location)
        b_vectors = joblib.load(b_location)
        x_vectors = joblib.load(x_location)

        for i in range(len(A_matrices)):
            if(np.shape(A_matrices[i])[0]<10): continue
            if(np.shape(A_matrices[i])[0]%100!=1): continue
            #print("matrix ",i)
            row_sizes.append(np.shape(A_matrices[i])[0])

            (ans, time) = block_kaczmarz.RBK(A_matrices[i],b_vectors[i],  x_vectors[i], tolerance)
            exec_times.append(time)
            print("Matrix #",i," done")

        print("file #",k," done")

    joblib.dump(row_sizes, "rbk_row_backup.pkl")
    joblib.dump(exec_times, "rbk_time_backup.pkl")

except:
    joblib.dump(row_sizes, "rbk_row_backup_err.pkl")
    joblib.dump(exec_times, "rbk_time_backup_err.pkl")


#joblib.dump(row_sizes, "./benchmark/kaczmarz/row_sizes.pkl")
#joblib.dump(exec_times, "./benchmark/kaczmarz/times.pkl")

