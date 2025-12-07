"""
Clase representativa del progreso de un usuario, une tanto el usuario como a sus
estadísticas en una sola clase y permite guardar y carga la información
"""

import json

from estadistica import *
from perfil import *

class Progreso:
    """
    Clase representativa del progreso de un usuario por medio de sus estadísticas
    """
    def __init__(self, perfil:PerfilUsuario, estadisticas:EstadisticasUsuario):
        self.perfil = perfil
        self.estadisticas = estadisticas

    def guardar(self):
        """
        guarda la información del usuario en un json
        """
        pass

    def cargar(self):
        """
        Carga la información del usuario de un json
        """
        pass

    def calculo_progreso(self):
        """
        Toma estadísticas del usuario y recalcula el su avance
        """
        pass