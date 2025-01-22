
import numpy as np
import numpy.linalg as LA
import timeit

# în cadrul acestor doi algoritmi, scopul este de a obține timpul în care algoritmul Kaczmarz (fie cu selecție ciclică, fie cu selecție aleatoare) găsește soluția problemei CMMP
# fiind un algoritm iterativ, soluția dată nu este exactă
# așadar, alg. Kaczmarz rulează până când eroarea dintre soluția Kaczmarz și cea reală se află sub o toleranță dată

# Input: matricea A, vectorul b, toleranța tol, și un nr maxim de iterații (opțional)
# Output: Pentru matrice nepătratice, soluția în sens CMMP a sistemului Ax=b, nr de iterații, și timpul de rulare
def alg_kaczmarz_cyclic(A, b, lsq_sol,  tol, maxiter=-1):
    # algoritmul converge la soluția de normă minimă atunci când vectorul inițial este ales 0
    # sursă: https://arxiv.org/pdf/1902.09946
    (m,n) = np.shape(A)
    x = np.zeros(n)
    x = x.astype(float)
    
    k = 0 # nr de iterații
    e = 1 # eroarea

    # timpul îl măsurăm de la începerea buclei
    t0 = timeit.default_timer()
    while(e>tol):
        # verificarea asta este făcută dacă s-a optat pt un număr maxim de iterații
        if(maxiter != -1):
            if(k>maxiter):
                print("S-a atins numărul maxim de iterații!")
                t1 = timeit.timeit()-t0
                return x,k,t1
        
        # aici fac cu iterare ciclică asupra liniilor matricei
        i = k%m
        #print(i)

        
        #print(A[i,:])
        #print("prod scalar")
        #print((A[i,:]@x))
        ai = A[i,:]
        y = x + (b[i] - ai@x )/(LA.norm(ai)**2) * ai   
        #print(y)
        
        x=y
        # criteriul de oprire constă în compararea reziduului r=Ax-b cu toleranța dată
        # depinzând de valorile lui A, respectiv b, e posibil ca această toleranță să fie aleasă prea mică pe cazul nepătratic (i.e. reziduul minim Ax-b să fie mai mare decât toleranța; în cazul ăsta, programul nu se oprește decât at. când atinge nr. maxim de iterații)
        e = LA.norm(np.abs(1-np.abs(lsq_sol@x)/(LA.norm(lsq_sol)*LA.norm(x))))
        k = k+1
    
    # înmulțesc cu 10^3 pentru a obține timpul în milisecunde
    t1 = (timeit.default_timer()-t0)*1000
    return x,t1

# calculează distribuția de probabilitate pentru alegerea unei linii din alg. Kaczmarz cu selecție aleatorie
# returnează pentru o matrice dată un vector al probabilităților p(i), unde p(i) este raportul dintre norma vectorului liniei i a mat. A la pătrat și norma Frobenius a mat. A la pătrat
def calculate_distribution(A):
    line_number = np.shape(A)[0]
    p = np.zeros(line_number)

    # pentru matricea A, metoda LA.norm(A) returnează norma Frobenius a matricei
    # calculez de dinainte pentru a nu o recalcula pentru fiecare iterație a buclei
    matrix_norm = LA.norm(A)**2
    for i in range(line_number):
        p[i] = LA.norm(A[i,:])**2/matrix_norm

    return p

def alg_kaczmarz_random(A,b,tol, lsq_sol, maxiter=-1):
    (m,n) = np.shape(A)
    x = np.zeros(n)
    x = x.astype(float)

    k = 0 # nr de iterații
    e = 1 # eroarea

    # timpul îl măsurăm aici înaintea calculării probabilităților
    t0 = timeit.default_timer()
    
    # obținem mai întâi distribuția de probabilitate pentru liniile lui A
    prob = calculate_distribution(np.copy(A))

    
    while(e>tol):
        # verificarea asta este făcută dacă s-a optat pt un număr maxim de iterații
        if(maxiter != -1):
            if(k>maxiter):
                print("S-a atins numărul maxim de iterații!")
                t1 = timeit.timeit()-t0
                return x,k,t1
        
        # iterare aleatorie
        i = np.random.choice(m, p = prob)
        #print(i)
        
        #print(A[i,:])
        #print("prod scalar")
        #print((A[i,:]@x))
        ai = A[i,:]
        y = x + (b[i] - ai@x )/(LA.norm(ai)**2) * ai   
        #print(y)
        
        x=y
        # criteriul de oprire constă în compararea reziduului r=Ax-b cu toleranța dată
        # depinzând de valorile lui A, respectiv b, e posibil ca această toleranță să fie aleasă prea mică pe cazul nepătratic (i.e. reziduul minim Ax-b să fie mai mare decât toleranța; în cazul ăsta, programul nu se oprește decât at. când atinge nr. maxim de iterații)
        e = LA.norm(np.abs(1-np.abs(lsq_sol@x)/(LA.norm(lsq_sol)*LA.norm(x))))

        k = k+1
    
    
    t1 = (timeit.default_timer()-t0)
    return x,t1

"""
A = 20*(np.random.rand(200,300)-0.5)
b = 20*(np.random.rand(200)-0.5)
print(np.shape(A))
print(np.shape(b))


squares_sol = LA.lstsq(A,b)[0]


tol = 1e-9
"""

"""
(sol,iter,time) = alg_kaczmarz_random(np.copy(A),np.copy(b),squares_sol,tol,1000000)
print("----------- soluția cu Kaczmarz aleatoriu------------")

print(sol)

print("----------- soluția reală a sistemului ---------------")
print(LA.lstsq(A,b))


print("nr de iterații:")
print(iter)

print("-------timpul------")
print(time)
"""

"""
(sol,iter,time) = alg_kaczmarz_cyclic(np.copy(A),np.copy(b),squares_sol,tol,1000000)
print("----------- soluția cu Kaczmarz cu iterație ciclică ------------")

print(sol)

print("----------- soluția reală a sistemului ---------------")
print(LA.lstsq(A,b))


print("nr de iterații:")
print(iter)

print("-------timpul------")
print(time)
"""

"""
print(A@sol)
print(b)

prod = np.transpose(A@sol)
print(LA.norm(A@sol-b))


test = LA.lstsq(A,b)[0]
residuals = LA.lstsq(A,b)[1]
print(test)

print("reziduul soluției")
print(residuals)
print(LA.norm(residuals))
"""