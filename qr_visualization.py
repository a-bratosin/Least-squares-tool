import sys
import numpy as np
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
import numpy.linalg as LA


rng = np.random.default_rng(0)


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


# Alg de triangulatizare ortogonală cu reflectori
def TORT_with_steps(A):
    (m, n) = np.shape(A)
    if(m==n): 
        p=m
    else:
        p = min(m - 1, n)

    beta = np.zeros(p, dtype=float)
    # Matricea ce stochează toți vectorii u(k)
    # Are dimensiunile mxp deoarece înmagazinează p vectori de lungime m, generând un vector pentru fiecare iterație a algoritmului
    # Pentru sisteme supradeterminate, U o să aibă dimensiunile (m,n)
    U = np.zeros((m, p), dtype=float)
    Q = np.eye(m, dtype=float)

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
        
            u = U[k:, k]
            v = u / LA.norm(u)
            B = np.eye(m, dtype=float)
            B[k:, k:] -= 2.0 * (v[:, None] @ v[None, :])  # B = I - 2vv^T
            
            Q = B @ Q
        
        yield np.copy(A), np.copy(U), np.copy(Q.T), np.copy(beta)

    return A, U, Q.T, beta


class QRVisualization(QMainWindow):
    def __init__(self, matrix):
        super().__init__()
        self.setWindowTitle("QR Algorithm Visualization")
        #Preia matricea de la 
        self.matrix = matrix

        # Componente UI
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.step_label = QLabel("Step: 0") #afiseaza numarul curent al pasului
        self.matrix_table = QTableWidget() #afiseaza matricea A la fiecare pas
        
        self.q_table = QTableWidget()
        
        self.u_table = QTableWidget() #afiseaza vectorul U la fiecare pas
        
        self.next_button = QPushButton("Next Step") #buton pentru a avansa la pasul urmator
        
        self.matrix_label = QLabel("Matrix R:")
        self.q_label = QLabel("Matrix Q:")
        self.u_label = QLabel("Matrix U:")
        
        self.layout.addWidget(self.step_label)

        self.layout.addWidget(self.matrix_label)
        self.layout.addWidget(self.matrix_table)

        self.layout.addWidget(self.q_label)
        self.layout.addWidget(self.q_table)

        self.layout.addWidget(self.u_label)
        self.layout.addWidget(self.u_table)

        self.layout.addWidget(self.next_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.qr_generator = None
        self.current_step = 0

        # conectam senmnalul de click al butonului cu metoda next step
        self.next_button.clicked.connect(self.next_step)
        
        #se initializeaza algoritmul
        self.reset_algorithm()

    def reset_algorithm(self):
        self.qr_generator = TORT_with_steps(self.matrix)
        self.current_step = 0
        self.step_label.setText("Step: 0")
        self.update_table(self.matrix)

    def update_table(self, matrix):
        rows, cols = matrix.shape
        self.matrix_table.setRowCount(rows)
        self.matrix_table.setColumnCount(cols)
        for i in range(rows):
            for j in range(cols):
                self.matrix_table.setItem(i, j, QTableWidgetItem(f"{matrix[i, j]:.4f}"))

    def update_u_table(self, U):
        rows, cols = U.shape
        self.u_table.setRowCount(rows)
        self.u_table.setColumnCount(cols)
        for i in range(rows):
            for j in range(cols):
                # item = QTableWidgetItem(str(U[i, j]))
                # self.u_table.setItem(i, j, item)
                self.u_table.setItem(i, j, QTableWidgetItem(f"{U[i, j]:.4f}"))

    def update_q_table(self, Q):
        rows, cols = Q.shape
        self.q_table.setRowCount(rows)
        self.q_table.setColumnCount(cols)
        for i in range(rows):
            for j in range(cols):
                self.q_table.setItem(i, j, QTableWidgetItem(f"{Q[i, j]:.4f}"))

    def next_step(self):
        try:
            A, U, Q, beta = next(self.qr_generator)
            self.current_step += 1
            self.step_label.setText(f"Step: {self.current_step}")
            self.update_table(A)  # Visualize A
            self.update_q_table(Q)
            self.update_u_table(U)  # Visualize U

        except StopIteration:
            self.step_label.setText("Algorithm complete!")
            self.next_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRVisualization()
    window.show()
    sys.exit(app.exec())
