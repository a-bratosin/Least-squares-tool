import numpy as np
import numpy.linalg as LA
import timeit

rng = np.random.default_rng(5)
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

def Ltris(L, b):
    n = len(L)
    x = np.zeros(n)
    for i in range(n):
        s = b[i]
        for j in range(i):
            s = s - L[i][j]*x[j]
        x[i] = s/L[i][i]
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

def CMMP_overdetermined(A, b):

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


def CMMP_underdetermined(A, b):
    A_copy = np.copy(A)
    t0 = timeit.default_timer()
    (m,n) = np.shape(A)
    # pentru a determina soluția în sens CMMP la cazul nedeterminat, trebuie să calculăm factorizarea QR a matricei A transpus
    (R,U,beta) = TORT(np.transpose(A))
    
    """
    print("\n\n\n-----------vectorii U obținuți--------------")
    print(U)
    print("\n\n\n\n")
    """
    # avem sist. RtQtrx=b; facem substituția Qtrx=y și rezolvăm subsistemul Rtr*y=b cu LTRIS 
    # eliminăm coloanele n+1,m ale matricei, care sunt nule
    # rămânem cu un R' inf triunghiular cu dimensiunea nxn
    R_tr = np.transpose(R)
    print(R_tr[:,:m])

    y = Ltris(R_tr[:,:m],b)

    # acum a mai rămas de rezolvat sistemul Qtr*x=y, care este ac. lucru cu Q*x = y, Q fiind simetrică
    # aplicăm Q la dreapta, și obținem x* = Q*y
    # deci aplicăm pe când efectul matricilor Householder vectorului y
    print(y)

   
    y = np.append(y,np.zeros(n-m).astype(float))
    print(y)

    print("\n\n----y real----\n\n")
    print(np.append(LA.inv(R_tr[:,:m])@b, np.zeros(n-m).astype(float)))

    
    print(np.shape(U))
    for k in range(m,-1,-1):
        tau = 0
        for i in range(k,n):
            
            test = U[i][k]
            #print(y[i])
            tau += U[i][k]*y[i]
        tau = tau/beta[k]

        #print(tau)
        for i in range(k,n):
            y[i] = y[i] - tau*U[i][k]
    
    """
    (Q_test,R_test) = np.linalg.qr(np.transpose(A_copy), mode='complete')
    
    print("Q")
    print(Q_test)
    x = Q_test@y
    """

    #print(R[:,:m-1])
    #print(R)
    #print(b[:m-1])

    # după transformări, am înmagazinat în y soluția în sens cmmp a sistemului
    x=y
    t1 = timeit.default_timer() - t0
    return x,t1


m = 4
n = 6
A =  rng.integers(-10,10, size=(m,n))
A = A.astype(float)
b = rng.integers(-10,10, size=m).astype(float)


print("-------------A-------------")
print(A)

print("\n---------------b----------------")
print(b)


print("---------------sol CMMP-----------")
print(LA.lstsq(A,b)[0])

(x, time) = CMMP_underdetermined(np.copy(A), np.copy(b))
print("\n---------------sol CMMP cu QR------------")
print(x)

print("Timpul de execuție:")
print(time)






