"""
Este archivo contiene funciones para rastrear y analizar estadísticas de usuario en el sistema de aprendizaje de inglés.
"""

class EstadisticasUsuario:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.progreso = {}
        self.puntuaciones = []

    def agregar_progreso(self, ejercicio_id, resultado):
        if ejercicio_id not in self.progreso:
            self.progreso[ejercicio_id] = []
        self.progreso[ejercicio_id].append(resultado)

    def agregar_puntuacion(self, puntuacion):
        self.puntuaciones.append(puntuacion)

    def obtener_promedio_puntuacion(self):
        if not self.puntuaciones:
            return 0
        return sum(self.puntuaciones) / len(self.puntuaciones)

    def obtener_estadisticas(self):
        return {
            "usuario_id": self.usuario_id,
            "progreso": self.progreso,
            "promedio_puntuacion": self.obtener_promedio_puntuacion(),
        }