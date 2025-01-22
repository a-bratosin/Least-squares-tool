import joblib
import timeit
import numpy.linalg as LA
import numpy as np

# script care face benchmark pentru funcția nativă de least squares
# mă folosesc de doi vectori: exec_times[] care stochează timpii de execuție, și row_sizes[] care stochează nr de linii pentru acel timp de execuție
# aceste două structuri vor fi stocate în dosarul benchmark
exec_times = []
row_sizes = []
for k in range(26):
    # aici selectează ./data deoarece scriptul este executat din directorul root al proiectului
    A_location = "./data/A_matrices"+str(k)+".pkl"
    b_location = "./data/b_vectors"+str(k)+".pkl"

    A_matrices = joblib.load(A_location)
    b_vectors = joblib.load(b_location)
    
    for i in range(len(A_matrices)):
        row_sizes.append(np.shape(A_matrices[i])[0])

        t0 = timeit.default_timer()
        sol = LA.lstsq(A_matrices[i],b_vectors[i],rcond=-1)[0]
        exec_times.append( timeit.default_timer() - t0)

    print("file #",k," done")
joblib.dump(row_sizes, "row_backup.pkl")
joblib.dump(exec_times, "time_backup.pkl")
joblib.dump(row_sizes, "./benchmark/lstsq/row_sizes.pkl")
joblib.dump(exec_times, "./benchmark/lstsq/times.pkl")


