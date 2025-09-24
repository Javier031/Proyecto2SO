import heapq
from .base import Estrategia

class SJF(Estrategia):
    """
    SJF no expropiativo con llegadas:
    - Entre los procesos que YA llegaron, elige el de menor duración (CPU).
    - Empates: primero por llegada (menor t0), luego por orden de inserción.
    """
    def __init__(self, qdef=2):
        super().__init__(qdef)
        self.ready = []
        self._ord = 0  # para desempate estable

    def add(self, p):
        self._ord += 1
        # ⚠️ CLAVE: duración primero, luego llegada, luego orden de alta
        heapq.heappush(self.ready, (p.duracion, p.llegada, self._ord, p))

    def elegir(self, actual):
        # No expropiativo: si hay proceso en CPU, continúa
        if actual is not None:
            return actual
        # CPU libre: toma el de menor duración de los que YA llegaron (el Planificador garantiza esto)
        if self.ready:
            return heapq.heappop(self.ready)[3]
        return None

    def pre_tick(self, actual):
        pass

    def post_tick(self, actual):
        # Termina cuando restante llega a 0; nunca hay expropiación en SJF
        return (actual.terminado, False)

    def reinsertar(self, p):
        # En SJF no debería llamarse, pero lo dejamos seguro
        self.add(p)

    def peek_ready(self):
        return [t[3] for t in self.ready]

    def dump_ready(self):
        out = [t[3] for t in self.ready]
        self.ready.clear()
        return out
