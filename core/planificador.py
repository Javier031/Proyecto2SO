from core.algoritmos.fcfs import FCFS
from core.algoritmos.sjf import SJF
from core.algoritmos.srtf import SRTF
from core.algoritmos.rr import RR

ALGS = {"FCFS": FCFS, "SJF": SJF, "SRTF": SRTF, "RR": RR}


class Planificador:
    """
    Motor de simulación con 1 CPU y memoria finita.
    Mantiene:
      - t: tiempo actual (ticks)
      - mem_total / mem_uso
      - cpu: proceso en ejecución (o None)
      - finalizados, espera_mem, pendientes (llegada futura)
      - eventos: lista de (id, t, tipo, pid, nombre, alg, restante)
    Reglas clave:
      - En cada tick, PRIMERO se consideran llegadas con llegada <= t.
      - Se elige el proceso con t actual (SJF no ve llegadas en t+1).
      - Se ejecuta 1 unidad y LUEGO se incrementa t.
    """
    def __init__(self, algoritmo="FCFS", quantum_defecto=2, memoria_total=1024):
        self.t = 0
        self.mem_total = int(memoria_total)
        self.mem_uso = 0

        self.cpu = None
        self.finalizados = []
        self.espera_mem = []   # llegaron pero no caben en RAM
        self.pendientes = []   # llegada futura

        self.eventos = []      # (id, t, tipo, pid, nombre, alg, restante)
        self._eid = 0
        self._last_pid = None

        self.q_def = int(quantum_defecto)
        self.set_algoritmo(algoritmo)

    # ------------------ utilidades internas ------------------

    def _alg_name(self):
        return self.alg.__class__.__name__

    def _log(self, tipo, p):
        """Agrega un evento al historial."""
        self._eid += 1
        self.eventos.append((self._eid, self.t, tipo, p.pid, p.nombre, self._alg_name(), p.restante))

    # ------------------ API pública ------------------

    def set_algoritmo(self, nombre):
        """Cambia la estrategia manteniendo la cola ready actual."""
        cls = ALGS.get(nombre.upper(), FCFS)
        ready = getattr(self, "alg", None).dump_ready() if hasattr(self, "alg") else []
        self.alg = cls(self.q_def)
        for p in ready:
            self.alg.add(p)

    def agregar(self, p):
        """Agrega un proceso al sistema (pendiente o listos/espera según llegada y RAM)."""
        if p.llegada > self.t:
            self.pendientes.append(p)
            self.pendientes.sort(key=lambda x: (x.llegada, x.pid))
        else:
            self._subir_mem_o_espera(p)

    def _subir_mem_o_espera(self, p):
        """Intenta subir a ready respetando RAM; si no cabe, queda en espera_mem."""
        if self.mem_uso + p.memoria <= self.mem_total:
            self.mem_uso += p.memoria
            self.alg.add(p)
            self._log("ALTA", p)
        else:
            self.espera_mem.append(p)

    def ingresar_llegadas(self):
        """Mete a ready todos los procesos con llegada <= t (sin avanzar reloj)."""
        i = 0
        while i < len(self.pendientes):
            p = self.pendientes[i]
            if p.llegada <= self.t:
                self._subir_mem_o_espera(p)
                self.pendientes.pop(i)
            else:
                i += 1

    def _liberar_mem(self, p):
        """Libera RAM del proceso p y sube desde espera_mem lo que quepa (en orden)."""
        self.mem_uso = max(0, self.mem_uso - p.memoria)
        i = 0
        while i < len(self.espera_mem):
            q = self.espera_mem[i]
            if self.mem_uso + q.memoria <= self.mem_total:
                self.mem_uso += q.memoria
                self.alg.add(q)
                self.espera_mem.pop(i)
                self._log("ALTA", q)
            else:
                i += 1

    # ------------------ ciclo de simulación ------------------

    def tick(self):
        """
        Avanza la simulación un tick.

        Orden correcto:
          1) Con t actual, ingresar llegadas (llegada <= t)
          2) Elegir proceso (estrategia puede preemptar si aplica)
          3) Si hay CPU, ejecutar 1 unidad
          4) Incrementar t
          5) Evaluar FIN / PREEMPT
        Así, un proceso con llegada = t+1 NO compite todavía en la decisión actual.
        """
        # 1) Llegadas al tiempo actual
        self.ingresar_llegadas()

        # 2) Elegir a quién ejecutar con t actual
        self.cpu = self.alg.elegir(self.cpu)

        # Registrar entrada a CPU (cuando cambia)
        if self.cpu is not None and self._last_pid != self.cpu.pid:
            self._log("EJEC", self.cpu)
            self._last_pid = self.cpu.pid

        # Si no hay proceso, el tiempo igual avanza (CPU ociosa)
        if self.cpu is None:
            self.t += 1
            return

        # 3) Ejecutar 1 unidad
        self.alg.pre_tick(self.cpu)
        self.cpu.tick(1)

        # 4) Avanzar el reloj
        self.t += 1

        # 5) Evaluar fin o expropiación según estrategia
        terminado, preempt = self.alg.post_tick(self.cpu)
        if terminado:
            self.cpu.fin = self.t
            self.finalizados.append(self.cpu)
            self._log("FIN", self.cpu)
            self._liberar_mem(self.cpu)
            self.cpu = None
            self._last_pid = None
        elif preempt:
            self._log("PREEM", self.cpu)
            self.alg.reinsertar(self.cpu)
            self.cpu = None
            self._last_pid = None

    # ------------------ snapshots para la GUI ------------------

    def snap_ready(self):
        return self.alg.peek_ready()

    def snap_cpu(self):
        return self.cpu

    def snap_final(self):
        return list(self.finalizados)

    def snap_espera(self):
        return list(self.espera_mem)

    def snap_pend(self):
        return list(self.pendientes)

    def snap_ev(self):
        return list(self.eventos)
