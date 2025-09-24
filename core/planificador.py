from core.algoritmos.fcfs import FCFS
from core.algoritmos.sjf import SJF
from core.algoritmos.srtf import SRTF
from core.algoritmos.rr import RR

ALGS = {"FCFS": FCFS, "SJF": SJF, "SRTF": SRTF, "RR": RR}

class Planificador:
    def __init__(self, algoritmo="FCFS", quantum_defecto=2, memoria_total=1024):
        self.t = 0
        self.mem_total = int(memoria_total)
        self.mem_uso = 0
        self.cpu = None
        self.finalizados = []
        self.espera_mem = []     # llegaron pero no caben
        self.pendientes = []     # llegada futura
        self.eventos = []        # (id, t, tipo, pid, nombre, alg, rest)
        self._eid = 0
        self.q_def = int(quantum_defecto)
        self.set_algoritmo(algoritmo)

    # ---- eventos ----
    def _alg_name(self): return self.alg.__class__.__name__
    def _log(self, tipo, p):
        self._eid += 1
        self.eventos.append((self._eid, self.t, tipo, p.pid, p.nombre, self._alg_name(), p.restante))

    # ---- API ----
    def set_algoritmo(self, nombre):
        cls = ALGS.get(nombre.upper(), FCFS)
        ready = getattr(self, "alg", None).dump_ready() if hasattr(self, "alg") else []
        self.alg = cls(self.q_def)
        for p in ready: self.alg.add(p)

    def agregar(self, p):
        if p.llegada > self.t:
            self.pendientes.append(p)
            self.pendientes.sort(key=lambda x: (x.llegada, x.pid))
        else:
            self._subir_mem_o_espera(p)

    def _subir_mem_o_espera(self, p):
        if self.mem_uso + p.memoria <= self.mem_total:
            self.mem_uso += p.memoria
            self.alg.add(p); self._log("ALTA", p)
        else:
            self.espera_mem.append(p)

    def ingresar_llegadas(self):
        i = 0
        while i < len(self.pendientes):
            p = self.pendientes[i]
            if p.llegada <= self.t:
                self._subir_mem_o_espera(p); self.pendientes.pop(i)
            else:
                i += 1

    def _liberar_mem(self, p):
        self.mem_uso = max(0, self.mem_uso - p.memoria)
        i = 0
        while i < len(self.espera_mem):
            q = self.espera_mem[i]
            if self.mem_uso + q.memoria <= self.mem_total:
                self.mem_uso += q.memoria
                self.alg.add(q); self.espera_mem.pop(i); self._log("ALTA", q)
            else:
                i += 1

    def tick(self):
        # avanzar reloj
        self.t += 1
        # ingresos que ya tocaron
        self.ingresar_llegadas()
        # elegir en CPU
        self.cpu = self.alg.elegir(self.cpu)
        # log de entrada a CPU
        if self.cpu and getattr(self, "_last_pid", None) != self.cpu.pid:
            self._log("EJEC", self.cpu); self._last_pid = self.cpu.pid
        # si no hay nadie, termina tick
        if self.cpu is None: return
        # ejecutar un tick
        self.alg.pre_tick(self.cpu)
        self.cpu.tick(1)
        fin, preem = self.alg.post_tick(self.cpu)
        if fin:
            self.cpu.fin = self.t
            self.finalizados.append(self.cpu); self._log("FIN", self.cpu)
            self._liberar_mem(self.cpu)
            self.cpu = None; self._last_pid = None
        elif preem:
            self._log("PREEM", self.cpu)
            self.alg.reinsertar(self.cpu)
            self.cpu = None; self._last_pid = None

    # snapshots
    def snap_ready(self): return self.alg.peek_ready()
    def snap_cpu(self): return self.cpu
    def snap_final(self): return list(self.finalizados)
    def snap_espera(self): return list(self.espera_mem)
    def snap_pend(self): return list(self.pendientes)
    def snap_ev(self): return list(self.eventos)
