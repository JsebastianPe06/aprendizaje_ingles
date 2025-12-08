"""
PARCHES PARA oraciones.py
Reemplaza solo estas funciones específicas en tu archivo oraciones.py existente
"""

# ============================================================
# EN RetoTraducirOracion - Reemplazar _generar_traduccion_base()
# ============================================================

def _generar_traduccion_base(self) -> str:
    """Genera una traducción básica palabra por palabra."""
    palabras = self.oracion_inglés.split()
    traduccion = []
    
    for palabra in palabras:
        palabra_limpia = palabra.strip('.,!?;:"').lower()
        info = self.diccionario.obtener_info(palabra_limpia)
        
        if info:
            # ESTRUCTURA REAL: traducciones.es[0]
            traducciones_es = info.get('traducciones', {}).get('es', [])
            if traducciones_es:
                traduccion.append(traducciones_es[0])
            else:
                traduccion.append(f"[{palabra}]")
        else:
            traduccion.append(f"[{palabra}]")
    
    return ' '.join(traduccion)


# ============================================================
# RESUMEN COMPLETO DE CAMBIOS PARA oraciones.py
# ============================================================
"""
El archivo oraciones.py solo necesita este cambio menor en RetoTraducirOracion.

Los métodos RetoCompletarOracion y RetoOrdenarOracion ya funcionan correctamente
con la estructura del JSON porque no dependen de traducciones específicas.

CAMBIO ÚNICO NECESARIO:
En RetoTraducirOracion, método _generar_traduccion_base():
- Cambiar: info.get('traduccion')
- Por: info.get('traducciones', {}).get('es', [])[0] si existe, sino usar [palabra]

Ese es el ÚNICO cambio necesario en oraciones.py
"""

# ============================================================
# ARCHIVO COMPLETO oraciones.py CORREGIDO (si prefieres copiar todo)
# ============================================================

"""
Retos con oraciones: completar, ordenar, traducir, corregir.
VERSIÓN CORREGIDA para estructura JSON real
"""

import random
from typing import Dict, Any, List
from .base import RetoBase

