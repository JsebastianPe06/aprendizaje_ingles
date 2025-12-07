"""
Este módulo contiene la clase representativa de las estadísticas de los usuarios
"""

class EstadisticasUsuario:
    """
    Clase representativa de las estadísticas de un usuario
    """
    def __init__(self):
        self.aciertos = 0
        self.fallos = 0
        self.tiempos_respuesta = []
        self.palabras_dominadas = set()
        self.palabras_problematicas = set()
