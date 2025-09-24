from .base import Estrategia

class FCFS(Estrategia):
    """
    Stub: pendiente de implementar por el equipo.
    Se lanza un error al instanciar para que falle al seleccionar el algoritmo.
    """
    def __init__(self, qdef=2):
        super().__init__(qdef)
        raise NotImplementedError(
            "FCFS pendiente de implementar por el equipo. HACE FALTA EL ALGORITMO FCFS "
            "Completa core/algoritmos/fcfs.py"
        )

    # Métodos “placeholder” (nunca se llamarán porque __init__ ya falla)
    def add(self, p): ...
    def elegir(self, actual): ...
    def pre_tick(self, actual): ...
    def post_tick(self, actual): ...
    def reinsertar(self, p): ...
    def peek_ready(self): return []
    def dump_ready(self): return []
