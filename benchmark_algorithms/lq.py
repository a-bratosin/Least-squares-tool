# algoritm pentru factorizarea LQ și rezolvarea unui sistem subdeterminat cu ajutorul acesteia
# teoretic poate fi implementată cu QR, cum factorizarea LQ poate fi scrisă în funcție de factorizarea QR a lui A transpus

# A_transpus = Q*R
# A = (Q*R)_transpus = R_transpus*Q_tr = L*Q

# practic, este ineficient să fac o transpunere (de două ori) pentru fiecare matrice calculată
# așa că o calculez direct, aplicând la dreapta matricile Householder, având efectul de a elimina el. matricei pe linie

import numpy as np
import numpy.linalg as LA
import timeit

rng = np.random.default_rng(5)

def Ltris(L, b):
    n = len(L)
    x = np.zeros(n)
    for i in range(n):
        s = b[i]
        for j in range(i):
            s = s - L[i][j]*x[j]
        x[i] = s/L[i][i]
    return x


# algoritmul este adapat din cartea de MN a lui Dumitrescu (LQ - alg 3.6)
# implementarea mea diferă prin faptul că vectorii Householder sunt memorați într-o matrice separată V

def LQ(A_in):
    A = np.copy(A_in)
    (m,n) = np.shape(A)
    s = min(m,n)

    beta = np.zeros(s)
    V = np.zeros((s,n))

    for k in range(s):

        # condiția asta o să fie mereu adevărată pentru matrici late, dar aici implementez varianta generală
        if(k<n):
            sigma = np.sign(A[k][k])*LA.norm(A[k,k:])
            if (sigma!=0): 
                print(sigma)
                print(A[k,k:])
                print(A[k,k:]/sigma)
                V[k,k:] = A[k,k:]/sigma
                V[k][k] = 1 + V[k][k]
                beta[k] = V[k][k] 

                for j in range(k+1,n):
                    A[k][j] = 0

                for i in range(k+1,m):
                    alpha = 0
                    for j in range(k,n):
                        alpha += A[i][j]*V[k][j]
                    alpha = (-1)*alpha/beta[k]

                    for j in range(k,n):
                        A[i][j] += alpha*V[k][j]

                A[k][k] = (-1)*sigma
    #print("din funcție")
    #print(A)
    return A,V,beta

m = 4
n = 6
A =  rng.integers(-10,10, size=(m,n))
A = A.astype(float)
b = rng.integers(-10,10, size=m).astype(float)

A_copy = np.copy(A)

(L,V,beta) = LQ(A_copy)

np.set_printoptions(precision=4)
print("\n\n-----------L--------\n")
print(np.shape(L))
print(L)


print("\n\n-----------A--------\n")
print(np.shape(A_copy))
print(A)

print("\n\n-----------V--------\n")
print(V)


(Q_test, R_test) = LA.qr(np.transpose(A), mode="complete")
print(np.transpose(R_test))