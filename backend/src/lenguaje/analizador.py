"""
Este archivo contiene funciones para analizar datos del lenguaje.
"""

def analizar_texto(texto):
    """
    Analiza un texto y retorna estadísticas.
    
    Args:
        texto (str): El texto a analizar
    
    Returns:
        dict: Estadísticas del texto
    """
    palabras = texto.lower().split()
    oraciones = texto.split('.')
    
    return {
        "total_palabras": len(palabras),
        "total_oraciones": len([o for o in oraciones if o.strip()]),
        "palabras_unicas": len(set(palabras)),
        "promedio_palabras_por_oracion": len(palabras) / max(1, len([o for o in oraciones if o.strip()])),
        "palabras": palabras
    }

def contar_frecuencia(palabras):
    """
    Cuenta la frecuencia de cada palabra.
    
    Args:
        palabras (list): Lista de palabras
    
    Returns:
        dict: Diccionario con frecuencias
    """
    frecuencia = {}
    for palabra in palabras:
        palabra_limpia = palabra.lower()
        frecuencia[palabra_limpia] = frecuencia.get(palabra_limpia, 0) + 1
    
    return dict(sorted(frecuencia.items(), key=lambda x: x[1], reverse=True))

def obtener_palabras_clave(palabras, cantidad=10):
    """Obtiene las palabras más frecuentes"""
    frecuencia = contar_frecuencia(palabras)
    return dict(list(frecuencia.items())[:cantidad])