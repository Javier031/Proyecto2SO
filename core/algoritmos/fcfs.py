from collections import deque
from .base import Estrategia

class FCFS(Estrategia):
    def __init__(self, qdef=2):
        super().__init__(qdef); self.ready = deque()

    def add(self, p): self.ready.append(p)

    def elegir(self, actual):
        if actual: return actual
        if self.ready: return self.ready.popleft()
        return None

    def pre_tick(self, actual): pass

    def post_tick(self, actual):
        return (actual.terminado, False)

    def reinsertar(self, p): self.ready.append(p)

    def peek_ready(self): return list(self.ready)

    def dump_ready(self): out = list(self.ready); self.ready.clear(); return out
