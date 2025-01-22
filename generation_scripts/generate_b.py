import numpy as np
import numpy.linalg as LA
import joblib
import gc

for k in range(26):
    A_location = "./data/A_matrices"+str(k)+".pkl"
    A_matrices = joblib.load(A_location)

    b_vector = []

    for A_matrix in A_matrices:
        print(np.shape(A_matrix))

        # pentru fiecare matricea A mxn, generez un x0 random, și îl determin pe b[i] ca fiind A*x0
        # astfel x0 este o soluție a sistemului Ax=b
        
        # preiau nr. de coloane ale matricei
        x0 = np.random.rand(np.shape(A_matrix)[1])

        new_vector = A_matrix@x0
        b_vector.append(new_vector)
    
    new_vector_file = "./data/b_vectors"+str(k)+".pkl"

    joblib.dump(b_vector,new_vector_file)