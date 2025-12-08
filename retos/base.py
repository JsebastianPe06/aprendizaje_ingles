"""
Clase base abstracta para todos los retos del sistema.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional

class RetoBase(ABC):
    """
    Clase base para todos los tipos de retos.
    Define la interfaz común que deben implementar todos los retos.
    """
    
    def __init__(self, palabra_objetivo: str, nivel_dificultad: str = "intermedio"):
        """
        Inicializa un reto.
        
        :param palabra_objetivo: Palabra principal que se está practicando
        :param nivel_dificultad: 'basico', 'intermedio', 'avanzado'
        """
        self.palabra_objetivo = palabra_objetivo
        self.nivel_dificultad = nivel_dificultad
        self.tiempo_inicio = None
        self.tiempo_fin = None
        self.intentos = 0
        self.max_intentos = 3
        self.completado = False
        self.puntaje = 0
        
    @abstractmethod
    def generar(self) -> Dict[str, Any]:
        """
        Genera el contenido del reto.
        Debe retornar un diccionario con toda la información necesaria
        para presentar el reto al usuario.
        """
        pass
    
    @abstractmethod
    def verificar(self, respuesta: Any) -> Dict[str, Any]:
        """
        Verifica si la respuesta del usuario es correcta.
        
        :param respuesta: Respuesta del usuario (puede ser str, list, dict, etc.)
        :return: Diccionario con resultado de la verificación
        """
        pass
    
    def iniciar(self):
        """Marca el inicio del reto."""
        self.tiempo_inicio = datetime.now()
        self.intentos = 0
        self.completado = False
        
    def finalizar(self):
        """Marca el fin del reto."""
        self.tiempo_fin = datetime.now()
        self.completado = True
        
    def obtener_tiempo_respuesta(self) -> float:
        """Retorna el tiempo en segundos que tomó completar el reto."""
        if self.tiempo_inicio and self.tiempo_fin:
            delta = self.tiempo_fin - self.tiempo_inicio
            return delta.total_seconds()
        return 0.0
    
    def calcular_quality(self, correcto: bool, tiempo_segundos: float = None) -> int:
        """
        Calcula el quality (0-5) para el motor SRS basado en el rendimiento.
        
        :param correcto: Si la respuesta fue correcta
        :param tiempo_segundos: Tiempo que tomó responder
        :return: Quality entre 0-5
        """
        if not correcto:
            # Incorrecto: quality basado en número de intentos
            if self.intentos == 1:
                return 2  # Primer intento fallido
            elif self.intentos == 2:
                return 1  # Segundo intento fallido
            else:
                return 0  # Múltiples intentos fallidos
        
        # Correcto: quality basado en tiempo y intentos
        if self.intentos == 1:
            # Primer intento correcto
            if tiempo_segundos is None:
                return 5
            elif tiempo_segundos < 5:
                return 5  # Muy rápido
            elif tiempo_segundos < 10:
                return 4  # Rápido
            else:
                return 3  # Lento pero correcto
        elif self.intentos == 2:
            return 3  # Segundo intento correcto
        else:
            return 3  # Múltiples intentos pero eventualmente correcto
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Retorna estadísticas del reto."""
        return {
            'palabra_objetivo': self.palabra_objetivo,
            'nivel': self.nivel_dificultad,
            'intentos': self.intentos,
            'completado': self.completado,
            'tiempo_respuesta': self.obtener_tiempo_respuesta(),
            'puntaje': self.puntaje
        }