class RetoCompletarOracion(RetoBase):
    """
    Completar una oración con la palabra correcta.
    Se muestra una oración con un espacio en blanco.
    """
    
    def __init__(self, palabra_objetivo: str, generador, diccionario, analizador,
                 nivel_dificultad: str = "intermedio",
                 con_opciones: bool = True):
        """
        :param palabra_objetivo: Palabra que debe completar
        :param generador: Instancia de GeneradorGramatical
        :param diccionario: Instancia de Diccionario
        :param analizador: Instancia de Analizador
        :param con_opciones: Si se dan opciones múltiples o es abierta
        """
        super().__init__(palabra_objetivo, nivel_dificultad)
        self.generador = generador
        self.diccionario = diccionario
        self.analizador = analizador
        self.con_opciones = con_opciones
        self.oracion_completa = ""
        self.oracion_con_blanco = ""
        self.opciones = []
        self.indice_correcto = None
        
    def generar(self) -> Dict[str, Any]:
        """Genera una oración con la palabra objetivo faltante."""
        # Generar oración que incluya la palabra objetivo
        resultado = self.generador.generar_oracion(
            palabra_clave=self.palabra_objetivo,
            nivel=self.nivel_dificultad
        )
        
        self.oracion_completa = resultado['oracion']
        
        # Crear versión con espacio en blanco
        self.oracion_con_blanco = self._crear_blanco(self.oracion_completa)
        
        # Si tiene opciones, generarlas
        if self.con_opciones:
            self.opciones = self._generar_opciones()
        
        return {
            'tipo_reto': 'completar_oracion',
            'oracion': self.oracion_con_blanco,
            'palabra_objetivo': self.palabra_objetivo,
            'con_opciones': self.con_opciones,
            'opciones': self.opciones if self.con_opciones else None,
            'pregunta': 'Completa la oración con la palabra correcta:'
        }
    
    def _crear_blanco(self, oracion: str) -> str:
        """Reemplaza la palabra objetivo con un espacio en blanco."""
        # Buscar la palabra en la oración (case insensitive)
        palabras = oracion.split()
        oracion_modificada = []
        
        for palabra in palabras:
            # Limpiar puntuación para comparar
            palabra_limpia = palabra.strip('.,!?;:"').lower()
            
            if palabra_limpia == self.palabra_objetivo.lower():
                # Mantener puntuación pero reemplazar palabra
                puntuacion = ''.join(c for c in palabra if c in '.,!?;:"')
                oracion_modificada.append('_____' + puntuacion)
            else:
                oracion_modificada.append(palabra)
        
        return ' '.join(oracion_modificada)
    
    def _generar_opciones(self) -> List[str]:
        """Genera opciones múltiples incluyendo la correcta."""
        info = self.diccionario.obtener_info(self.palabra_objetivo)
        if not info:
            return [self.palabra_objetivo]
        
        categoria = info.get('categorias', ['general'])[0]
        palabras_categoria = self.diccionario.palabras_por_categoria(categoria)
        
        # Filtrar y tomar opciones incorrectas
        distractores = [p for p in palabras_categoria if p != self.palabra_objetivo]
        random.shuffle(distractores)
        opciones = distractores[:3]
        
        # Insertar respuesta correcta
        self.indice_correcto = random.randint(0, len(opciones))
        opciones.insert(self.indice_correcto, self.palabra_objetivo)
        
        return opciones
    
    def verificar(self, respuesta: Any) -> Dict[str, Any]:
        """Verifica la respuesta del usuario."""
        self.intentos += 1
        correcto = False
        mensaje = ""
        
        if self.con_opciones:
            # Verificar por índice
            if isinstance(respuesta, str):
                try:
                    respuesta = int(respuesta)
                except ValueError:
                    if respuesta in self.opciones:
                        respuesta = self.opciones.index(respuesta)
            
            if respuesta == self.indice_correcto:
                correcto = True
        else:
            # Verificar respuesta abierta
            correcto = self.analizador.verificar_respuesta_exacta(
                respuesta=str(respuesta),
                solucion=self.palabra_objetivo,
                umbral=0.85
            )
        
        if correcto:
            self.puntaje = 100
            mensaje = f"¡Correcto! La oración completa es:\n{self.oracion_completa}"
            self.finalizar()
        else:
            self.puntaje = max(0, 100 - (self.intentos * 30))
            if self.intentos >= self.max_intentos:
                mensaje = f"Incorrecto. La respuesta era: {self.palabra_objetivo}\n"
                mensaje += f"Oración completa: {self.oracion_completa}"
                self.finalizar()
            else:
                mensaje = f"Incorrecto. Intento {self.intentos}/{self.max_intentos}"
        
        quality = self.calcular_quality(correcto, self.obtener_tiempo_respuesta())
        
        return {
            'correcto': correcto,
            'mensaje': mensaje,
            'respuesta_correcta': self.palabra_objetivo if not correcto else None,
            'oracion_completa': self.oracion_completa if self.completado else None,
            'intentos_usados': self.intentos,
            'intentos_restantes': max(0, self.max_intentos - self.intentos),
            'puntaje': self.puntaje,
            'quality': quality,
            'completado': self.completado
        }


