from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QLineEdit,QApplication,QWidget, QPushButton, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel
from PyQt6.QtGui import QColor, QPalette

app = QApplication([])

# matrice de stringuri, în care sunt scrise inițial elementele matricei
# apoi, când utilizatorul apasă ok, matricea este transformată în array de numpy, verificându-se dacă acest lucru este posibil
class StringMatrix:
    def __init__(self, rows, columns):
        self.content = [["" for x in range(columns)] for y in range(rows)]
    
    def display_elements(self):
        print(self.content)
        
       

class MatrixLine(QLineEdit):
    def __init__(self, row, column, matrix):
        super().__init__()

        self.matrix_row = row
        self.matrix_column = column
        self.modified_matrix = matrix

        #self.returnPressed.connect(self.return_pressed)
        #self.selectionChanged.connect(self.selection_changed)
        self.textChanged.connect(self.update_matrix)
        self.textEdited.connect(self.text_edited)
    
    def update_matrix(self,s):
        print("Text changed!")
        print("At position: " + str(self.matrix_row) + "," + str(self.matrix_column))
        self.modified_matrix.content[self.matrix_row][self.matrix_column] = s
        print(self.modified_matrix.content)

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
        
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)
"""

class MatrixGrid(QGridLayout):
    def __init__(self, nr_rows, nr_columns):
        super().__init__()

        self.strings = StringMatrix(nr_rows,nr_columns)
        for i in range(nr_rows):
            for j in range(nr_columns):
                self.addWidget(MatrixLine(i,j,self.strings),i,j)

class SizeSelection(QHBoxLayout):
    def __init__(self):
        super().__init__()

        label1 = QLabel("Nr de linii:")
        row_selector = QComboBox()
        row_selector.insertItems(0, ["3","4","5","6"])
        label2 = QLabel("Nr de coloane:")
        column_selector = QComboBox()
        column_selector.insertItems(0, ["3","4","5","6"])
        
        self.addWidget(label1)
        self.addWidget(row_selector)
        self.addWidget(label2)
        self.addWidget(column_selector)

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
        """
        layout = QGridLayout()
        strings = StringMatrix(3,3)
        layout.addWidget(MatrixLine(0,0, strings),0,0)
        layout.addWidget(MatrixLine(0,1, strings),0,1)
        layout.addWidget(MatrixLine(1,1, strings),1,1)
        layout.addWidget(MatrixLine(2,2, strings),2,2)
        """

        
        matrix = MatrixGrid(3,3)
        
        
        
        
        frame = QVBoxLayout()
        test = SizeSelection()
        frame.addLayout(test)
        frame.addLayout(matrix)
        
        layout = QHBoxLayout()
        layout.addLayout(frame)
        
        button = QPushButton()
        button.clicked.connect(lambda clicked: self.show_matrix(clicked,matrix))
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    
    def show_matrix(self,clicked, matrix):
        print(matrix.strings.content)


    


window = MainWindow()
window.show()

app.exec()