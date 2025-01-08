from visualization_input import MainWindow
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit,QApplication,QWidget, QPushButton, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel

app = QApplication([])


window = MainWindow()
window.show()

app.exec()
