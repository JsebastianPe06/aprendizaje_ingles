class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.palabras = []

    def agregar_palabra(self, palabra):
        """Agrega una palabra a la categoría"""
        if palabra not in self.palabras:
            self.palabras.append(palabra)

    def obtener_palabras(self):
        """Obtiene todas las palabras de la categoría"""
        return self.palabras

    def eliminar_palabra(self, palabra):
        """Elimina una palabra de la categoría"""
        if palabra in self.palabras:
            self.palabras.remove(palabra)
            return True
        return False

    def cantidad_palabras(self):
        """Retorna la cantidad de palabras"""
        return len(self.palabras)

    def a_diccionario(self):
        """Convierte la categoría a diccionario"""
        return {
            "nombre": self.nombre,
            "palabras": self.palabras,
            "cantidad": len(self.palabras)
        }

# Categorías predefinidas
CATEGORIAS_DISPONIBLES = {
    "Saludos": ["hello", "goodbye", "hi", "bye", "welcome"],
    "Números": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
    "Colores": ["red", "blue", "green", "yellow", "purple", "orange", "black", "white"],
    "Frutas": ["apple", "banana", "orange", "grape", "watermelon", "strawberry"],
    "Animales": ["cat", "dog", "bird", "fish", "elephant", "lion", "tiger"],
    "Verbos": ["run", "walk", "jump", "sleep", "eat", "drink", "play", "work"]
}

def listar_categorias():
    """Lista todas las categorías disponibles"""
    categorias = []
    for nombre, palabras in CATEGORIAS_DISPONIBLES.items():
        cat = Categoria(nombre)
        for palabra in palabras:
            cat.agregar_palabra(palabra)
        categorias.append(cat.a_diccionario())
    return categorias

def obtener_categoria(nombre):
    """Obtiene una categoría específica"""
    if nombre in CATEGORIAS_DISPONIBLES:
        cat = Categoria(nombre)
        for palabra in CATEGORIAS_DISPONIBLES[nombre]:
            cat.agregar_palabra(palabra)
        return cat.a_diccionario()
    return None