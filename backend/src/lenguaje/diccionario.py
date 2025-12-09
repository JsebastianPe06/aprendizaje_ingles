class Diccionario:
    def __init__(self):
        self.diccionario = {}

    def agregar_palabra(self, palabra, significado):
        """Agrega una palabra con su significado al diccionario"""
        self.diccionario[palabra.lower()] = significado

    def obtener_significado(self, palabra):
        """Obtiene el significado de una palabra"""
        return self.diccionario.get(palabra.lower(), "Palabra no encontrada")

    def eliminar_palabra(self, palabra):
        """Elimina una palabra del diccionario"""
        if palabra.lower() in self.diccionario:
            del self.diccionario[palabra.lower()]
            return True
        return False

    def listar_palabras(self):
        """Lista todas las palabras del diccionario"""
        return list(self.diccionario.keys())

    def buscar_palabras(self, prefijo):
        """Busca palabras que comiencen con un prefijo"""
        return [p for p in self.diccionario.keys() if p.startswith(prefijo.lower())]

    def obtener_todas_palabras(self):
        """Retorna todas las palabras con sus significados"""
        return self.diccionario