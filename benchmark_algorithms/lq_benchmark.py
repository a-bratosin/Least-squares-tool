import joblib
import timeit
import numpy.linalg as LA
import numpy as np
import kaczmarz
import lq
# script care face benchmark pentru funcția nativă de least squares
# mă folosesc de doi vectori: exec_times[] care stochează timpii de execuție, și row_sizes[] care stochează nr de linii pentru acel timp de execuție
# aceste două structuri vor fi stocate în dosarul benchmark
exec_times = []
row_sizes = []

tolerance = 1e-7
for k in range(8):
    # aici selectează ./data deoarece scriptul este executat din directorul root al proiectului
    A_location = "./data/A_matrices"+str(k)+".pkl"
    b_location = "./data/b_vectors"+str(k)+".pkl"
    x_location = "./data/x_vectors"+str(k)+".pkl"
    
    A_matrices = joblib.load(A_location)
    b_vectors = joblib.load(b_location)
    x_vectors = joblib.load(x_location)

    for i in range(len(A_matrices)):
        if(np.shape(A_matrices[i])[0]%5!=1): continue
        row_sizes.append(np.shape(A_matrices[i])[0])

        (ans, time) = lq.CMMP_underdetermined(A_matrices[i],b_vectors[i])
        exec_times.append(time)
        print("matrix ",i, " done")


    print("file #",k," done")
joblib.dump(row_sizes, "lq_row_backup0-7.pkl")
joblib.dump(exec_times, "lq_time_backup0-7.pkl")
joblib.dump(row_sizes, "./benchmark_algorithms/benchmark/kaczmarz/lq_row_sizes0-7.pkl")
joblib.dump(exec_times, "./benchmark_algorithms/benchmark/kaczmarz/lq_times0-7.pkl")

