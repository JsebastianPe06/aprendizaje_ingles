"""
Reto de tarjetas: asociar palabra en inglés con su significado/traducción.
VERSIÓN CORREGIDA para estructura JSON real
"""

import random
from typing import Dict, Any, List
from .base import RetoBase

class RetoTarjetas(RetoBase):
    """
    Reto tipo flashcard: mostrar una palabra y pedir que seleccione
    el significado correcto entre varias opciones.
    
    Variantes:
    - Inglés → Español (traducción)
    - Inglés → Definición en inglés
    - Palabra → Sinónimo
    """
    
    def __init__(self, palabra_objetivo: str, diccionario, 
                nivel_dificultad: str = "intermedio",
                tipo: str = "traduccion",
                num_opciones: int = 4):
        """
        :param palabra_objetivo: Palabra a practicar
        :param diccionario: Instancia de Diccionario
        :param nivel_dificultad: Dificultad del reto
        :param tipo: 'traduccion', 'definicion', 'sinonimo'
        :param num_opciones: Número de opciones a mostrar
        """
        super().__init__(palabra_objetivo, nivel_dificultad)
        self.diccionario = diccionario
        self.tipo = tipo
        self.num_opciones = num_opciones
        self.opciones = []
        self.respuesta_correcta = None
        self.indice_correcto = None
        
    def generar(self) -> Dict[str, Any]:
        """
        Genera el reto de tarjeta.
        """
        info = self.diccionario.obtener_info(self.palabra_objetivo)
        if not info:
            raise ValueError(f"Palabra '{self.palabra_objetivo}' no encontrada en diccionario")
        # Obtener respuesta correcta según tipo - ESTRUCTURA REAL DEL JSON
        if self.tipo == "traduccion":
            traducciones_es = info.get('traducciones', {}).get('es', [])
            self.respuesta_correcta = traducciones_es[0] if traducciones_es else 'Sin traducción'
        elif self.tipo == "definicion":
            definiciones = info.get('definiciones', [])
            if definiciones:
                self.respuesta_correcta = definiciones[0]
            else:
                # Fallback a traducción
                traducciones_es = info.get('traducciones', {}).get('es', [])
                self.respuesta_correcta = traducciones_es[0] if traducciones_es else 'Sin definición'
        elif self.tipo == "sinonimo":
            sinonimos = info.get('sinonimos', [])
            if sinonimos:
                self.respuesta_correcta = sinonimos[0]
            else:
                # Fallback a traducción
                traducciones_es = info.get('traducciones', {}).get('es', [])
                self.respuesta_correcta = traducciones_es[0] if traducciones_es else 'Sin sinónimo'
        # Generar opciones incorrectas (distractores)
        self.opciones = self._generar_distractores()
        # Insertar respuesta correcta en posición aleatoria
        self.indice_correcto = random.randint(0, len(self.opciones))
        self.opciones.insert(self.indice_correcto, self.respuesta_correcta)
        return {
            'tipo_reto': 'tarjetas',
            'tipo_tarjeta': self.tipo,
            'palabra': self.palabra_objetivo,
            'pregunta': self._generar_pregunta(),
            'opciones': self.opciones,
            'num_opciones': len(self.opciones)
        }
    
    def _generar_pregunta(self) -> str:
        """Genera el texto de la pregunta."""
        if self.tipo == "traduccion":
            return f"¿Qué significa '{self.palabra_objetivo}' en español?"
        elif self.tipo == "definicion":
            return f"¿Cuál es la definición de '{self.palabra_objetivo}'?"
        elif self.tipo == "sinonimo":
            return f"¿Cuál es un sinónimo de '{self.palabra_objetivo}'?"
        return f"¿Qué significa '{self.palabra_objetivo}'?"
    
    def _generar_distractores(self) -> List[str]:
        """Genera opciones incorrectas pero plausibles."""
        distractores = []
        info_objetivo = self.diccionario.obtener_info(self.palabra_objetivo)
        categoria = info_objetivo.get('categorias', ['general'])[0] if info_objetivo else 'general'
        # Obtener palabras de la misma categoría
        palabras_categoria = self.diccionario.palabras_por_categoria(categoria)
        # Filtrar la palabra objetivo
        palabras_candidatas = [p for p in palabras_categoria if p != self.palabra_objetivo]
        random.shuffle(palabras_candidatas)
        # Generar distractores
        for palabra in palabras_candidatas:
            if len(distractores) >= self.num_opciones - 1:
                break
            info = self.diccionario.obtener_info(palabra)
            if not info:
                continue
            if self.tipo == "traduccion":
                traducciones_es = info.get('traducciones', {}).get('es', [])
                distractor = traducciones_es[0] if traducciones_es else None
            elif self.tipo == "definicion":
                definiciones = info.get('definiciones', [])
                if definiciones:
                    distractor = definiciones[0]
                else:
                    traducciones_es = info.get('traducciones', {}).get('es', [])
                    distractor = traducciones_es[0] if traducciones_es else None
            elif self.tipo == "sinonimo":
                sinonimos = info.get('sinonimos', [])
                if sinonimos:
                    distractor = sinonimos[0]
                else:
                    traducciones_es = info.get('traducciones', {}).get('es', [])
                    distractor = traducciones_es[0] if traducciones_es else None
            if distractor and distractor != self.respuesta_correcta:
                distractores.append(distractor)
        # Si no hay suficientes distractores, agregar genéricos
        distractores_genericos = [
            "opción incorrecta A",
            "opción incorrecta B", 
            "opción incorrecta C"
        ]
        while len(distractores) < self.num_opciones - 1:
            distractores.append(distractores_genericos[len(distractores)])
        return distractores[:self.num_opciones - 1]
    
    def verificar(self, respuesta: Any) -> Dict[str, Any]:
        """
        Verifica la respuesta del usuario.
        
        :param respuesta: Puede ser el índice (0-3) o el texto de la opción
        :return: Diccionario con resultado
        """
        self.intentos += 1
        correcto = False
        mensaje = ""
        # Convertir respuesta a índice si es necesario
        if isinstance(respuesta, str):
            try:
                # Si es número como string
                respuesta = int(respuesta)
            except ValueError:
                # Si es el texto de la opción
                if respuesta in self.opciones:
                    respuesta = self.opciones.index(respuesta)
                else:
                    return {
                        'correcto': False,
                        'mensaje': 'Respuesta no válida',
                        'quality': 0,
                        'completado': False
                    }
        # Verificar si es correcto
        if respuesta == self.indice_correcto:
            correcto = True
            self.puntaje = 100
            mensaje = "¡Correcto!"
            self.finalizar()
        else:
            self.puntaje = max(0, 100 - (self.intentos * 30))
            if self.intentos >= self.max_intentos:
                mensaje = f"Incorrecto. La respuesta era: {self.respuesta_correcta}"
                self.finalizar()
            else:
                mensaje = f"Incorrecto. Intento {self.intentos}/{self.max_intentos}"
        # Calcular quality para SRS
        quality = self.calcular_quality(correcto, self.obtener_tiempo_respuesta())
        return {
            'correcto': correcto,
            'mensaje': mensaje,
            'respuesta_correcta': self.respuesta_correcta if not correcto else None,
            'opcion_correcta': self.indice_correcto,
            'intentos_usados': self.intentos,
            'intentos_restantes': max(0, self.max_intentos - self.intentos),
            'puntaje': self.puntaje,
            'quality': quality,
            'completado': self.completado
        }


