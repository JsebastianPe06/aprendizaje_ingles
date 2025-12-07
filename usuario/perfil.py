"""
En este módulo se define solo al usuario y sus atributos
"""

class PerfilUsuario:
    """
    Clase representativa del usuario del programa
    """
    def __init__(self, nombre, nivel=0):
        self.nombre = nombre
        self.nivel = nivel  # entero del 0 al 100
