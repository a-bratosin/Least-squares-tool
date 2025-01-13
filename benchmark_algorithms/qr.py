import numpy as np
import numpy.linalg as LA
import timeit

rng = np.random.default_rng(0)
# Algoritmul UTRIS
def Utris(U, b):
    n = len(U)
    x = np.zeros((n,1))
    for i in range(n-1,-1, -1):
        s = b[i]
        for j in range(i+1,n):
            s = s -U[i][j]*x[j]
        x[i] = s/U[i][i]
    return x

# alg de triangulatizare ortogonală cu reflectori
def TORT(A):
    (m,n) = np.shape(A)
    p = min(m-1,n)
    beta = np.zeros(p)
    beta = beta.astype(float)
    # matricea ce stochează toți vectorii u(k)
    # are dimensiunile mxp deoarece înmagazinează p vectori de lungime m, generând un vector pentru fiecare iterație a algoritmului
    # pentru sisteme supradeterminate, U o să aibă dimensiunile (m,n)
    U = np.zeros((m,p))
    U = U.astype(float)

    for k in range(p):
        sigma = np.sign(A[k][k])*LA.norm(A[k:,k])
        
        if(sigma == 0):
            beta[k] = 0
        else:
            U[k][k] = A[k][k] + sigma
            # stocăm coeficienții vectorului uk pentru restul coloanei
            for i in range(k+1,m):
                U[i][k] = A[i][k]
            
            beta[k] = sigma*U[k][k]
            A[k][k] = -sigma

            #
            for i in range(k+1,m):
                A[i][k] = 0
            
            for j in range(k+1,n):
                tau = 0
                
                for i in range(k,m):
                    tau += U[i][k]*A[i][j]
                
                tau = tau / beta[k]
               

                for i in range(k,m):
                    A[i][j] = A[i][j] - tau*U[i][k]
    
    return A, U, beta

def CMMP_supradeterminat(A, b):

    t0 = timeit.default_timer()
    (m,n) = np.shape(A)
    (R,U,beta) = TORT(A)
    
    """
    print("\n\n\n-----------vectorii U obținuți--------------")
    print(U)
    print("\n\n\n\n")
    """
    for k in range(n):
        tau = 0
        for i in range(k,m):
            tau += U[i][k]*b[i]
        tau = tau/beta[k]

        #print(tau)
        for i in range(k,m):
            b[i] = b[i] - tau*U[i][k]
    
    #print(b)

    x = Utris(R[:n,:], b[:n])
    t1 = timeit.default_timer() - t0
    return x,t1

m = 2000
n = 40
A =  rng.integers(1,11, size=(m,n))
A = A.astype(float)
b = rng.integers(10, size=m).astype(float)


print("-------------A-------------")
print(A)

print("\n---------------b----------------")
print(b)


print("---------------sol CMMP-----------")
print(LA.lstsq(A,b)[0])

(x, time) = CMMP_supradeterminat(np.copy(A), np.copy(b))
print("\n---------------sol CMMP cu QR------------")
print(x)

print("Timpul de execuție:")
print(time)






