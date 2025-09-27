from .base import Estrategia

class SJF(Estrategia):
    """
    Algoritmo de planificación SJF (Shortest Job First) - No expropiativo.
    Selecciona siempre el proceso con el menor tiempo de CPU de la cola de listos.
    """

    def __init__(self, qdef=2):
        super().__init__(qdef)
        self.ready_queue = []  # Cola de procesos listos

    def add(self, p):
        """
        Agregar un proceso a la cola de listos.
        """
        self.ready_queue.append(p)
        # Ordenamos por tiempo de CPU requerido (menor primero)
        self.ready_queue.sort(key=lambda x: x.tiempo_cpu)

    def elegir(self, actual):
        """
        Elegir el siguiente proceso a ejecutar.
        Retorna el proceso con menor tiempo de CPU de la cola.
        """
        if self.ready_queue:
            return self.ready_queue.pop(0)
        return None

    def pre_tick(self, actual):
        """
        Operaciones antes de cada tick de CPU.
        Para SJF no expropiativo no es necesario nada especial aquí.
        """
        pass

    def post_tick(self, actual):
        """
        Operaciones después de cada tick de CPU.
        Para SJF no expropiativo no se requiere lógica adicional.
        """
        pass

    def reinsertar(self, p):
        """
        Reinsertar un proceso a la cola de listos.
        (Si aún no terminó o debe volver a esperar).
        """
        self.add(p)

    def peek_ready(self):
        """
        Ver la cola de listos sin modificarla.
        """
        return list(self.ready_queue)

    def dump_ready(self):
        """
        Vaciar la cola y devolver los procesos.
        """
        procesos = list(self.ready_queue)
        self.ready_queue.clear()
        return procesos