class RetoTarjetasInverso(RetoTarjetas):
    """
    Variante inversa: mostrar significado/traducción y pedir la palabra en inglés.
    """
    def generar(self) -> Dict[str, Any]:
        """Genera el reto inverso."""
        info = self.diccionario.obtener_info(self.palabra_objetivo)
        
        if not info:
            raise ValueError(f"Palabra '{self.palabra_objetivo}' no encontrada")
        # En este caso, la "pregunta" es el significado - ESTRUCTURA REAL DEL JSON
        if self.tipo == "traduccion":
            traducciones_es = info.get('traducciones', {}).get('es', [])
            pregunta_texto = traducciones_es[0] if traducciones_es else 'Sin traducción'
        elif self.tipo == "definicion":
            definiciones = info.get('definiciones', [])
            if definiciones:
                pregunta_texto = definiciones[0]
            else:
                traducciones_es = info.get('traducciones', {}).get('es', [])
                pregunta_texto = traducciones_es[0] if traducciones_es else 'Sin definición'
        else:
            traducciones_es = info.get('traducciones', {}).get('es', [])
            pregunta_texto = traducciones_es[0] if traducciones_es else 'Sin información'
        # La respuesta correcta es la palabra en inglés
        self.respuesta_correcta = self.palabra_objetivo
        # Generar distractores (otras palabras en inglés)
        categoria = info.get('categorias', ['general'])[0]
        palabras_categoria = self.diccionario.palabras_por_categoria(categoria)
        palabras_candidatas = [p for p in palabras_categoria if p != self.palabra_objetivo]
        random.shuffle(palabras_candidatas)
        self.opciones = palabras_candidatas[:self.num_opciones - 1]
        # Insertar respuesta correcta
        self.indice_correcto = random.randint(0, len(self.opciones))
        self.opciones.insert(self.indice_correcto, self.respuesta_correcta)
        return {
            'tipo_reto': 'tarjetas_inverso',
            'tipo_tarjeta': self.tipo,
            'pregunta_texto': pregunta_texto,
            'pregunta': f"¿Qué palabra en inglés significa '{pregunta_texto}'?",
            'opciones': self.opciones,
            'num_opciones': len(self.opciones)
        }