import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import joblib
#import qr_visualization

lstsq_row_sizes = joblib.load("benchmark_algorithms/benchmark/lstsq/lstsq_rows.pkl")
lstsq_times = joblib.load("benchmark_algorithms/benchmark/lstsq/lstsq_times.pkl")

"""
# interpolare
lstsq_spline = make_interp_spline(np.asarray(lstsq_row_sizes),np.log10(np.asarray(lstsq_times)))
lstsq_x_spline = np.linspace(np.asarray(lstsq_row_sizes).min(), np.asarray(lstsq_row_sizes).max(), 1000)
lstsq_y_spline = lstsq_spline(lstsq_x_spline)
"""
# citirea datelor pt Kaczmarz

kzmr_rows_07 = joblib.load("benchmark_algorithms/benchmark/kaczmarz/rbk_row_backup0-7.pkl")
kzmr_rows_814 = joblib.load("benchmark_algorithms/benchmark/kaczmarz/rbk_row_backup8-14.pkl")
kzmr_rows_1525 = joblib.load("benchmark_algorithms/benchmark/kaczmarz/rbk_row_backup15-25.pkl")

kzmr_rows = kzmr_rows_07 + kzmr_rows_814 + kzmr_rows_1525

kzmr_times_07 = joblib.load("benchmark_algorithms/benchmark/kaczmarz/rbk_time_backup0-7.pkl")
kzmr_times_814 = joblib.load("benchmark_algorithms/benchmark/kaczmarz/rbk_time_backup8-14.pkl")
kzmr_times_1525 = joblib.load("benchmark_algorithms/benchmark/kaczmarz/rbk_time_backup15-25.pkl")

kzmr_times = kzmr_times_07 + kzmr_times_814 + kzmr_times_1525

#print(np.asarray(kzmr_times))
"""
# interpolare
kzmr_spline = make_interp_spline(np.asarray(kzmr_rows),(np.asarray(kzmr_times)))
kzmr_x_spline = np.linspace(np.asarray(kzmr_rows).min(), np.asarray(kzmr_rows).max(), 1000)
kzmr_y_spline = lstsq_spline(kzmr_x_spline)
"""

lq_row_sizes = joblib.load("benchmark_algorithms/benchmark/qr/lq_row_sizes0-7.pkl")
lq_times = joblib.load("benchmark_algorithms/benchmark/qr/lq_times0-7.pkl")



print("loaded")
ax = plt.subplot(111)
ax.semilogy(lstsq_row_sizes,lstsq_times)
ax.semilogy(kzmr_rows, kzmr_times)
ax.semilogy(lq_row_sizes, lq_times)
plt.xlabel("Mărimea lui m")
plt.ylabel("Timpul de execuție (secunde)")
plt.legend(["Least squares din numpy", "RBK", "LQ"])
"""
plt.figure()
#plt.plot(lstsq_x_spline, lstsq_y_spline)
plt.semilogy(kzmr_x_spline, kzmr_y_spline)
"""
plt.show()
joblib.dump(ax, "graph.pkl")

