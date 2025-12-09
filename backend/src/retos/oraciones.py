"""
Este archivo maneja los desafíos relacionados con oraciones en el sistema de aprendizaje de inglés.
"""
import random
from typing import List, Dict

def generar_oracion(vocabulario: List[str]) -> str:
    """
    Genera una oración utilizando el vocabulario proporcionado.
    
    Args:
        vocabulario (list): Lista de palabras que se utilizarán para formar la oración.
    
    Returns:
        str: Una oración generada a partir del vocabulario.
    """
    cantidad_palabras = min(len(vocabulario), random.randint(3, 6))
    palabras_seleccionadas = random.sample(vocabulario, cantidad_palabras)
    return ' '.join(palabras_seleccionadas) + '.'

def validar_oracion(oracion: str) -> bool:
    """
    Valida si la oración cumple con ciertos criterios.
    
    Args:
        oracion (str): La oración a validar.
    
    Returns:
        bool: True si la oración es válida, False en caso contrario.
    """
    palabras = oracion.strip().split()
    # Mínimo 3 palabras, debe terminar con puntuación
    return len(palabras) >= 3 and oracion.strip().endswith(('.',  '!', '?'))

def contar_palabras(oracion: str) -> int:
    """
    Cuenta el número de palabras en una oración.
    
    Args:
        oracion (str): La oración a analizar.
    
    Returns:
        int: Número de palabras en la oración.
    """
    return len(oracion.strip().split())

def generar_reto_oracion(palabra_clave: str, nivel: str = "basico") -> Dict:
    """
    Genera un reto de construcción de oraciones.
    
    Args:
        palabra_clave (str): Palabra que debe incluir la oración
        nivel (str): Nivel de dificultad
    
    Returns:
        dict: Datos del reto
    """
    ejemplos = {
        "basico": [
            f"Create a sentence with the word: {palabra_clave}",
            f"Write a sentence using: {palabra_clave}"
        ],
        "intermedio": [
            f"Write a meaningful sentence with {palabra_clave} in past tense",
            f"Create a question using {palabra_clave}"
        ],
        "avanzado": [
            f"Write a complex sentence using {palabra_clave} and a relative clause",
            f"Create a sentence with {palabra_clave} in conditional form"
        ]
    }
    
    instrucciones = random.choice(ejemplos.get(nivel, ejemplos["basico"]))
    
    return {
        "tipo": "construir_oracion",
        "palabra_clave": palabra_clave,
        "instruccion": instrucciones,
        "nivel": nivel,
        "validacion_requerida": True
    }