"""
Reto de formar palabras: dar letras desordenadas y pedir formar la palabra correcta.
VERSIÓN CORREGIDA para estructura JSON real
"""

import random
from typing import Dict, Any, List
from .base import RetoBase

class RetoFormarPalabras(RetoBase):
    """
    Reto de anagrama: dar letras mezcladas y pedir que forme la palabra.
    
    Variantes:
    - Letras completamente mezcladas
    - Con pista (traducción o definición)
    - Con letras extra (más difícil)
    """
    
    def __init__(self, palabra_objetivo: str, diccionario, analizador,
                nivel_dificultad: str = "intermedio",
                con_pista: bool = True,
                letras_extra: int = 0):
        """
        :param palabra_objetivo: Palabra a formar
        :param diccionario: Instancia de Diccionario
        :param analizador: Instancia de Analizador (para verificación flexible)
        :param nivel_dificultad: Dificultad
        :param con_pista: Si se muestra pista (traducción)
        :param letras_extra: Número de letras adicionales (distractores)
        """
        super().__init__(palabra_objetivo, nivel_dificultad)
        self.diccionario = diccionario
        self.analizador = analizador
        self.con_pista = con_pista
        self.letras_extra = letras_extra
        self.letras_mezcladas = []
        self.pista = None

    def generar(self) -> Dict[str, Any]:
        """
        Genera el reto de formar palabra.
        """
        info = self.diccionario.obtener_info(self.palabra_objetivo)
        if not info:
            raise ValueError(f"Palabra '{self.palabra_objetivo}' no encontrada")
        # Obtener letras de la palabra
        letras = list(self.palabra_objetivo.lower())
        # Agregar letras extra (distractores) si se especifica
        if self.letras_extra > 0:
            letras_distractoras = self._generar_letras_extra(letras)
            letras.extend(letras_distractoras)
        # Mezclar letras
        self.letras_mezcladas = letras.copy()
        random.shuffle(self.letras_mezcladas)
        # Asegurar que no quede igual a la palabra original
        intentos = 0
        while ''.join(self.letras_mezcladas) == self.palabra_objetivo.lower() and intentos < 10:
            random.shuffle(self.letras_mezcladas)
            intentos += 1
        # Generar pista si se requiere - ESTRUCTURA REAL DEL JSON
        if self.con_pista:
            # Primero intentar traducción
            traducciones_es = info.get('traducciones', {}).get('es', [])
            if traducciones_es:
                self.pista = traducciones_es[0]
            else:
                # Fallback a definición
                definiciones = info.get('definiciones', [])
                self.pista = definiciones[0] if definiciones else 'Sin pista'
        return {
            'tipo_reto': 'formar_palabras',
            'letras': self.letras_mezcladas,
            'letras_texto': ' '.join(self.letras_mezcladas).upper(),
            'num_letras': len(self.palabra_objetivo),
            'pista': self.pista,
            'pregunta': self._generar_pregunta(),
            'tiene_letras_extra': self.letras_extra > 0
        }

    def _generar_pregunta(self) -> str:
        """Genera el texto de la pregunta."""
        base = f"Ordena las letras para formar una palabra"
        if self.letras_extra > 0:
            base += f" (hay {self.letras_extra} letra(s) extra)"
        if self.pista:
            base += f"\nPista: {self.pista}"
        return base

    def _generar_letras_extra(self, letras_originales: List[str]) -> List[str]:
        """
        Genera letras adicionales como distractores.
        """
        vocales = ['a', 'e', 'i', 'o', 'u']
        consonantes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 
                    'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
        # Contar vocales y consonantes en la palabra original
        vocales_originales = sum(1 for l in letras_originales if l in vocales)
        consonantes_originales = len(letras_originales) - vocales_originales
        extras = []
        for _ in range(self.letras_extra):
            # Decidir si agregar vocal o consonante (proporcional a la palabra)
            if random.random() < vocales_originales / len(letras_originales):
                # Agregar vocal que no esté ya
                candidatas = [v for v in vocales if v not in letras_originales + extras]
                if candidatas:
                    extras.append(random.choice(candidatas))
                else:
                    extras.append(random.choice(vocales))
            else:
                # Agregar consonante
                candidatas = [c for c in consonantes if c not in letras_originales + extras]
                if candidatas:
                    extras.append(random.choice(candidatas))
                else:
                    extras.append(random.choice(consonantes))
        return extras
    
    def verificar(self, respuesta: Any) -> Dict[str, Any]:
        """
        Verifica la respuesta del usuario.
        
        :param respuesta: Palabra formada por el usuario
        :return: Diccionario con resultado
        """
        self.intentos += 1
        if not isinstance(respuesta, str):
            respuesta = str(respuesta)
        respuesta = respuesta.strip().lower()
        # Usar analizador para verificación flexible (tolera pequeños errores)
        correcto = self.analizador.verificar_respuesta_exacta(respuesta=respuesta,
            solucion=self.palabra_objetivo, umbral=0.9)
        mensaje = ""
        if correcto:
            self.puntaje = 100 - (self.intentos - 1) * 20
            self.puntaje = max(0, self.puntaje)
            mensaje = f"¡Correcto! La palabra es '{self.palabra_objetivo}'"
            self.finalizar()
        else:
            self.puntaje = max(0, 100 - (self.intentos * 25))
            if self.intentos >= self.max_intentos:
                mensaje = f"Se acabaron los intentos. La palabra era: '{self.palabra_objetivo}'"
                self.finalizar()
            else:
                # Dar retroalimentación útil
                if len(respuesta) != len(self.palabra_objetivo):
                    mensaje = f"Incorrecto. La palabra tiene {len(self.palabra_objetivo)} letras. "
                else:
                    mensaje = "Incorrecto. "
                mensaje += f"Intento {self.intentos}/{self.max_intentos}"
                # Mostrar pista en segundo intento si no la había - ESTRUCTURA REAL DEL JSON
                if self.intentos == 2 and not self.con_pista:
                    info = self.diccionario.obtener_info(self.palabra_objetivo)
                    if info:
                        traducciones_es = info.get('traducciones', {}).get('es', [])
                        self.pista = traducciones_es[0] if traducciones_es else 'Sin pista adicional'
                    else:
                        self.pista = 'Sin pista adicional'
                    mensaje += f"\nPista: {self.pista}"
        quality = self.calcular_quality(correcto, self.obtener_tiempo_respuesta())
        return {
            'correcto': correcto,
            'mensaje': mensaje,
            'respuesta_usuario': respuesta,
            'respuesta_correcta': self.palabra_objetivo if self.completado else None,
            'intentos_usados': self.intentos,
            'intentos_restantes': max(0, self.max_intentos - self.intentos),
            'puntaje': self.puntaje,
            'quality': quality,
            'completado': self.completado,
            'similitud': self.analizador.similitud(respuesta, self.palabra_objetivo)
        }


