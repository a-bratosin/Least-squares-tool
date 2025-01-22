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
    QHBoxLayout,
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


def CMMP_subdeterminat(A_orig, b_orig):
    A = np.copy(A_orig)
    b = np.copy(b_orig)

    (m, n) = np.shape(A)
    (L,V,beta) = LQ(A)

    y = Ltris(L[:, :m], b)
    
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


class LTSQ_Visualization(QMainWindow):
    def __init__(self, matrix, b):
        super().__init__()
        self.setWindowTitle("Soluția CMMP")
        self.setGeometry(100, 100, 800, 600)

        # Interfață principală
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Label pentru instrucțiuni
        self.label = QLabel("Solutia problemei celor mai mici patrate:")
        self.layout.addWidget(self.label)

        # Tabele pentru A, b și soluție
        self.matrix_table = QTableWidget()
        self.vector_table = QTableWidget()
        self.solution_table = QTableWidget()
        self.layout.addWidget(self.matrix_table)
        self.layout.addWidget(self.vector_table)
        self.layout.addWidget(self.solution_table)

        # Butoane
        self.solve_button = QPushButton("Calculează CMMP")
        self.solve_button.clicked.connect(self.calculate_cmmp)

        self.layout.addWidget(self.solve_button)
        

        # Datele matricei și vectorului
        self.A = matrix
        self.b = b

        self.display_matrix(self.A, self.matrix_table, "Matricea A introdusa:")
        self.display_vector(self.b, self.vector_table, "b")
        
        
    def calculate_cmmp(self):
        (m, n) = np.shape(self.A)
        # Calcul CMMP
        A_copy = self.A.copy()
        b_copy = self.b.copy()
        z, residuals, rank, s = np.linalg.lstsq(self.A, b_copy, rcond=None)
        print("---z---")
        print(z)
        print(self.A @ z)
        
        
        if (m >= n):
            x = CMMP_supradeterminat(A_copy, b_copy)
        else:
            x = CMMP_subdeterminat(A_copy, b_copy)

        
        # Afișare soluție în tabel
        self.display_vector(x.flatten(), self.solution_table, "Soluție CMMP")
        print("----x---")
        print(self.A @ x)
        

    def display_matrix(self, matrix, table_widget, header):
        rows, cols = matrix.shape
        table_widget.setRowCount(rows)
        table_widget.setColumnCount(cols)
        table_widget.setHorizontalHeaderLabels([f"{j+1}" for j in range(cols)])
        table_widget.setVerticalHeaderLabels([f"{i+1}" for i in range(rows)])

        for i in range(rows):
            for j in range(cols):
                item = QTableWidgetItem(f"{matrix[i, j]:.6f}")
                table_widget.setItem(i, j, item)

        table_widget.setWindowTitle(header)

    def display_vector(self, vector, table_widget, header):
        rows = len(vector)
        table_widget.setRowCount(rows)
        table_widget.setColumnCount(1)
        table_widget.setHorizontalHeaderLabels([header])
        table_widget.setVerticalHeaderLabels([f"{i+1}" for i in range(rows)])

        for i in range(rows):
            item = QTableWidgetItem(f"{vector[i]:.6f}")
            table_widget.setItem(i, 0, item)

        table_widget.setWindowTitle(header)
