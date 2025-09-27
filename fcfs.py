<<<<<<< HEAD
from .base import AlgoritmoPlanificacion

class FCFS(AlgoritmoPlanificacion):
    def ejecutar(self):
        tiempo = 0
        resultados = []

        for proceso in sorted(self.procesos, key=lambda x: x.llegada):
            if tiempo < proceso.llegada:
                tiempo = proceso.llegada
            inicio = tiempo
            fin = inicio + proceso.duracion
            tiempo = fin
            resultados.append((proceso.nombre, inicio, fin))

        return resultados
_ready(self): return []
=======
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
>>>>>>> e92bb34283695cde380f553dbf0bddab51de6225