class RetoFormarPalabrasMultiple(RetoBase):
    """
    Variante avanzada: formar múltiples palabras con un conjunto de letras.
    Similar a juegos como "Wordament" o "Boggle".
    """
    
    def __init__(self, palabras_objetivo: List[str], diccionario, analizador,
        nivel_dificultad: str = "avanzado"):
        """
        :param palabras_objetivo: Lista de palabras que se pueden formar
        :param diccionario: Instancia de Diccionario
        :param analizador: Instancia de Analizador
        """
        super().__init__(palabras_objetivo[0] if palabras_objetivo else "", nivel_dificultad)
        self.palabras_objetivo = palabras_objetivo
        self.diccionario = diccionario
        self.analizador = analizador
        self.letras_disponibles = []
        self.palabras_encontradas = set()
        self.max_intentos = 10  # Más intentos para este tipo
        
    def generar(self) -> Dict[str, Any]:
        """Genera el reto de formar múltiples palabras."""
        if not self.palabras_objetivo:
            raise ValueError("Debe proporcionar al menos una palabra objetivo")
        # Generar conjunto de letras que permita formar todas las palabras
        todas_letras = set()
        for palabra in self.palabras_objetivo:
            todas_letras.update(palabra.lower())
        self.letras_disponibles = list(todas_letras)
        random.shuffle(self.letras_disponibles)
        return {
            'tipo_reto': 'formar_palabras_multiple',
            'letras': self.letras_disponibles,
            'letras_texto': ' '.join(self.letras_disponibles).upper(),
            'num_palabras_objetivo': len(self.palabras_objetivo),
            'palabras_encontradas': len(self.palabras_encontradas),
            'pregunta': f"Forma {len(self.palabras_objetivo)} palabras usando estas letras"
        }
    
    def verificar(self, respuesta: Any) -> Dict[str, Any]:
        """Verifica si la palabra formada es una de las objetivo."""
        self.intentos += 1
        if not isinstance(respuesta, str):
            respuesta = str(respuesta)
        respuesta = respuesta.strip().lower()
        correcto = False
        mensaje = ""
        # Verificar si es una de las palabras objetivo
        for palabra in self.palabras_objetivo:
            if self.analizador.verificar_respuesta_exacta(respuesta, palabra, umbral=0.9):
                if palabra not in self.palabras_encontradas:
                    self.palabras_encontradas.add(palabra)
                    correcto = True
                    mensaje = f"¡Correcto! Has encontrado '{palabra}'"
                else:
                    mensaje = f"Ya habías encontrado '{palabra}'"
                break
        if not correcto and respuesta not in [p for p in self.palabras_objetivo]:
            mensaje = f"'{respuesta}' no es una de las palabras objetivo"
        # Verificar si completó todas
        if len(self.palabras_encontradas) == len(self.palabras_objetivo):
            self.finalizar()
            mensaje += "\n¡Completaste todas las palabras! 🎉"
            self.puntaje = 100
        else:
            self.puntaje = int((len(self.palabras_encontradas) / len(self.palabras_objetivo)) * 100)
        quality = 4 if len(self.palabras_encontradas) == len(self.palabras_objetivo) else 3
        return {
            'correcto': correcto,
            'mensaje': mensaje,
            'palabras_encontradas': list(self.palabras_encontradas),
            'palabras_restantes': len(self.palabras_objetivo) - len(self.palabras_encontradas),
            'progreso': f"{len(self.palabras_encontradas)}/{len(self.palabras_objetivo)}",
            'intentos_usados': self.intentos,
            'puntaje': self.puntaje,
            'quality': quality,
            'completado': self.completado
        }