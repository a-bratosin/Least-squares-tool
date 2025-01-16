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
import sys

rng = np.random.default_rng(5)

# Algoritmul UTRIS
def Utris(U, b):
    n = len(U)
    x = np.zeros((n, 1))
    for i in range(n - 1, -1, -1):
        s = b[i]
        for j in range(i + 1, n):
            s = s - U[i][j] * x[j]
        x[i] = s / U[i][i]
    return x


# Algoritmul LTRIS
def Ltris(L, b):
    n = len(L)
    x = np.zeros(n)
    for i in range(n):
        s = b[i]
        for j in range(i):
            s = s - L[i][j]*x[j]
        x[i] = s/L[i][i]
    return x

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


# Se efectueaza triangularizarea ortogonala la dreapta a matricei A, i.e. AZ = L, unde Z = Z1Z2...Zs, iar Zk sunt reflectori hermitici.
def LQ(A_in):
    A = np.copy(A_in)
    (m,n) = np.shape(A)
    s = min(m,n)

    beta = np.zeros(s)
    V = np.zeros((s,n))

    for k in range(s):
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
    A_copy = np.copy(A)
    (m, n) = np.shape(A)
    (R, U, beta) = TORT(np.transpose(A))
    
    R_tr = np.transpose(R)
    print(R_tr[:, :m])

    y = Ltris(R_tr[:, :m], b)
    print(y)

    y = np.append(y, np.zeros(n - m).astype(float))
    for k in range(m, -1, -1):
        tau = 0
        for i in range(k, n):

            test = U[i][k]
            # print(y[i])
            tau += U[i][k] * y[i]
        tau = tau / beta[k]

        # print(tau)
        for i in range(k, n):
            y[i] = y[i] - tau * U[i][k]

    x = y
    return x


class LTSQ_Visualization(QMainWindow):
    def __init__(self, matrix):
        super().__init__()
        self.setWindowTitle("Soluția CMMP")
        self.setGeometry(100, 100, 800, 600)
        self.matrix = matrix

        # Interfață principală
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Apasă pe buton pentru a calcula soluția.")
        self.layout.addWidget(self.label)
        
        self.label = QLabel("Matricea introdusa initial.")
        self.layout.addWidget(self.label)
        

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.button = QPushButton("Calculează CMMP")
        self.button.clicked.connect(self.calculate_cmmp)
        self.layout.addWidget(self.button)

    def calculate_cmmp(self):
        # Generare matrice A și vector b
        A = self.matrix
        b = rng.random(5)

        # Calcul CMMP
        x = CMMP_supradeterminat(A, b)

        # Afișare rezultate în tabel
        self.display_solution(x)

    def display_solution(self, x):
        self.table.setRowCount(len(x))
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Soluție CMMP"])

        for i, value in enumerate(x):
            item = QTableWidgetItem(f"{value[0]:.6f}")
            self.table.setItem(i, 0, item)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = CMMPApp()
#     window.show()
#     sys.exit(app.exec())
