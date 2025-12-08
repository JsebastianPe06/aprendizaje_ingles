"""
Módulo de seguimiento de progreso del usuario.
Rastrea el avance en palabras individuales y categorías.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

class SeguimientoProgreso:
    """
    Rastrea el progreso detallado del usuario:
    - Palabras aprendidas y su nivel de dominio
    - Progreso por categorías/temas
    - Historial de sesiones
    - Análisis de fortalezas y debilidades
    """
    
    def __init__(self, usuario_id: str):
        """
        Inicializa el seguimiento de progreso.
        
        :param usuario_id: ID del usuario
        """
        self.usuario_id = usuario_id
        
        # Palabras y su estado
        self.palabras = {}  # palabra -> estado detallado
        
        # Progreso por categoría
        self.progreso_categorias = {
            'sustantivo': {'total': 0, 'aprendidas': 0, 'dominadas': 0},
            'verbo': {'total': 0, 'aprendidas': 0, 'dominadas': 0},
            'adjetivo': {'total': 0, 'aprendidas': 0, 'dominadas': 0},
            'adverbio': {'total': 0, 'aprendidas': 0, 'dominadas': 0}
        }
        
        # Progreso por dominio semántico
        self.progreso_dominios = {
            'education': {'aprendidas': 0, 'dominadas': 0},
            'health': {'aprendidas': 0, 'dominadas': 0},
            'work': {'aprendidas': 0, 'dominadas': 0},
            'general': {'aprendidas': 0, 'dominadas': 0}
        }
        
        # Historial de sesiones
        self.historial_sesiones = []
        
        # Análisis de rendimiento
        self.rendimiento = {
            'fortalezas': [],  # tipos de reto donde destaca
            'debilidades': [],  # tipos de reto a mejorar
            'palabras_dificiles': [],  # palabras con más errores
            'palabras_faciles': []  # palabras dominadas rápidamente
        }
    
    def registrar_palabra(self, palabra: str, categoria: str = None, 
                         dominio: str = None):
        """
        Registra una palabra nueva en el sistema.
        
        :param palabra: Palabra a registrar
        :param categoria: Categoría gramatical
        :param dominio: Dominio semántico
        """
        if palabra not in self.palabras:
            self.palabras[palabra] = {
                'primera_vez': datetime.now().isoformat(),
                'ultima_practica': None,
                'veces_practicada': 0,
                'veces_correcta': 0,
                'veces_incorrecta': 0,
                'nivel_dominio': 0,  # 0-100
                'estado': 'nuevo',  # nuevo, aprendiendo, aprendido, dominado
                'categoria': categoria,
                'dominio': dominio,
                'tiempo_promedio': 0.0,
                'racha_correctas': 0,
                'historial': []
            }
    
    def actualizar_palabra(self, palabra: str, correcto: bool, 
                          tiempo_segundos: float = 0, quality: int = 3):
        """
        Actualiza el estado de una palabra después de practicarla.
        
        :param palabra: Palabra practicada
        :param correcto: Si la respuesta fue correcta
        :param tiempo_segundos: Tiempo que tomó responder
        :param quality: Calidad de la respuesta (0-5)
        """
        if palabra not in self.palabras:
            self.registrar_palabra(palabra)
        
        estado = self.palabras[palabra]
        estado['veces_practicada'] += 1
        estado['ultima_practica'] = datetime.now().isoformat()
        
        if correcto:
            estado['veces_correcta'] += 1
            estado['racha_correctas'] += 1
        else:
            estado['veces_incorrecta'] += 1
            estado['racha_correctas'] = 0
        
        # Actualizar tiempo promedio
        total = estado['veces_practicada']
        estado['tiempo_promedio'] = (
            (estado['tiempo_promedio'] * (total - 1) + tiempo_segundos) / total
        )
        
        # Actualizar nivel de dominio
        self._actualizar_nivel_dominio(palabra, quality)
        
        # Registrar en historial
        estado['historial'].append({
            'fecha': datetime.now().isoformat(),
            'correcto': correcto,
            'tiempo': tiempo_segundos,
            'quality': quality
        })
        
        # Limitar historial a últimos 20 registros
        if len(estado['historial']) > 20:
            estado['historial'] = estado['historial'][-20:]
    
    def _actualizar_nivel_dominio(self, palabra: str, quality: int):
        """
        Actualiza el nivel de dominio de una palabra.
        
        :param palabra: Palabra a actualizar
        :param quality: Calidad de la última respuesta (0-5)
        """
        estado = self.palabras[palabra]
        
        # Calcular precisión
        total = estado['veces_practicada']
        if total == 0:
            return
        
        precision = (estado['veces_correcta'] / total) * 100
        
        # Calcular nivel de dominio (0-100)
        # Considera: precisión, número de prácticas, quality, racha
        nivel = (
            precision * 0.4 +  # 40% precisión
            min(total * 5, 30) +  # 30% práctica (máx 6 prácticas)
            quality * 5 +  # 25% última quality
            min(estado['racha_correctas'] * 2, 5)  # 5% racha
        )
        
        estado['nivel_dominio'] = min(100, int(nivel))
        
        # Actualizar estado
        if estado['nivel_dominio'] >= 80:
            estado['estado'] = 'dominado'
        elif estado['nivel_dominio'] >= 50:
            estado['estado'] = 'aprendido'
        elif estado['nivel_dominio'] >= 20:
            estado['estado'] = 'aprendiendo'
        else:
            estado['estado'] = 'nuevo'
        
        # Actualizar contadores de categorías
        self._actualizar_progreso_categorias()
    
    def _actualizar_progreso_categorias(self):
        """Actualiza los contadores de progreso por categoría."""
        # Resetear contadores
        for cat in self.progreso_categorias:
            self.progreso_categorias[cat]['aprendidas'] = 0
            self.progreso_categorias[cat]['dominadas'] = 0
        
        for dominio in self.progreso_dominios:
            self.progreso_dominios[dominio]['aprendidas'] = 0
            self.progreso_dominios[dominio]['dominadas'] = 0
        
        # Contar
        for palabra, estado in self.palabras.items():
            categoria = estado.get('categoria')
            dominio = estado.get('dominio')
            
            if categoria and categoria in self.progreso_categorias:
                if estado['estado'] in ['aprendido', 'dominado']:
                    self.progreso_categorias[categoria]['aprendidas'] += 1
                if estado['estado'] == 'dominado':
                    self.progreso_categorias[categoria]['dominadas'] += 1
            
            if dominio and dominio in self.progreso_dominios:
                if estado['estado'] in ['aprendido', 'dominado']:
                    self.progreso_dominios[dominio]['aprendidas'] += 1
                if estado['estado'] == 'dominado':
                    self.progreso_dominios[dominio]['dominadas'] += 1
    
    def registrar_sesion(self, tipo_reto: str, retos_completados: int,
                        precision: float, duracion: float):
        """
        Registra una sesión de práctica.
        
        :param tipo_reto: Tipo de reto practicado
        :param retos_completados: Número de retos completados
        :param precision: Precisión promedio (0-100)
        :param duracion: Duración en minutos
        """
        self.historial_sesiones.append({
            'fecha': datetime.now().isoformat(),
            'tipo_reto': tipo_reto,
            'retos_completados': retos_completados,
            'precision': precision,
            'duracion': duracion
        })
        
        # Limitar historial a últimas 50 sesiones
        if len(self.historial_sesiones) > 50:
            self.historial_sesiones = self.historial_sesiones[-50:]
        
        # Actualizar análisis de rendimiento
        self._analizar_rendimiento()
    
    def _analizar_rendimiento(self):
        """Analiza el rendimiento para identificar fortalezas y debilidades."""
        # Analizar por tipo de reto
        rendimiento_por_tipo = defaultdict(lambda: {'total': 0, 'precision': []})
        
        for sesion in self.historial_sesiones[-20:]:  # Últimas 20 sesiones
            tipo = sesion['tipo_reto']
            rendimiento_por_tipo[tipo]['total'] += 1
            rendimiento_por_tipo[tipo]['precision'].append(sesion['precision'])
        
        # Identificar fortalezas (precisión > 80%)
        self.rendimiento['fortalezas'] = []
        self.rendimiento['debilidades'] = []
        
        for tipo, datos in rendimiento_por_tipo.items():
            if datos['precision']:
                promedio = sum(datos['precision']) / len(datos['precision'])
                if promedio >= 80:
                    self.rendimiento['fortalezas'].append({
                        'tipo': tipo,
                        'precision': promedio
                    })
                elif promedio < 60:
                    self.rendimiento['debilidades'].append({
                        'tipo': tipo,
                        'precision': promedio
                    })
        
        # Identificar palabras difíciles (< 50% precisión, > 3 prácticas)
        palabras_dificiles = []
        palabras_faciles = []
        
        for palabra, estado in self.palabras.items():
            if estado['veces_practicada'] >= 3:
                precision = (estado['veces_correcta'] / estado['veces_practicada']) * 100
                
                if precision < 50:
                    palabras_dificiles.append({
                        'palabra': palabra,
                        'precision': precision,
                        'practicas': estado['veces_practicada']
                    })
                elif precision >= 90 and estado['estado'] == 'dominado':
                    palabras_faciles.append({
                        'palabra': palabra,
                        'precision': precision
                    })
        
        # Ordenar y limitar
        palabras_dificiles.sort(key=lambda x: x['precision'])
        palabras_faciles.sort(key=lambda x: x['precision'], reverse=True)
        
        self.rendimiento['palabras_dificiles'] = palabras_dificiles[:10]
        self.rendimiento['palabras_faciles'] = palabras_faciles[:10]
    
    def obtener_palabras_por_estado(self, estado: str) -> List[str]:
        """
        Obtiene lista de palabras en un estado específico.
        
        :param estado: 'nuevo', 'aprendiendo', 'aprendido', 'dominado'
        :return: Lista de palabras
        """
        return [p for p, e in self.palabras.items() if e['estado'] == estado]
    
    def obtener_palabras_debiles(self, limite: int = 10) -> List[str]:
        """
        Obtiene las palabras que necesitan más práctica.
        
        :param limite: Número máximo de palabras
        :return: Lista de palabras ordenadas por necesidad de práctica
        """
        palabras_debiles = []
        
        for palabra, estado in self.palabras.items():
            if estado['veces_practicada'] > 0:
                precision = (estado['veces_correcta'] / estado['veces_practicada']) * 100
                
                # Calcular puntuación de necesidad (menor = más necesaria)
                necesidad = (
                    100 - precision +  # Baja precisión
                    (100 - estado['nivel_dominio']) * 0.5 +  # Bajo dominio
                    max(0, 7 - estado['veces_practicada']) * 5  # Pocas prácticas
                )
                
                palabras_debiles.append({
                    'palabra': palabra,
                    'necesidad': necesidad,
                    'precision': precision
                })
        
        # Ordenar por necesidad (descendente)
        palabras_debiles.sort(key=lambda x: x['necesidad'], reverse=True)
        
        return [p['palabra'] for p in palabras_debiles[:limite]]
    
    def obtener_estadisticas_generales(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales del progreso."""
        total_palabras = len(self.palabras)
        
        if total_palabras == 0:
            return {
                'total_palabras': 0,
                'palabras_aprendidas': 0,
                'palabras_dominadas': 0,
                'precision_promedio': 0.0,
                'tiempo_promedio': 0.0
            }
        
        aprendidas = len([p for p, e in self.palabras.items() 
                         if e['estado'] in ['aprendido', 'dominado']])
        dominadas = len([p for p, e in self.palabras.items() 
                        if e['estado'] == 'dominado'])
        
        # Calcular precisión promedio
        total_intentos = sum(e['veces_practicada'] for e in self.palabras.values())
        total_correctos = sum(e['veces_correcta'] for e in self.palabras.values())
        precision = (total_correctos / total_intentos * 100) if total_intentos > 0 else 0
        
        # Tiempo promedio
        tiempos = [e['tiempo_promedio'] for e in self.palabras.values() 
                  if e['tiempo_promedio'] > 0]
        tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
        
        return {
            'total_palabras': total_palabras,
            'palabras_aprendidas': aprendidas,
            'palabras_dominadas': dominadas,
            'precision_promedio': precision,
            'tiempo_promedio': tiempo_promedio,
            'progreso_categorias': self.progreso_categorias,
            'progreso_dominios': self.progreso_dominios
        }
    
    def guardar(self, directorio: str = "data/progreso"):
        """Guarda el progreso en un archivo JSON."""
        os.makedirs(directorio, exist_ok=True)
        filepath = os.path.join(directorio, f"{self.usuario_id}_progreso.json")
        
        data = {
            'usuario_id': self.usuario_id,
            'palabras': self.palabras,
            'progreso_categorias': self.progreso_categorias,
            'progreso_dominios': self.progreso_dominios,
            'historial_sesiones': self.historial_sesiones,
            'rendimiento': self.rendimiento
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def cargar(cls, usuario_id: str, directorio: str = "data/progreso"):
        """Carga el progreso desde un archivo JSON."""
        filepath = os.path.join(directorio, f"{usuario_id}_progreso.json")
        
        if not os.path.exists(filepath):
            return cls(usuario_id)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        progreso = cls(usuario_id)
        progreso.palabras = data.get('palabras', {})
        progreso.progreso_categorias = data.get('progreso_categorias', progreso.progreso_categorias)
        progreso.progreso_dominios = data.get('progreso_dominios', progreso.progreso_dominios)
        progreso.historial_sesiones = data.get('historial_sesiones', [])
        progreso.rendimiento = data.get('rendimiento', progreso.rendimiento)
        
        return progreso