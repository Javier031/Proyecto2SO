import tkinter as tk
from tkinter import ttk
from ui.simulador import VentanaSimulador

ALGOS = ["FCFS", "SJF", "SRTF", "RR"]

class MenuInicio(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#111")
        title = tk.Label(self, text="Simulador de Planificación de Procesos", fg="#eee", bg="#111", font=("Segoe UI", 14, "bold"))
        title.pack(pady=(16,6))
        tk.Label(self, text="Selecciona un algoritmo y configura parámetros", fg="#bbb", bg="#111").pack(pady=(0,12))

        form = tk.Frame(self, bg="#111"); form.pack(pady=6)
        tk.Label(form, text="Algoritmo:", fg="#ddd", bg="#111").grid(row=0, column=0, sticky="e", padx=6, pady=4)
        self.alg = tk.StringVar(value="FCFS")
        ttk.Combobox(form, textvariable=self.alg, values=ALGOS, width=10, state="readonly").grid(row=0, column=1, sticky="w", pady=4)

        tk.Label(form, text="Memoria total (MB):", fg="#ddd", bg="#111").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.mem = tk.StringVar(value="1024")
        tk.Entry(form, textvariable=self.mem, width=10).grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(form, text="Quantum por defecto:", fg="#ddd", bg="#111").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.qdef = tk.StringVar(value="2")
        tk.Entry(form, textvariable=self.qdef, width=10).grid(row=2, column=1, sticky="w", pady=4)

        tk.Label(form, text="Tick (ms):", fg="#ddd", bg="#111").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        self.tick = tk.StringVar(value="1000")
        tk.Entry(form, textvariable=self.tick, width=10).grid(row=3, column=1, sticky="w", pady=4)

        btn = tk.Button(self, text="Abrir simulador", command=self._abrir, padx=12, pady=6)
        btn.pack(pady=12)

    def _abrir(self):
        top = tk.Toplevel(self.master)
        top.title(f"Simulador — {self.alg.get()}")
        top.geometry("1200x720")
        VentanaSimulador(top,
                         algoritmo=self.alg.get(),
                         memoria_total=int(self.mem.get() or 1024),
                         quantum_defecto=int(self.qdef.get() or 2),
                         tick_ms=int(self.tick.get() or 1000)).pack(fill="both", expand=True)
