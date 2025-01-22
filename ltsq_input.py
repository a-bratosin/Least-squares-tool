from least_squares import LTSQ_Visualization
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QLineEdit,QApplication,QWidget, QPushButton, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QDialogButtonBox
from PyQt6.QtGui import QColor, QPalette
import numpy as np


# matrice de stringuri, în care sunt scrise inițial elementele matricei
# apoi, când utilizatorul apasă ok, matricea este transformată în array de numpy, verificându-se dacă acest lucru este posibil
class StringMatrix:
    def __init__(self, rows, columns):
        self.content = [["" for x in range(columns)] for y in range(rows)]
    
    def display_elements(self):
        print(self.content)
        

class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Least Squares Tool")

        QBtn = QDialogButtonBox.StandardButton.Close

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Eroare! Matrice introdusă incorect!")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

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

class MatrixGrid(QGridLayout):
    def __init__(self, nr_rows, nr_columns):
        super().__init__()

        self.rows = nr_rows
        self.columns = nr_columns
        self.strings = StringMatrix(nr_rows,nr_columns)
        for i in range(nr_rows):
            for j in range(nr_columns):
                self.addWidget(MatrixLine(i,j,self.strings),i,j)
    
    def resize_matrix(self, new_rows=-1, new_columns=-1):
        if(new_rows==-1):
            new_rows = self.rows
        if(new_columns==-1):
            new_columns = self.columns
        
        if(new_rows>self.rows):
            self.add_rows(new_rows)
        if(new_rows<self.rows):
            self.remove_rows(new_rows)

        if(new_columns>self.columns):
            self.add_columns(new_columns)
        if(new_columns<self.columns):
            self.remove_columns(new_columns)

        self.resize_contents(new_rows, new_columns)

        self.rows = new_rows
        self.columns = new_columns
        
        print("linii noi: ", self.rows, " coloane noi: ", self.columns)

    def resize_contents(self, new_rows, new_columns):
        new_strings = [["" for x in range(new_columns)] for y in range(new_rows)]

        for i in range(min(self.rows, new_rows)):
            for j in range(min(self.columns, new_columns)):
                new_strings[i][j] = self.strings.content[i][j]
        
        self.strings.content = new_strings

    # aici asum că new_rows> rows
    def add_rows(self,new_rows):
        if(new_rows <= self.rows):
            print("Programul încearcă să mărească nr. de linii cu un nr mai mic decât cel existent!")
            return
        for i in range(self.rows, new_rows):
            for j in range(self.columns):
                self.addWidget(MatrixLine(i,j, self.strings), i,j)

    def remove_rows(self, new_rows):
        if(new_rows >= self.rows):
            print("Programul încearcă să scadă nr. de linii cu un nr mai mare decât cel existent!")
            return
        for i in range(self.rows-1, new_rows-1, -1):
            for j in range(self.columns):
                element_to_delete = self.itemAtPosition(i,j)
                element_to_delete.widget().hide()
                self.removeItem(element_to_delete)

    def add_columns(self,new_columns):
        if(new_columns <= self.columns):
            print("Programul încearcă să mărească nr. de coloane cu un nr mai mic decât cel existent!")
            print("Coloane noi: ",new_columns," Coloane vechi:",self.rows)
            return
        for j in range(self.columns, new_columns):
            for i in range(self.rows):
                self.addWidget(MatrixLine(i,j, self.strings), i,j)

    def remove_columns(self, new_columns):
        if(new_columns >= self.columns):
            print("Programul încearcă să scadă nr. de coloane cu un nr mai mare decât cel existent!")
            return
        for j in range(self.columns-1, new_columns-1, -1):
            for i in range(self.rows):
                element_to_delete = self.itemAtPosition(i,j)
                element_to_delete.widget().hide()
                self.removeItem(element_to_delete)
    

