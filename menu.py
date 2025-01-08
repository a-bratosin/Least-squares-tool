from visualization_input import QRInputWindow
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit,QApplication,QWidget, QPushButton, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton

app = QApplication([])

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        qt_vis = QPushButton("QR factorisation")

        qt_vis.setStyleSheet("padding: 10px;")
        lstsq = QPushButton("Least Squares Solver")
        lstsq.setStyleSheet("padding: 10px;")
        kzmr = QPushButton("Kaczmarz vs QR factorization")
        kzmr.setStyleSheet("padding: 10px;")
        

        layout = QVBoxLayout()
        
        layout.addWidget(qt_vis)
        layout.addWidget(lstsq)
        layout.addWidget(kzmr)
        

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    

window = MainMenu()
window.show()

app.exec()
