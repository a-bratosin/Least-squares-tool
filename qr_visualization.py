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


# alg de triangulatizare ortogonală cu reflectori
def TORT_with_steps(A):
    (m, n) = np.shape(A)
    p = min(m - 1, n)
    beta = np.zeros(p)
    beta = beta.astype(float)
    # matricea ce stochează toți vectorii u(k)
    # are dimensiunile mxp deoarece înmagazinează p vectori de lungime m, generând un vector pentru fiecare iterație a algoritmului
    # pentru sisteme supradeterminate, U o să aibă dimensiunile (m,n)
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
        yield np.copy(A), np.copy(U), np.copy(beta)

    return A, U, beta


class QRVisualization(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Algorithm Visualization")

        # Componente UI
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.step_label = QLabel("Step: 0") #afiseaza numarul curent al pasului
        self.matrix_table = QTableWidget() #afiseaza matricea A la fiecare pas
        
        self.u_table = QTableWidget() #afiseaza vectorul U la fiecare pas
        
        self.next_button = QPushButton("Next Step") #buton pentru a avansa la pasul urmator
        
        self.matrix_label = QLabel("Matrix A:")
        self.u_label = QLabel("Matrix U:")

        self.layout.addWidget(self.step_label)
        self.layout.addWidget(self.matrix_label)
        self.layout.addWidget(self.matrix_table)
        self.layout.addWidget(self.u_label)
        self.layout.addWidget(self.u_table)
        self.layout.addWidget(self.next_button)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.qr_generator = None
        self.current_step = 0

        # conectam senmnalul de click al butonului cu metoda next step
        self.next_button.clicked.connect(self.next_step)

        # Example matrix
        # TODO: preia matrice de la visualization_input.py
        self.matrix = rng.integers(1, 11, size=(8, 8)).astype(float)
        
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
                item = QTableWidgetItem(str(U[i, j]))  # Convertește fiecare valoare în string
                self.u_table.setItem(i, j, item)


    def next_step(self):
        try:
            A, U, beta = next(self.qr_generator)
            self.current_step += 1
            self.step_label.setText(f"Step: {self.current_step}")
            self.update_table(A)  # Visualize A
            self.update_u_table(U)  # Visualize U
        except StopIteration:
            self.step_label.setText("Algorithm complete!")
            self.next_button.setEnabled(False)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = QRVisualization()
#     window.show()
#     sys.exit(app.exec())
