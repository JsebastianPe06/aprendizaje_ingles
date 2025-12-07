"""
Módulo para poder trabajar calsificando por medio de categorías
"""

class ClasificadorCategorias:
    """
    Utilidades para trabajar con categorías/POS del diccionario.
    """
    # Convenciones internas: usamos strings en españosl
    SUSTANTIVO = 'sustantivo'
    VERBO = 'verbo'
    ADJETIVO = 'adjetivo'
    ADVERBIO = 'adverbio'
    PREPOSICION = 'preposicion'

    def obtener_categorias(self, info_palabra:str)-> list[str]:
        """
        Devuelve una lista de las categorías de una palabra
        
        :param info_palabra: palabra en inglés que forme parte del diccionario
        """
        return info_palabra.get('categorias', []) if info_palabra else []

    def es_verbo(self, info_palabra:str)-> bool:
        """
        Devuelve si la palabra es un verbo
        
        :param info_palabra: palabra en inglés que forme parte del diccionario
        """
        return self.VERBO in self.obtener_categorias(info_palabra)

    def es_sustantivo(self, info_palabra:str)-> bool:
        """
        Devuelve si la palabra es un sustantivo

        :param info_palabra: palabra en inglés que forme parte del diccionario
        """
        return self.SUSTANTIVO in self.obtener_categorias(info_palabra)

    def es_adjetivo(self, info_palabra):
        """
        Devuelve si la palabra es un adjetivo

        :param info_palabra: palabra en inglés que forme parte del diccionario
        """
        return self.ADJETIVO in self.obtener_categorias(info_palabra)

    def es_adverbio(self, info_palabra):
        """
        Devuelve si la palabre es un adverbio

        :param info_palabra: palabra en inglés que forme parte del diccionario
        """
        return self.ADVERBIO in self.obtener_categorias(info_palabra)