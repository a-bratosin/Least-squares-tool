import matplotlib.pyplot as plt
import joblib

row_sizes = joblib.load("row_backup.pkl")
times = joblib.load("time_backup.pkl")

plt.semilogy(row_sizes,times)
plt.show()
