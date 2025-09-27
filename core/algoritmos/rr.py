from collections import deque
from .base import Estrategia

class RR(Estrategia):
    def __init__(self, qdef=2):
        super().__init__(qdef); self.ready = deque(); self._qleft = 0

    def add(self, p):
        if p.quantum is None: p.quantum = self.qdef
        self.ready.append(p)

    def elegir(self, actual):
        if actual is None:
            if not self.ready: return None
            p = self.ready.popleft(); self._qleft = p.quantum; return p
        if self._qleft > 0: return actual
        self.ready.append(actual)
        if not self.ready: return None
        p = self.ready.popleft(); self._qleft = p.quantum; return p

    def pre_tick(self, actual):
        if self._qleft <= 0: self._qleft = actual.quantum
        self._qleft -= 1

    def post_tick(self, actual):
        if actual.terminado:
            self._qleft = 0; return (True, False)
        if self._qleft == 0: return (False, True)
        return (False, False)

    def reinsertar(self, p): self.ready.append(p)

    def peek_ready(self): return list(self.ready)

    def dump_ready(self): out = list(self.ready); self.ready.clear(); return out
