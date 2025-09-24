from .base import Estrategia

class SJF(Estrategia):
    def __init__(self, qdef=2):
        super().__init__(qdef)
        raise NotImplementedError(
            "SJF pendiente de implementar por el equipo. HACE FALTA EL ALGORITMO SJF "
            "Completa core/algoritmos/sjf.py"
        )

    def add(self, p): ...
    def elegir(self, actual): ...
    def pre_tick(self, actual): ...
    def post_tick(self, actual): ...
    def reinsertar(self, p): ...
    def peek_ready(self): return []
    def dump_ready(self): return []
