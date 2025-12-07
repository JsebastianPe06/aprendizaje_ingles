"""
Docstring for lenguaje.analizador
"""

from .categorias import ClasificadorCategorias
from .diccionario import Diccionario

class Analizador:
    """
    Analizador ligero que ofrece utilidades para:
    - obtener la forma correcta de una palabra según tiempo/numero
    - verificar si una respuesta (string) coincide razonablemente con la
        solución esperada (tolerancia con Levenshtein)
    - comparar semánticamente usando sinónimos
    Se pretende que sea dependiente de Diccionario y ClasificadorCategorias.
    """

    def __init__(self, diccionario: Diccionario, clasificador: ClasificadorCategorias):
        self.dic = diccionario
        self.cat = clasificador

    # ---------- coincidencia aproximada de strings ----------
    @staticmethod
    def distancia_levenshtein(a: str, b: str) -> int:
        """
        Calcula distancia de Levenshtein (iterativa, O(len(a)*len(b))).
        """
        if a == b:
            return 0
        if len(a) == 0:
            return len(b)
        if len(b) == 0:
            return len(a)
        a = a.lower()
        b = b.lower()
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a, start=1):
            cur = [i] + [0] * len(b)
            for j, cb in enumerate(b, start=1):
                add = prev[j] + 1
                delete = cur[j-1] + 1
                change = prev[j-1] + (0 if ca == cb else 1)
                cur[j] = min(add, delete, change)
            prev = cur
        return prev[-1]

    def similitud(self, a: str, b: str) -> float:
        """
        Devuelve similitud normalizada 0..1 basada en Levenshtein.
        """
        if not a or not b:
            return 0.0
        d = self.distancia_levenshtein(a, b)
        maxlen = max(len(a), len(b))
        return 1 - d / maxlen

    def verificar_respuesta_exacta(self, respuesta: str, solucion: str, umbral=0.85) -> bool:
        """
        Verifica si la respuesta del usuario coincide con la solución,
        usando similitud o coincidencia exacta y aceptando sinónimos.
        """
        if not respuesta:
            return False
        if respuesta.strip().lower() == solucion.strip().lower():
            return True
        sim = self.similitud(respuesta.strip().lower(), solucion.strip().lower())
        if sim >= umbral:
            return True
        # intentar sinónimos
        info = self.dic.obtener_info(solucion)
        if info:
            sinonimos = info.get('sinonimos', [])
            for s in sinonimos:
                if respuesta.strip().lower() == s.strip().lower():
                    return True
                if self.similitud(respuesta.strip().lower(), s.strip().lower()) >= umbral:
                    return True
        return False

    # ---------- formas simples ----------
    def obtener_plural(self, palabra: str):
        """
        Devuelve forma plural si existe en diccionario.forms, sino intenta regla simple.
        """
        info = self.dic.obtener_info(palabra)
        if not info:
            return None
        formas = info.get('formas', {})
        plural = formas.get('plural') or []
        if plural:
            return plural[0]
        # regla simple: si termina en y -> ies, si termina en s->es, else +s
        if palabra.endswith('y') and len(palabra) > 1 and palabra[-2] not in 'aeiou':
            return palabra[:-1] + 'ies'
        if palabra.endswith(('s','x','z','ch','sh')):
            return palabra + 'es'
        return palabra + 's'

    def obtener_past(self, palabra: str):
        info = self.dic.obtener_info(palabra)
        if not info:
            return None
        formas = info.get('formas', {})
        past = formas.get('past') or []
        if past:
            return past[0]
        # regla simple regular
        if palabra.endswith('e'):
            return palabra + 'd'
        if palabra.endswith('y') and palabra[-2] not in 'aeiou':
            return palabra[:-1] + 'ied'
        return palabra + 'ed'