class RetoOrdenarOracion(RetoBase):
    """
    Ordenar palabras para formar una oración correcta.
    """
    
    def __init__(self, palabra_objetivo: str, generador, analizador,
                 nivel_dificultad: str = "intermedio"):
        """
        :param palabra_objetivo: Palabra clave de la oración
        :param generador: Instancia de GeneradorGramatical
        :param analizador: Instancia de Analizador
        """
        super().__init__(palabra_objetivo, nivel_dificultad)
        self.generador = generador
        self.analizador = analizador
        self.oracion_correcta = ""
        self.palabras_desordenadas = []
        
    def generar(self) -> Dict[str, Any]:
        """Genera una oración desordenada."""
        # Generar oración correcta
        resultado = self.generador.generar_oracion(
            palabra_clave=self.palabra_objetivo,
            nivel=self.nivel_dificultad
        )
        
        self.oracion_correcta = resultado['oracion']
        
        # Separar en palabras manteniendo puntuación
        palabras = self.oracion_correcta.split()
        
        # Separar puntuación de la última palabra
        ultima_palabra = palabras[-1]
        if ultima_palabra[-1] in '.!?':
            puntuacion = ultima_palabra[-1]
            palabras[-1] = ultima_palabra[:-1]
        else:
            puntuacion = '.'
        
        # Desordenar palabras
        self.palabras_desordenadas = palabras.copy()
        random.shuffle(self.palabras_desordenadas)
        
        # Asegurar que no quede en el mismo orden
        intentos = 0
        while self.palabras_desordenadas == palabras and intentos < 10:
            random.shuffle(self.palabras_desordenadas)
            intentos += 1
        
        return {
            'tipo_reto': 'ordenar_oracion',
            'palabras': self.palabras_desordenadas,
            'palabras_texto': ' / '.join(self.palabras_desordenadas),
            'puntuacion': puntuacion,
            'num_palabras': len(palabras),
            'pregunta': 'Ordena las palabras para formar una oración correcta:'
        }
    
    def verificar(self, respuesta: Any) -> Dict[str, Any]:
        """
        Verifica el orden de las palabras.
        
        :param respuesta: String con las palabras ordenadas o lista de palabras
        """
        self.intentos += 1
        
        if isinstance(respuesta, list):
            respuesta = ' '.join(respuesta)
        
        respuesta = str(respuesta).strip()
        
        # Agregar punto si no tiene puntuación
        if not respuesta[-1] in '.!?':
            respuesta += '.'
        
        # Capitalizar primera letra
        respuesta = respuesta[0].upper() + respuesta[1:]
        
        # Usar similitud para verificar (permite pequeñas variaciones)
        similitud = self.analizador.similitud(respuesta.lower(), self.oracion_correcta.lower())
        correcto = similitud >= 0.9
        
        mensaje = ""
        if correcto:
            self.puntaje = 100
            mensaje = f"¡Correcto! 🎉\nOración: {self.oracion_correcta}"
            self.finalizar()
        else:
            self.puntaje = max(0, 100 - (self.intentos * 25))
            
            if self.intentos >= self.max_intentos:
                mensaje = f"Incorrecto. El orden correcto era:\n{self.oracion_correcta}"
                self.finalizar()
            else:
                mensaje = f"Incorrecto. Intento {self.intentos}/{self.max_intentos}\n"
                mensaje += f"Similitud: {int(similitud * 100)}%"
        
        quality = self.calcular_quality(correcto, self.obtener_tiempo_respuesta())
        
        return {
            'correcto': correcto,
            'mensaje': mensaje,
            'respuesta_usuario': respuesta,
            'respuesta_correcta': self.oracion_correcta if self.completado else None,
            'similitud': similitud,
            'intentos_usados': self.intentos,
            'intentos_restantes': max(0, self.max_intentos - self.intentos),
            'puntaje': self.puntaje,
            'quality': quality,
            'completado': self.completado
        }


