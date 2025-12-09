"""
Este archivo define clases y funciones base relacionadas con los retos del sistema de aprendizaje de inglés.
"""

class RetoBase:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def iniciar_reto(self):
        raise NotImplementedError("Este método debe ser implementado por subclases.")

    def obtener_resultado(self):
        raise NotImplementedError("Este método debe ser implementado por subclases.")