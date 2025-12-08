"""
Módulo de logging para el sistema de aprendizaje.
"""

import logging
import os
from datetime import datetime
from typing import Optional

class LoggerConfig:
    """
    Configuración y gestión de logs del sistema.
    """
    
    @staticmethod
    def configurar_logger(nombre: str = 'aprendizaje_ingles',
                        nivel: str = 'INFO',
                        archivo: bool = True,
                        consola: bool = True) -> logging.Logger:
        """
        Configura un logger para el sistema.
        
        :param nombre: Nombre del logger
        :param nivel: Nivel de logging ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        :param archivo: Si se debe guardar en archivo
        :param consola: Si se debe mostrar en consola
        :return: Logger configurado
        """
        logger = logging.getLogger(nombre)
        logger.setLevel(getattr(logging, nivel.upper()))
        
        # Evitar duplicar handlers
        if logger.handlers:
            return logger
        
        # Formato
        formato = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler de archivo
        if archivo:
            os.makedirs('logs', exist_ok=True)
            fecha = datetime.now().strftime('%Y%m%d')
            archivo_log = f'logs/{nombre}_{fecha}.log'
            
            file_handler = logging.FileHandler(archivo_log, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formato)
            logger.addHandler(file_handler)
        
        # Handler de consola
        if consola:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formato)
            logger.addHandler(console_handler)
        
        return logger


class AuditoriaUsuario:
    """
    Registra acciones importantes del usuario para análisis.
    """
    def __init__(self, usuario_id: str):
        """
        Inicializa el auditor.
        
        :param usuario_id: ID del usuario
        """
        self.usuario_id = usuario_id
        self.logger = LoggerConfig.configurar_logger(
            f'auditoria_{usuario_id}',
            nivel='INFO',
            archivo=True,
            consola=False
        )
    
    def registrar_inicio_sesion(self):
        """
        Registra el inicio de una sesión.
        """
        self.logger.info(f"Usuario {self.usuario_id} inició sesión")
    
    def registrar_fin_sesion(self, duracion: float, retos: int):
        """
        Registra el fin de una sesión.
        :param duracion: Duración en minutos
        :param retos: Número de retos completados
        """
        self.logger.info(
            f"Usuario {self.usuario_id} finalizó sesión: "
            f"{duracion:.1f} min, {retos} retos"
        )
    
    def registrar_reto(self, tipo: str, resultado: str, tiempo: float):
        """
        Registra un reto completado.

        :param tipo: Tipo de reto
        :param resultado: 'correcto' o 'incorrecto'
        :param tiempo: Tiempo en segundos
        """
        self.logger.info(
            f"Reto {tipo}: {resultado} en {tiempo:.1f}s"
        )
    
    def registrar_subida_nivel(self, nivel_anterior: int, nivel_nuevo: int):
        """
        Registra una subida de nivel.
        
        :param nivel_anterior: Nivel anterior
        :param nivel_nuevo: Nivel nuevo
        """
        self.logger.info(
            f"¡SUBIDA DE NIVEL! {nivel_anterior} → {nivel_nuevo}"
        )
    
    def registrar_logro(self, logro: str):
        """
        Registra un logro desbloqueado.
        
        :param logro: Nombre del logro
        """
        self.logger.info(f"¡LOGRO DESBLOQUEADO! {logro}")
    
    def registrar_error(self, mensaje: str, excepcion: Optional[Exception] = None):
        """
        Registra un error.
        
        :param mensaje: Mensaje de error
        :param excepcion: Excepción si existe
        """
        if excepcion:
            self.logger.error(f"{mensaje}: {str(excepcion)}", exc_info=True)
        else:
            self.logger.error(mensaje)


class EstadisticasSesion:
    """
    Rastrea estadísticas de una sesión individual.
    """
    
    def __init__(self):
        """Inicializa el rastreador de sesión."""
        self.inicio = datetime.now()
        self.retos_completados = 0
        self.retos_correctos = 0
        self.retos_incorrectos = 0
        self.tiempo_total = 0.0
        self.palabras_practicadas = set()
        self.tipos_reto = []
    
    def registrar_reto(self, correcto: bool, tiempo: float, 
        palabra: str, tipo: str):
        """
        Registra un reto completado.
        
        :param correcto: Si fue correcto
        :param tiempo: Tiempo en segundos
        :param palabra: Palabra practicada
        :param tipo: Tipo de reto
        """
        self.retos_completados += 1
        
        if correcto:
            self.retos_correctos += 1
        else:
            self.retos_incorrectos += 1
        
        self.tiempo_total += tiempo
        self.palabras_practicadas.add(palabra)
        self.tipos_reto.append(tipo)
    
    def obtener_duracion(self) -> float:
        """
        Obtiene la duración de la sesión en minutos.
        """
        delta = datetime.now() - self.inicio
        return delta.total_seconds() / 60
    
    def obtener_precision(self) -> float:
        """
        Obtiene la precisión de la sesión.
        """
        if self.retos_completados == 0:
            return 0.0
        return (self.retos_correctos / self.retos_completados) * 100
    
    def obtener_resumen(self) -> dict:
        """Obtiene un resumen de la sesión."""
        return {
            'duracion': self.obtener_duracion(),
            'retos_completados': self.retos_completados,
            'retos_correctos': self.retos_correctos,
            'retos_incorrectos': self.retos_incorrectos,
            'precision': self.obtener_precision(),
            'tiempo_promedio': (
                self.tiempo_total / self.retos_completados 
                if self.retos_completados > 0 else 0
            ),
            'palabras_unicas': len(self.palabras_practicadas),
            'tipos_practicados': len(set(self.tipos_reto))
        }
    
    def imprimir_resumen(self):
        """Imprime un resumen formateado de la sesión."""
        resumen = self.obtener_resumen()
        
        print("\n" + "=" * 50)
        print("  RESUMEN DE LA SESIÓN")
        print("=" * 50)
        print(f"  Duración: {resumen['duracion']:.1f} minutos")
        print(f" Retos completados: {resumen['retos_completados']}")
        print(f" Correctos: {resumen['retos_correctos']}")
        print(f" Incorrectos: {resumen['retos_incorrectos']}")
        print(f" Precisión: {resumen['precision']:.1f}%")
        print(f" Palabras únicas: {resumen['palabras_unicas']}")
        print(f" Tiempo promedio: {resumen['tiempo_promedio']:.1f}s por reto")
        print("=" * 50)