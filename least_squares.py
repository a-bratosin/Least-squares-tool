import numpy as np
import numpy.linalg as LA
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
)


def Utris(U, b):
    n = len(U)
    x = np.zeros((n, 1))
    for i in range(n - 1, -1, -1):
        s = b[i]
        for j in range(i + 1, n):
            s = s - U[i][j] * x[j]
        x[i] = s / U[i][i]
    return x


def Ltris(L, b):
    n = len(L)
    x = np.zeros((n, 1))

    for i in range(n):
        s = b[i]
        for j in range(i):
            s = s - L[i][j] * x[j]
        x[i] = s / L[i][i]
    return x


# alg de triangulatizare ortogonală cu reflectori
def TORT(A):
    (m, n) = np.shape(A)
    p = min(m - 1, n)
    beta = np.zeros(p)
    beta = beta.astype(float)

    U = np.zeros((m, p))
    U = U.astype(float)

    for k in range(p):
        sigma = np.sign(A[k][k]) * LA.norm(A[k:, k])

        if sigma == 0:
            beta[k] = 0
        else:
            U[k][k] = A[k][k] + sigma
            # stocăm coeficienții vectorului uk pentru restul coloanei
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

    return A, U, beta

#Se efectueaz˘a triangularizarea ortogonala la dreapta a matricei A, i.e. AZ = L, unde Z = Z1Z2...Zs, iar Zk sunt reflectori hermitici.
def LQ(A, v):
    (m,n) = np.shape(A)
    beta = np.zeros(s)
    for k in range(1, m + 1):
        beta[k] = 0

        # Dacă k < n
        if k < n:
            # Pasul 2: Se definește σ
            σ = A[k-1, k-1:n]  # Elementele de pe linia k, coloanele k până la n
            
            # Pasul 3: Dacă σ = 0
            if np.all(σ == 0):
                # Dacă akk = 0
                if A[k-1, k-1] == 0:
                    σ = np.abs(A[k-1, k-1])  # Folosim valoarea absolută
                else:
                    σ = np.abs(A[k-1, k-1])  # Restabilim valoarea

            # Actualizăm akj și vkj
            for j in range(k-1, n):
                A[k-1, j] = A[k-1, j] / σ  # Normalizare a akj
                v[k-1, j] = A[k-1, j]  # Actualizare vkj

            # Pasul 4: Setăm βk
            βk = 1 + A[k-1, k-1]

            # Pasul 5: Iterație pentru i = k+1 până la m
            for i in range(k, m):
                # Calculăm α
                α = - np.sum(A[i, k-1:n] * v[k-1, k-1:n]) / βk

                # Actualizăm elementele aij
                for j in range(k-1, n):
                    A[i, j] += α * v[k-1, j]

            # Pasul 6: Actualizăm akk
            A[k-1, k-1] = -np.abs(σ)

    return A, v

# CMMP pentru un sistem supradeterminat m > n
def CMMP_supradeterminat(A, b):
    (m, n) = np.shape(A)
    (R, U, beta) = TORT(A)

    for k in range(n):
        tau = 0
        for i in range(k, m):
            tau += U[i][k] * b[i]
        tau = tau / beta[k]

        for i in range(k, m):
            b[i] = b[i] - tau * U[i][k]

    x = Utris(R[:n, :], b[:n])
    return x


# CMMP pentru sistem subdeterminat m < n
def CMMP_subdeterminat(A, b):
    (m, n) = np.shape(A)
    x = np.zeros(n)
    for k in range(m):
        x[k] = Ltris(A, b)

    x[m:n] = 0

    for k in range(m, 0, -1):
        t = A[k - 1][k - 1]  # Salvam valoarea inițială a akk
        A[k - 1][k - 1] = v[k - 1]  # Setam akk la valoarea βk
        alpha = -np.sum([v[k - 1] * x[j - 1] for j in range(k, n)]) / v[k - 1]

        # Actualizarea valorilor din x
        for j in range(k - 1, n):
            x[j] += alpha * v[k - 1]

        A[k - 1][k - 1] = t  # Restauram valoarea inițială a akk

    return x
