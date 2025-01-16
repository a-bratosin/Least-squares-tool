
import numpy as np
import numpy.linalg as LA
import timeit


# funcție de partiționare a matricei A în tau matrici peste care se poate face block Kaczmarz
def select_partition(A):
    (m,n) = np.shape(A)
    
    # pentru matrice m mici (<100), iau partiționarea 10
    # pentru m mai mari, tau este 10%*m
    # așadar, blocurile o să aibă maxim 10 linii

    tau = m//10

    J = []
    for k in range(tau-1):
        new_block = A[k*10:((k+1)*10),:]
        #print(new_block)
        J.append(new_block)
    
    # deoarece împărțirea la 10 o să aibă mai mereu rest, îi dau ultimei matrici liniile din rest
    new_block = A[10*(tau-1):,:]
    J.append(new_block)

    return J


# funcție pentru determinarea distribuției de probabilitate a blocurilor J
def select_distribution(J,A):
    tau = len(J)
    distribution = np.zeros(tau)

    for k in range(tau):
        #print(k)
        distribution[k] = LA.norm(J[k])**2/LA.norm(A)**2
    
    return distribution

def RBK(A, b, target, tol):
    (m,n) = np.shape(A)
    t0 = timeit.default_timer()
    J = select_partition(A)

    prob = select_distribution(J, A)
    
    # eroarea algoritmului
    e = 1

    #x = A[0,:]
    x= np.zeros(n)
    #print(len(J))
    while(e>tol):
        # selectează din lista de blocuri un J conform distribuției de probabilitate dată
        # aș putea să rescriu distribuția asta fără să memorez și J-ul, dar văd mai întâi dacă merge așa
        J_k = J[np.random.choice(range(len(J)), p=prob)]
        rows = np.shape(J_k)[0]

        # calculez step size-ul pentru pasul actual
        step_size_sum = 0
        step_size_vector_sum = np.zeros(n)
        for i in range(rows):
            weight = 1/LA.norm(J_k)**2
            #weight = weight/LA.norm(J_k[i, :])**2

            projection = J_k[i]@x - b[i]
            #print(type(projection))
            step_size_sum = step_size_sum + weight*projection*projection
            step_size_vector_sum = step_size_vector_sum + weight*projection*J_k[i, :]
        
        step_size = step_size_sum/(LA.norm(step_size_vector_sum)**2) # acum stochează val. lui Lk

        step_size = 1.5*step_size

        block_projection = np.zeros(n)
        
        for i in range(rows):
            weight = LA.norm(J_k[i, :])**2/LA.norm(J_k)**2
            projection = J_k[i,:]@x - b[i]

            block_projection = block_projection + (weight*projection/LA.norm(J_k[i, :])**2)*J_k[i, :]

        block_projection = step_size*block_projection

        y = x - block_projection
        #print(np.shape(x))
        #print(np.shape(target))
        e =  LA.norm(x-y)
        x=y
        #print(e)
        #print(x)

    t1 = timeit.default_timer() -t0
    return x,t1
        



"""
A_test = 100*np.random.rand(125,5)
print("Mat A\n\n", A_test, "\n\n")

J = select_partition(A_test)

#print(J)
distributions = block_distribution(J,A_test)

sum = 0
for distribution in distributions:
    sum = sum + distribution

print(sum)
   """ 

"""
A_test = 100*np.random.rand(405,600)
print(A_test)
x_generate = 100*np.random.rand(600)

b_test = A_test@x_generate

least_sq = LA.lstsq(A_test,b_test)[0]

sol,time = RBK(A_test,b_test,least_sq,1e-7)
print(sol)
"""