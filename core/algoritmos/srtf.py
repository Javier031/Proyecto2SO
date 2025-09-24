import heapq
from .base import Estrategia

class SRTF(Estrategia):
    def __init__(self, qdef=2):
        super().__init__(qdef); self.ready = []; self._ord = 0

    def add(self, p):
        self._ord += 1
        # prioridad: llegada (menor primero), luego restante, luego orden
        heapq.heappush(self.ready, (p.llegada, p.restante, self._ord, p))

    def elegir(self, actual):
        # si no hay actual, toma el mejor de la cola
        if actual is None:
            if self.ready: return heapq.heappop(self.ready)[3]
            return None
        # si hay candidato con menor restante (y llegó), preempta
        if self.ready:
            _, best_rest, _, best = self.ready[0]
            if best_rest < actual.restante:
                self.add(actual)
                return heapq.heappop(self.ready)[3]
        return actual

    def pre_tick(self, actual): pass

    def post_tick(self, actual):
        if actual.terminado: return (True, False)
        return (False, False)

    def reinsertar(self, p): self.add(p)

    def peek_ready(self): return [t[3] for t in self.ready]

    def dump_ready(self): out = [t[3] for t in self.ready]; self.ready.clear(); return out
