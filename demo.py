from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QLineEdit,QApplication,QWidget, QPushButton, QMainWindow, QGridLayout
from PyQt6.QtGui import QColor, QPalette

app = QApplication([])

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

       

class MatrixLine(QLineEdit):
    def __init__(self, row, column):
        super().__init__()

        matrix_row = row
        matrix_column = column
        
        self.returnPressed.connect(self.return_pressed)
        self.selectionChanged.connect(self.selection_changed)
        self.textChanged.connect(self.text_changed)
        self.textEdited.connect(self.text_edited)
        
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)
"""
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QLineEdit()
        widget.setMaxLength(20)
        widget.setPlaceholderText("Enter your text")

        #widget.setReadOnly(True) # uncomment this to make readonly
        """
        widget.returnPressed.connect(self.return_pressed)
        widget.selectionChanged.connect(self.selection_changed)
        widget.textChanged.connect(self.text_changed)
        widget.textEdited.connect(self.text_edited)
        """

        layout = QGridLayout()
        layout.addWidget(MatrixLine(0,0),0,0)
        layout.addWidget(MatrixLine(0,1),0,1)
        layout.addWidget(MatrixLine(1,1),1,1)
        layout.addWidget(MatrixLine(2,2),2,2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        


    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)


window = MainWindow()
window.show()

app.exec()