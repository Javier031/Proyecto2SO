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
