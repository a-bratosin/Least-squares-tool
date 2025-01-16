from visualization_input import QRInputWindow
from qr_visualization import QRVisualization
from ltsq_input import LtsqInputWindow
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit,QApplication,QWidget, QPushButton, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton

app = QApplication([])

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        qt_vis = QPushButton("QR factorisation")

        qt_vis.setStyleSheet("padding: 10px;")
        qt_vis.clicked.connect(self.open_qr_input)

        lstsq = QPushButton("Least Squares Solver")
        lstsq.clicked.connect(self.open_ltsq_input)

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
        self.qr_window = None
        self.ltsq_window = None

    def open_qr_input(self):
        self.hide()

        self.qr_window = QRInputWindow()
        self.qr_window.show()
        self.qr_window.destroyed.connect(self.show_main_menu)

    def open_ltsq_input(self):
        self.hide()

        self.ltsq_window = LtsqInputWindow()
        self.ltsq_window.show()
        self.ltsq_window.destroyed.connect(self.show_main_menu)

    def show_main_menu(self):
        self.show()


    

window = MainMenu()
window.show()

app.exec()