class RetoTraducirOracion(RetoBase):
    """
    Traducir una oración del inglés al español (o viceversa).
    """
    
    def __init__(self, palabra_objetivo: str, generador, diccionario, analizador,
                 nivel_dificultad: str = "intermedio",
                 ingles_a_espanol: bool = True):
        """
        :param palabra_objetivo: Palabra clave
        :param generador: Instancia de GeneradorGramatical
        :param diccionario: Instancia de Diccionario
        :param analizador: Instancia de Analizador
        :param ingles_a_espanol: Dirección de traducción
        """
        super().__init__(palabra_objetivo, nivel_dificultad)
        self.generador = generador
        self.diccionario = diccionario
        self.analizador = analizador
        self.ingles_a_espanol = ingles_a_espanol
        self.oracion_inglés = ""
        self.traduccion_sugerida = ""
        
    def generar(self) -> Dict[str, Any]:
        """Genera una oración para traducir."""
        # Generar oración en inglés
        resultado = self.generador.generar_oracion(
            palabra_clave=self.palabra_objetivo,
            nivel=self.nivel_dificultad
        )
        
        self.oracion_inglés = resultado['oracion']
        
        # Generar traducción palabra por palabra (simplificado)
        self.traduccion_sugerida = self._generar_traduccion_base()
        
        if self.ingles_a_espanol:
            oracion_a_mostrar = self.oracion_inglés
            pregunta = "Traduce al español:"
        else:
            oracion_a_mostrar = self.traduccion_sugerida
            pregunta = "Traduce al inglés:"
        
        return {
            'tipo_reto': 'traducir_oracion',
            'oracion': oracion_a_mostrar,
            'direccion': 'inglés→español' if self.ingles_a_espanol else 'español→inglés',
            'pregunta': pregunta,
            'palabras_clave': resultado.get('palabras_usadas', [])
        }
    
    def _generar_traduccion_base(self) -> str:
        """Genera una traducción básica palabra por palabra."""
        palabras = self.oracion_inglés.split()
        traduccion = []
        
        for palabra in palabras:
            palabra_limpia = palabra.strip('.,!?;:"').lower()
            info = self.diccionario.obtener_info(palabra_limpia)
            
            if info:
                # ESTRUCTURA REAL DEL JSON: traducciones.es[0]
                traducciones_es = info.get('traducciones', {}).get('es', [])
                if traducciones_es:
                    traduccion.append(traducciones_es[0])
                else:
                    traduccion.append(f"[{palabra}]")
            else:
                traduccion.append(f"[{palabra}]")
        
        return ' '.join(traduccion)
    
    def verificar(self, respuesta: Any) -> Dict[str, Any]:
        """
        Verifica la traducción (verificación flexible).
        """
        self.intentos += 1
        respuesta = str(respuesta).strip()
        
        if self.ingles_a_espanol:
            objetivo = self.traduccion_sugerida
        else:
            objetivo = self.oracion_inglés
        
        # Similitud flexible (la traducción puede variar)
        similitud = self.analizador.similitud(respuesta.lower(), objetivo.lower())
        
        # Más leniente para traducciones (umbral 0.7)
        correcto = similitud >= 0.7
        
        mensaje = ""
        if correcto:
            self.puntaje = int(similitud * 100)
            mensaje = f"¡Bien hecho! 🎉\nTraducción sugerida: {objetivo}"
            self.finalizar()
        else:
            self.puntaje = max(0, int(similitud * 100) - (self.intentos * 20))
            
            if self.intentos >= self.max_intentos:
                mensaje = f"Traducción sugerida:\n{objetivo}"
                self.finalizar()
            else:
                mensaje = f"Intento {self.intentos}/{self.max_intentos}\n"
                mensaje += f"Similitud: {int(similitud * 100)}%"
                
                if similitud > 0.5:
                    mensaje += "\n(Vas por buen camino)"
        
        quality = self.calcular_quality(correcto, self.obtener_tiempo_respuesta())
        
        return {
            'correcto': correcto,
            'mensaje': mensaje,
            'respuesta_usuario': respuesta,
            'traduccion_sugerida': objetivo if self.completado else None,
            'similitud': similitud,
            'intentos_usados': self.intentos,
            'intentos_restantes': max(0, self.max_intentos - self.intentos),
            'puntaje': self.puntaje,
            'quality': quality,
            'completado': self.completado
        }