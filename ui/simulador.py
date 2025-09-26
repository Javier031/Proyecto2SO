import tkinter as tk
from tkinter import ttk, messagebox
import random

from core.proceso import Proceso
from core.planificador import Planificador

class VentanaSimulador(tk.Frame):
    """
    UI fija, sin gráfica. Tablas SIEMPRE visibles en todos los algoritmos:
    - Pendientes (llegada futura)
    - Cola de Listos
    - CPU (en ejecución)
    - Espera de Memoria
    - Finalizados
    - Historial de eventos (ALTA, EJEC, PREEM, FIN)
    Controles arriba con textfields y botones.
    """
    def __init__(self, master, algoritmo, memoria_total=1024, quantum_defecto=2, tick_ms=1000):
        super().__init__(master, bg="#101010")
        self.plan = Planificador(algoritmo=algoritmo, memoria_total=memoria_total, quantum_defecto=quantum_defecto)
        self.tick_ms = int(tick_ms)
        self.sim_activa = False
        self._loop_job = None

        self._build_ui(algoritmo)
        self._refresh_all()

    # ---------- Layout ----------
    def _build_ui(self, algoritmo):
        header = tk.Frame(self, bg="#101010"); header.pack(fill="x", padx=10, pady=(10,6))
        tk.Label(header, text=f"Algoritmo: {algoritmo}", fg="#eee", bg="#101010", font=("Segoe UI", 13, "bold")).pack(side="left")
        self.var_info = tk.StringVar(value="t=0  |  RAM: 0/0 MB")
        tk.Label(header, textvariable=self.var_info, fg="#bbb", bg="#101010").pack(side="right")

        # Controles
        controls = tk.Frame(self, bg="#101010"); controls.pack(fill="x", padx=10, pady=(0,10))
        def _entry(width): return tk.Entry(controls, width=width)

        self.e_nombre = _entry(14); self.e_dur = _entry(6); self.e_lleg = _entry(6); self.e_mem = _entry(6); self.e_q = _entry(6)
        for txt, w in [("Nombre", self.e_nombre), ("Dur", self.e_dur), ("Lleg", self.e_lleg), ("MB", self.e_mem), ("Q", self.e_q)]:
            tk.Label(controls, text=txt+":", fg="#ddd", bg="#101010").pack(side="left"); w.pack(side="left", padx=(0,8))

        tk.Button(controls, text="Agregar", command=self._agregar_manual).pack(side="left", padx=6)
        tk.Button(controls, text="Aleatorio", command=self._agregar_random).pack(side="left", padx=6)
        self.btn_run = tk.Button(controls, text="Iniciar", command=self._toggle); self.btn_run.pack(side="left", padx=6)
        tk.Button(controls, text="Pausar/Reset reloj", command=self._reset_tiempo).pack(side="left", padx=6)
        tk.Button(controls, text="Cerrar", command=self._cerrar).pack(side="right")

        # Tablas
        body = tk.Frame(self, bg="#101010"); body.pack(fill="both", expand=True, padx=10, pady=(0,10))
        left = tk.Frame(body, bg="#101010"); left.pack(side="left", fill="both", expand=True, padx=(0,6))
        right = tk.Frame(body, bg="#101010"); right.pack(side="left", fill="both", expand=True, padx=(6,0))

        self.tv_pend = self._make_tv(left, "Pendientes (llegada futura)", ["PID","Nombre","MB","Dur","Rest","Lleg"])
        self.tv_list = self._make_tv(left, "Cola de LISTOS", ["PID","Nombre","Q","MB","Dur","Rest","Lleg"])
        self.tv_cpu  = self._make_tv(right, "CPU (ejecución)", ["PID","Nombre","Q","MB","Rest","Lleg"], height=3)
        self.tv_esp  = self._make_tv(right, "Espera de Memoria", ["PID","Nombre","MB","Dur","Rest","Lleg"], height=7)
        self.tv_fin  = self._make_tv(right, "Finalizados", ["PID","Nombre","Dur","Lleg","Fin"], height=7)
        self.tv_hist = self._make_tv(self, "Historial", ["T","Tipo","PID","Nombre","Alg","Rest"], height=8)
        self.tv_hist.pack(fill="both", expand=False, padx=10, pady=(0,10))

    def _make_tv(self, parent, title, cols, height=10):
        lf = tk.LabelFrame(parent, text=title, fg="#eee", bg="#101010")
        lf.pack(fill="both", expand=True, pady=(0,8))
        tv = ttk.Treeview(lf, show="headings", height=height, columns=cols)
        for c in cols: tv.heading(c, text=c); tv.column(c, anchor="center", width=90)
        tv.pack(fill="both", expand=True); return tv

    # ---------- Acciones ----------
    def _cerrar(self):
        if self._loop_job is not None:
            try: self.after_cancel(self._loop_job)
            except Exception: pass
            self._loop_job = None
        self.master.destroy()

    def _toggle(self):
        if self.sim_activa:
            self.sim_activa = False; self.btn_run.config(text="Iniciar")
            if self._loop_job is not None:
                try: self.after_cancel(self._loop_job)
                except Exception: pass
                self._loop_job = None
        else:
            self.sim_activa = True; self.btn_run.config(text="Pausar")
            self.plan.ingresar_llegadas()  # incorporar llegadas ya vencidas
            self._refresh_all()
            if self._loop_job is None:
                self._loop_job = self.after(1, self._loop)

    def _reset_tiempo(self):
        self.sim_activa = False; self.btn_run.config(text="Iniciar")
        if self._loop_job is not None:
            try: self.after_cancel(self._loop_job)
            except Exception: pass
            self._loop_job = None
        self.plan.t = 0
        self._refresh_all()

    def _agregar_manual(self):
        try:
            n = (self.e_nombre.get().strip() or None)
            d = int(self.e_dur.get().strip())
            l = int(self.e_lleg.get().strip() or self.plan.t)
            m = int(self.e_mem.get().strip() or 64)
            q = int(self.e_q.get().strip()) if self.e_q.get().strip() else None
            p = Proceso(n, d, l, memoria=m, quantum=q)
            self.plan.agregar(p)
            self.plan.ingresar_llegadas()
            self._refresh_all()
        except Exception:
            messagebox.showerror("Error", "Campos inválidos. Revisa Nombre, Dur, Lleg, MB, Q.")

    def _agregar_random(self):
        n = f"Proceso {int(random.random()*10000)}"
        d = random.randint(2, 12)
        l = self.plan.t
        m = random.choice([32,48,64,96,128])
        q = random.randint(2,5) if self.plan.alg.__class__.__name__ == "RR" else None
        p = Proceso(n, d, l, memoria=m, quantum=q)
        self.plan.agregar(p)
        self.plan.ingresar_llegadas()
        self._refresh_all()

    # ---------- Loop ----------
    def _loop(self):
        if not self.sim_activa:
            self._loop_job = None; return
        self.plan.tick()
        self._refresh_all()
        self._loop_job = self.after(self.tick_ms, self._loop)

    # ---------- UI Refresh ----------
    def _refresh_all(self):
        def fill(tv, rows):
            tv.delete(*tv.get_children())
            for r in rows: tv.insert("", "end", values=r)

        pend = [(p.pid, p.nombre, p.memoria, p.duracion, p.restante, p.llegada) for p in self.plan.snap_pend()]
        fill(self.tv_pend, pend)

        ready = [(p.pid, p.nombre, (p.quantum if p.quantum is not None else "-"), p.memoria, p.duracion, p.restante, p.llegada) for p in self.plan.snap_ready()]
        fill(self.tv_list, ready)

        cpu_rows = []
        c = self.plan.snap_cpu()
        if c: cpu_rows.append((c.pid, c.nombre, (c.quantum if c.quantum is not None else "-"), c.memoria, c.restante, c.llegada))
        fill(self.tv_cpu, cpu_rows)

        esp = [(p.pid, p.nombre, p.memoria, p.duracion, p.restante, p.llegada) for p in self.plan.snap_espera()]
        fill(self.tv_esp, esp)

        fin = [(p.pid, p.nombre, p.duracion, p.llegada, p.fin) for p in self.plan.snap_final()]
        fill(self.tv_fin, fin)

        hist = [(t, tipo, pid, nombre, alg, rest) for (_, t, tipo, pid, nombre, alg, rest) in self.plan.snap_ev()]
        fill(self.tv_hist, hist)

        self.var_info.set(f"t={self.plan.t}  |  RAM: {self.plan.mem_uso}/{self.plan.mem_total} MB")
        try: self.update_idletasks()
        except Exception: pass
