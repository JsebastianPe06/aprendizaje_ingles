"""
Este archivo contiene funciones y clases para rastrear el progreso del usuario en el sistema de aprendizaje de inglés.
""" 

class Progreso:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.progreso = {}

    def registrar_progreso(self, leccion_id, estado):
        self.progreso[leccion_id] = estado

    def obtener_progreso(self):
        return self.progreso

    def resetear_progreso(self):
        self.progreso = {}