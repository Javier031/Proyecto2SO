import heapq
from .base import Estrategia

class SJF(Estrategia):
    def __init__(self, qdef=2):
        super().__init__(qdef); self.ready = []; self._ord = 0

    def add(self, p):
        self._ord += 1
        # prioridad: llegada (menor primero), luego duracion, luego orden de inserción
        heapq.heappush(self.ready, (p.llegada, p.duracion, self._ord, p))

    def elegir(self, actual):
        if actual: return actual  # no expropiativo
        if self.ready: return heapq.heappop(self.ready)[3]
        return None

    def pre_tick(self, actual): pass

    def post_tick(self, actual):
        return (actual.terminado, False)

    def reinsertar(self, p): self.add(p)

    def peek_ready(self): return [t[3] for t in self.ready]

    def dump_ready(self): out = [t[3] for t in self.ready]; self.ready.clear(); return out
