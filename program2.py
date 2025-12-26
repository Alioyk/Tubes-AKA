import sys
import time
import random
import matplotlib.pyplot as plt
from tabulate import tabulate

# set batas rekursif
sys.setrecursionlimit(5000)

class DynamicWalletBenchmark:
    def __init__(self):
        self.history_n = []
        self.history_iter_time = []
        self.history_rec_time = []

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title("Performance Comparison: Iteratif vs Rekursif")
        self.ax.set_xlabel("Jumlah Transaksi (N)")
        self.ax.set_ylabel("Execution Time (seconds)")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        self.line_iter, = self.ax.plot([], [], 'b-o', linewidth=2, label='Iteratif')
        self.line_rec, = self.ax.plot([], [], 'r-x', linewidth=2, label='Rekursif')
        self.ax.legend()

    # ITERATIF
    def hitung_iteratif(self, data):
        total = 0
        for nilai in data:
            total += nilai
        return total
    
    # REKURSIF
    def hitung_rekursif(self, data, n):
        if n == 0:
            return 0
        return data[n-1] + self.hitung_rekursif(data, n-1)

    # UPDATE GRAFIK
    def update_plot(self):
        combined = sorted(zip(self.history_n, self.history_iter_time, self.history_rec_time))
        if not combined:
            return

        n_sorted, iter_sorted, rec_sorted = zip(*combined)
        self.line_iter.set_data(n_sorted, iter_sorted)
        self.line_rec.set_data(n_sorted, rec_sorted)
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    # TAMPILKAN TABEL
    def tampilkan_tabel(self):
        combined = sorted(zip(self.history_n, self.history_iter_time, self.history_rec_time))
        table = []
        for n, t_iter, t_rec in combined:
            table.append([n, f"{t_iter:.6f}", f"{t_rec:.6f}"])

        print(tabulate(table, headers=["N", "Iterative Time (s)", "Recursive Time (s)"], tablefmt="grid"))

    # PROGRAM UTAMA
    def start(self):
        while True:
            try:
                user_input = input("\n>>> Masukkan N (atau 'keluar'): ")
                if user_input.lower() == 'keluar':
                    break
                
                n = int(user_input)
                if n <= 0:
                    print("Masukkan angka positif (N > 0)")
                    continue
                
                print(f"-> Men-generate {n} data dan meng-run test...")
                data_transaksi = [random.randint(10000, 500000) for _ in range(n)]

                start_t = time.perf_counter()
                self.hitung_iteratif(data_transaksi)
                time_iter = time.perf_counter() - start_t

                time_rec = None
                try:
                    start_t = time.perf_counter()
                    self.hitung_rekursif(data_transaksi, n)
                    time_rec = time.perf_counter() - start_t
                except RecursionError:
                    print(f"MAX N={n} terlalu BESAR untuk Rekursif. Skip.")
                
                if time_rec is not None:
                    self.history_n.append(n)
                    self.history_iter_time.append(time_iter)
                    self.history_rec_time.append(time_rec)
                    print(f"Hasil: Iteratif={time_iter:.6f}s, Rekursif={time_rec:.6f}s")

                    # Update grafik dan tabel
                    self.update_plot()
                    self.tampilkan_tabel()

            except ValueError:
                print("Input tidak valid. Masukkan angka bulat.")

        print("\nProgram berhenti. Menutup grafik...")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    app = DynamicWalletBenchmark()
    app.start()
