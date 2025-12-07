"""
Grafo que se construye DIRECTAMENTE desde el JSON, sin intermediarios.
"""

import json
import random
from typing import Dict, List, Set, Optional

class Grafo:
    """
    Grafo semántico construido DIRECTAMENTE desde el archivo JSON.
    Control total sobre los datos y estructura.
    """
    
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = {}
        self.grafo = {}  # palabra -> {palabras relacionadas}
        self.palabras_por_categoria = {}
        self.palabras_por_dominio = {}
        self.construido = False
        
        # Cargar JSON inmediatamente
        self._cargar_json()
    
    def _cargar_json(self):
        """Carga el JSON directamente desde el archivo."""
        print(f"Cargando JSON desde {self.json_path}...")
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        if 'palabras' not in self.data:
            raise ValueError("JSON debe tener clave 'palabras'")
        
        total = len(self.data['palabras'])
        print(f"✓ JSON cargado: {total} palabras")
    
    def construir(self):
        """Construye el grafo directamente desde los datos del JSON."""
        print("Construyendo grafo desde JSON...")
        
        # Inicializar estructuras
        self.grafo = {}
        self.palabras_por_categoria = {
            'sustantivo': [],
            'verbo': [],
            'adjetivo': [],
            'adverbio': []
        }
        
        self.palabras_por_dominio = {
            'education': {'sustantivo': [], 'verbo': [], 'adjetivo': []},
            'health': {'sustantivo': [], 'verbo': [], 'adjetivo': []},
            'work': {'sustantivo': [], 'verbo': [], 'adjetivo': []},
            'general': {'sustantivo': [], 'verbo': [], 'adjetivo': []}
        }
        
        # PRIMERO: Indexar todas las palabras
        palabras_list = list(self.data['palabras'].keys())
        
        for palabra in palabras_list:
            info = self.data['palabras'][palabra]
            
            # 1. Inicializar nodo en el grafo
            if palabra not in self.grafo:
                self.grafo[palabra] = set()
            
            # 2. Indexar por categoría gramatical
            categorias = info.get('categorias', [])
            for cat in categorias:
                if cat in self.palabras_por_categoria:
                    self.palabras_por_categoria[cat].append(palabra)
            
            # 3. Indexar por dominio semántico
            dominio = info.get('semantica', {}).get('dominio', 'general')
            if dominio in self.palabras_por_dominio:
                for cat in categorias:
                    if cat in ['sustantivo', 'verbo', 'adjetivo']:
                        self.palabras_por_dominio[dominio][cat].append(palabra)
        
        # SEGUNDO: Construir conexiones semánticas
        conexiones_totales = 0
        
        for palabra in palabras_list:
            info = self.data['palabras'][palabra]
            
            # Solo procesar palabras con semántica
            if 'semantica' not in info:
                continue
                
            semantica = info['semantica']
            relaciones = semantica.get('relaciones', {})
            
            # Asegurar entrada en el grafo
            if palabra not in self.grafo:
                self.grafo[palabra] = set()
            
            # 1. Conexiones por sinónimos (las más fuertes)
            sinonimos = relaciones.get('sinonimos', [])
            for sinonimo in sinonimos[:5]:  # Limitar a 5
                if sinonimo in self.data['palabras']:
                    self._agregar_conexion(palabra, sinonimo)
                    conexiones_totales += 1
            
            # 2. Conexiones por hiperónimos (relaciones jerárquicas)
            hiperonimos = relaciones.get('hypernyms', [])
            for hiperonimo in hiperonimos[:3]:  # Limitar a 3
                if hiperonimo in self.data['palabras']:
                    self._agregar_conexion(palabra, hiperonimo)
                    conexiones_totales += 1
            
            # 3. Conexiones por dominio compartido (mismo tema)
            dominio = semantica.get('dominio', 'general')
            if dominio in self.palabras_por_dominio:
                # Tomar algunas palabras del mismo dominio (misma categoría)
                categorias_palabra = info.get('categorias', [])
                for cat in categorias_palabra:
                    if cat in ['sustantivo', 'verbo', 'adjetivo']:
                        palabras_mismo_dominio = self.palabras_por_dominio[dominio][cat]
                        for otra in palabras_mismo_dominio[:10]:  # Limitar
                            if otra != palabra:
                                self._agregar_conexion(palabra, otra)
                                conexiones_totales += 1
        
        self.construido = True
        print(f"✓ Grafo construido desde JSON: {len(self.grafo)} nodos, {conexiones_totales} conexiones")
        
        # Mostrar estadísticas
        print("\n ESTADÍSTICAS DEL GRAFO:")
        print(f"  Sustantivos: {len(self.palabras_por_categoria['sustantivo'])}")
        print(f"  Verbos: {len(self.palabras_por_categoria['verbo'])}")
        print(f"  Adjetivos: {len(self.palabras_por_categoria['adjetivo'])}")
        print(f"  Adverbios: {len(self.palabras_por_categoria['adverbio'])}")
        
        for dominio in self.palabras_por_dominio:
            sust = len(self.palabras_por_dominio[dominio]['sustantivo'])
            verb = len(self.palabras_por_dominio[dominio]['verbo'])
            adj = len(self.palabras_por_dominio[dominio]['adjetivo'])
            print(f"  {dominio.capitalize()}: {sust}sust, {verb}verb, {adj}adj")
    
    def _agregar_conexion(self, palabra1: str, palabra2: str):
        """Agrega conexión bidireccional entre dos palabras."""
        if palabra1 not in self.grafo:
            self.grafo[palabra1] = set()
        if palabra2 not in self.grafo:
            self.grafo[palabra2] = set()
        
        self.grafo[palabra1].add(palabra2)
        self.grafo[palabra2].add(palabra1)
    
    def obtener_palabras_categoria(self, categoria: str, dominio: str = None) -> List[str]:
        """
        Obtiene palabras de una categoría específica, opcionalmente filtradas por dominio.
        """
        if categoria not in self.palabras_por_categoria:
            return []
        
        if dominio and dominio in self.palabras_por_dominio:
            # Filtrar por dominio
            if categoria in ['sustantivo', 'verbo', 'adjetivo']:
                return self.palabras_por_dominio[dominio][categoria]
        
        return self.palabras_por_categoria[categoria]
    
    def obtener_vecinos(self, palabra: str, max_vecinos: int = 10) -> List[str]:
        """Obtiene palabras relacionadas con la dada."""
        if not self.construido:
            self.construir()
        
        if palabra not in self.grafo:
            return []
        
        vecinos = list(self.grafo[palabra])
        random.shuffle(vecinos)
        return vecinos[:max_vecinos]
    
    def obtener_palabra_aleatoria(self, categoria: str = None, dominio: str = None) -> Optional[str]:
        """
        Obtiene una palabra aleatoria, filtrada por categoría y/o dominio.
        """
        if categoria and dominio:
            palabras = self.obtener_palabras_categoria(categoria, dominio)
        elif categoria:
            palabras = self.obtener_palabras_categoria(categoria)
        elif dominio:
            # Obtener todas las palabras del dominio
            if dominio in self.palabras_por_dominio:
                todas = []
                for cat in ['sustantivo', 'verbo', 'adjetivo']:
                    todas.extend(self.palabras_por_dominio[dominio][cat])
                palabras = list(set(todas))
            else:
                palabras = []
        else:
            # Todas las palabras
            palabras = list(self.grafo.keys())
        
        if not palabras:
            return None
        
        return random.choice(palabras)
    
    def verificar_categoria(self, palabra: str, categoria: str) -> bool:
        """Verifica si una palabra pertenece a cierta categoría."""
        if palabra not in self.data['palabras']:
            return False
        
        info = self.data['palabras'][palabra]
        categorias = info.get('categorias', [])
        return categoria in categorias
    
    def obtener_info(self, palabra: str) -> Optional[Dict]:
        """Obtiene información de una palabra directamente del JSON."""
        return self.data.get('palabras', {}).get(palabra.lower())