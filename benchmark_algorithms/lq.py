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

# Alg de triangulatizare ortogonală cu reflectori
def TORT(A):
    (m, n) = np.shape(A)
    if m == n:
        p = m
    else:
        p = min(m - 1, n)

    beta = np.zeros(p, dtype=float)
    U = np.zeros((m, p), dtype=float)

    for k in range(p):
        sigma = np.sign(A[k][k]) * LA.norm(A[k:, k])

        if sigma == 0:
            beta[k] = 0
        else:
            U[k][k] = A[k][k] + sigma
            # Stocam coeficienții vectorului uk pentru restul coloanei
            for i in range(k + 1, m):
                U[i][k] = A[i][k]

            beta[k] = sigma * U[k][k]
            A[k][k] = -sigma

            #
            for i in range(k + 1, m):
                A[i][k] = 0

            for j in range(k + 1, n):
                tau = 0

                for i in range(k, m):
                    tau += U[i][k] * A[i][j]

                tau = tau / beta[k]

                for i in range(k, m):
                    A[i][j] = A[i][j] - tau * U[i][k]
        # yield np.copy(A), np.copy(U), np.copy(beta)

    return A, U, beta


# CMMP pentru sistem subdeterminat m < n
def CMMP_underdetermined(A_orig, b_orig):
    A = np.copy(A_orig)
    b = np.copy(b_orig)

    (m, n) = np.shape(A)
    #(R, U, beta) = TORT(np.transpose(A))
    (L,V,beta) = LQ(A)
    
    #R_tr = np.transpose(R)
    #print(R_tr[:, :m])

    y = Ltris(L[:, :m], b)
    #print(y)

    
    
    
    y = np.append(y, np.zeros(n - m).astype(float))
    for k in range(m-1, -1, -1):
        t = V[k][k]
        V[k][k] = beta[k]

        alpha = 0
        for j in range(k,n):
            alpha = alpha + V[k][j]*y[j]
        alpha = (-1)*alpha/beta[k]

        for j in range(k,n):
            y[j] = y[j] + alpha*V[k][j]

    x = y
    return x



m = 4
n = 6
A =  rng.integers(-10,10, size=(m,n))
A = A.astype(float)
b = rng.integers(-10,10, size=m).astype(float)

"""
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

"""


sol_lstsq = LA.lstsq(A,b)[0]

sol_lq = CMMP_underdetermined(A,b)

print("Sol prin lstsq")
print(sol_lstsq)

print("\n\n\nsol prin LQ")
print(sol_lq)