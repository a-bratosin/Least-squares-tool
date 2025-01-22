# QR and Kaczmarz Algorithm Visualization

This project provides a Python-based graphical user interface (GUI) to visualize and compare numerical methods for solving systems of equations and matrix decompositions. The focus is on:

- **QR Algorithm Visualization**  

- **Least Squares Problem Solution**  
- **Comparison of the Kaczmarz Algorithm with QR and Least Squares**

The application is built using **PyQt5**, along with **NumPy**, **joblib**, and **timeit** for backend computations.

---

## Features

### 1. **QR Algorithm Visualizer**

- Watch the QR decomposition process step by step.  
- Input a matrix and observe the progression of the algorithm.  

### 2. **Kaczmarz vs Other Algorithms**

- Compare the efficiency and performance of the **Kaczmarz Algorithm** with:  
  - QR decomposition  
  - Least squares solutions  

### 3. **Least Squares Solution**

- Input a matrix to compute and view the least squares solution directly.  
- Visual and numerical output to better understand the results.

---

## Installation and Setup

To run this project, ensure you have the following modules installed:

- **PyQt5**: For building the graphical user interface.  
- **NumPy**: For numerical computations.  
- **joblib**: For efficient saving and loading of data.  
- **timeit**: For performance benchmarking.  

### Steps to Set Up

1. Clone this repository to your local machine:

    ```bash
        git clone git@github.com:a-bratosin/Least-squares-tool.git   # Via ssh
        cd Least-squares-tool
    ```

1. Create a virtual environment (optional but recommended)

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

1. Install dependencies

    ```bash
    pip install PyQt5 numpy joblib timeit
    ```

1. Run the program

    ```bash
    python menu.py
    ```

## Usage

### Main Menu

The main program is `menu.py`, which launches the GUI. The interface provides three main functionalities accessible via buttons:

1. **QR Algorithm Visualizer**

   - Input a matrix and visualize the step-by-step QR decomposition process.  
2. **Kaczmarz vs Other Algorithms**  
   - Compare the efficiency of the Kaczmarz Algorithm against QR decomposition and Least Squares solutions.  
3. **Least Squares Solution**  
   - Enter a matrix to compute and view the least squares solution.

## Input

- Matrices are entered through the graphical user interface (GUI).  
- Ensure the input follows the correct format (e.g., numeric matrices).

Each feature provides an intuitive interface to help users understand and compare the algorithms effectively.