class SizeSelection(QHBoxLayout):
    def __init__(self, wrapper, vector_input):
        super().__init__()

        self.wrapper = wrapper
        self.vector_input = vector_input

        label1 = QLabel("Nr de linii:")
        row_selector = QComboBox()
        row_selector.insertItems(0, ["2","3","4","5","6", "7", "8", "9", "10"])
        row_selector.setCurrentIndex(1)
        row_selector.textActivated.connect(lambda text: self.update_matrix_size(new_rows=text))
        #row_selector.setStyleSheet("margin-right: 10px")
        label2 = QLabel("Nr de coloane:")
        
        #label2.setStyleSheet("margin-left: 10px")
        column_selector = QComboBox()
        column_selector.insertItems(0, ["2","3","4","5","6", "7", "8", "9", "10"])
        column_selector.setCurrentIndex(1)
        column_selector.textActivated.connect(lambda text: self.update_matrix_size(new_columns=text))

        self.addWidget(label1)
        self.addWidget(row_selector)
        self.addWidget(label2)
        self.addWidget(column_selector)
    
    def test(self, text):
        print(text)
    # funcție care funcționează atât pentru actualizarea rândurilor, cât și a coloanelor
    def update_matrix_size(self, new_rows=-1, new_columns=-1):
        # obține matricea din interiorul wrapper-ului pentru a putea extrage informații din ea
        matrix = self.wrapper.itemAtPosition(0,0)

        # dacă nr de linii nu este invocat, rămâne același
        if new_rows == -1:
            rows = matrix.rows
            
            columns = int(new_columns)
            print("New column count: ", columns)
        # idem pt coloane
        if new_columns == -1:
            columns = matrix.columns
            
            rows = int(new_rows)
            print("New row count: ", rows)    
        matrix.resize_matrix(rows, columns)
        self.vector_input.resize_vector(rows)


class VectorLine(QLineEdit):
    def __init__(self, index, vector):
        super().__init__()
        self.index = index
        self.vector = vector
        self.textChanged.connect(self.update_vector)

    def update_vector(self, s):
        print(f"Text changed in vector at index {self.index}: {s}")
        self.vector[self.index] = s


class VectorInput(QVBoxLayout):
    def __init__(self, nr_rows):
        super().__init__()
        self.nr_rows = nr_rows
        self.vector = ["" for _ in range(nr_rows)]

        self.labels = QLabel("Introduceți vectorul b:")
        self.addWidget(self.labels)

        self.vector_lines = []
        for i in range(nr_rows):
            line = VectorLine(i, self.vector)
            self.addWidget(line)
            self.vector_lines.append(line)

    def resize_vector(self, new_rows):
        # Resize vector and update UI
        if new_rows > self.nr_rows:
            for i in range(self.nr_rows, new_rows):
                line = VectorLine(i, self.vector)
                self.addWidget(line)
                self.vector_lines.append(line)
                self.vector.append("")
        elif new_rows < self.nr_rows:
            for i in range(self.nr_rows - 1, new_rows - 1, -1):
                line = self.vector_lines.pop()
                line.hide()
                self.takeAt(self.indexOf(line))
                del self.vector[i]

        self.nr_rows = new_rows
        print(f"Vector resized to {self.nr_rows} elements.")

    def get_vector(self):
        return self.vector


class LtsqInputWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Least Squares Tool")
        
        self.ls_window = None

        widget = QLineEdit()
        widget.setMaxLength(20)
        widget.setPlaceholderText("Enter your text")

        wrapper = QGridLayout()
        self.matrix = MatrixGrid(3,3)
        wrapper.addLayout(self.matrix,0,0)
        
        self.vector_input = VectorInput(3)
        
        frame = QVBoxLayout()
        test = SizeSelection(wrapper, self.vector_input)
        test.setContentsMargins(10,10,10,10)
        frame.addLayout(test)
        frame.addLayout(wrapper)
        frame.addLayout(self.vector_input)

        
        layout = QVBoxLayout()
        layout.addLayout(frame)
        
        button = QPushButton("Ok")
        button.clicked.connect(self.process_inputs)
        button.setStyleSheet("margin: 10px; alignment: center;")
        button.setMaximumWidth(150)
        button.setMinimumHeight(45)
        button.setMinimumWidth(100)
        #button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def process_inputs(self):
        try:
            np_matrix = to_numpy_array(self.matrix.strings.content)
            
            np_vector = np.array(self.vector_input.get_vector(), dtype=float)

            if np_matrix.shape[0] != len(np_vector):
                raise ValueError("Numărul de rânduri din matrice și dimensiunea vectorului b nu coincid.")

            self.hide()
            self.ls_window = LTSQ_Visualization(np_matrix, np_vector)
            self.ls_window.show()
        except ValueError as ve:
            print(f"Error: {ve}")
            dlg = ErrorDialog()
            dlg.exec()
        except Exception as e:
            print(f"Unexpected error: {e}")
            dlg = ErrorDialog()
            dlg.exec()
        


def to_numpy_array(string_matrix):
    numpy_matrix= np.asarray(string_matrix, dtype=float)

    return numpy_matrix

# if __name__ == "__main__":
#     import sys

#     # Create an instance of QApplication
#     app = QApplication(sys.argv)
    
#     # Create and show the main window
#     main_window = LtsqInputWindow()
#     main_window.show()
    
#     # Execute the application
#     sys.exit(app.exec())
