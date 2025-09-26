class Proceso:
    _seq = 0
    def __init__(self, nombre, duracion, llegada, memoria=64, quantum=None):
        Proceso._seq += 1
        self.pid = Proceso._seq
        self.nombre = nombre or f"Proceso {self.pid}"
        self.duracion = int(duracion)
        self.restante = int(duracion)
        self.llegada = int(llegada)
        self.memoria = int(memoria)
        self.quantum = int(quantum) if quantum is not None else None
        self.fin = None  # tiempo de finalización

    def tick(self, unidades=1):
        usado = min(unidades, self.restante)
        self.restante -= usado
        return usado

    @property
    def terminado(self):
        return self.restante <= 0

    def __repr__(self):
        return f"<P{self.pid} {self.nombre} dur={self.duracion} rest={self.restante} t0={self.llegada}>"
