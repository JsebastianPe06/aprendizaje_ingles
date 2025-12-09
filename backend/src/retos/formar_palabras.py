"""
Reto de formar palabras con letras.
"""
import random
from typing import List, Dict

class RetoFormarPalabras:
    def __init__(self, palabra_objetivo: str):
        self.palabra_objetivo = palabra_objetivo.lower()
        self.letras = list(self.palabra_objetivo)
        random.shuffle(self.letras)
        self.intentos = 0
        self.respuesta_usuario = ""
    
    def obtener_letras(self):
        """Obtiene las letras desordenadas"""
        return self.letras
    
    def verificar_respuesta(self, respuesta: str) -> Dict:
        """Verifica si la respuesta es correcta"""
        self.intentos += 1
        respuesta_limpia = respuesta.lower().strip()
        
        es_correcto = respuesta_limpia == self.palabra_objetivo
        
        return {
            "correcto": es_correcto,
            "respuesta_correcta": self.palabra_objetivo,
            "respuesta_usuario": respuesta_limpia,
            "intentos": self.intentos
        }

def formar_palabras(palabra):
    """
    Función que toma una palabra y genera variaciones de la misma.
    
    Args:
        palabra (str): La palabra base para formar variaciones.
    
    Returns:
        list: Una lista de variaciones de la palabra.
    """
    variaciones = []
    
    # Prefijos comunes en inglés
    prefijos = ['re', 'un', 'dis', 'pre', 'mis']
    # Sufijos comunes en inglés
    sufijos = ['ing', 'ed', 'tion', 'ness', 'ment', 'able', 'less']
    
    palabra_base = palabra.lower()
    
    for prefijo in prefijos:
        variaciones.append(prefijo + palabra_base)
    
    for sufijo in sufijos:
        variaciones.append(palabra_base + sufijo)
    
    return variaciones

def generar_reto_formar_palabras(palabra: str) -> Dict:
    """Genera un reto de formar palabras"""
    reto = RetoFormarPalabras(palabra)
    
    return {
        "tipo": "formar_palabras",
        "palabra_objetivo": palabra,
        "letras_desordenadas": reto.obtener_letras(),
        "dificultad": calcular_dificultad(palabra)
    }

def calcular_dificultad(palabra: str) -> str:
    """Calcula la dificultad basada en la longitud de la palabra"""
    longitud = len(palabra)
    if longitud <= 5:
        return "facil"
    elif longitud <= 8:
        return "media"
    else:
        return "dificil"