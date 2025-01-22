import numpy as np
import numpy.linalg as LA
import joblib

# script that generates the least squares solution for every Ax=b system

for k in range(26):
    A_location = "./data/A_matrices"+str(k)+".pkl"
    b_location = "./data/b_vectors"+str(k)+".pkl"

    A_matrices = joblib.load(A_location)
    b_vectors = joblib.load(b_location)

    x_solutions = []

    for i in range(len(A_matrices)):

        x_solution = LA.lstsq(A_matrices[i],b_vectors[i],rcond=-1)[0]
        x_solutions.append(x_solution)
    
    solutions_location = "./data/x_vectors"+str(k)+".pkl"
    joblib.dump(x_solutions, solutions_location)
    print(k)

