"""
Este archivo implementa una estructura de grafo para palabras, posiblemente para representar relaciones semánticas entre ellas.
"""

class Nodo:
    def __init__(self, palabra):
        self.palabra = palabra
        self.vecinos = {}

    def agregar_vecino(self, vecino, peso=1):
        self.vecinos[vecino] = peso

    def __repr__(self):
        return f"Nodo({self.palabra})"

class GrafoPalabras:
    def __init__(self):
        self.nodos = {}

    def agregar_palabra(self, palabra):
        if palabra not in self.nodos:
            self.nodos[palabra] = Nodo(palabra)

    def agregar_relacion(self, palabra1, palabra2, peso=1):
        self.agregar_palabra(palabra1)
        self.agregar_palabra(palabra2)
        self.nodos[palabra1].agregar_vecino(palabra2, peso)
        self.nodos[palabra2].agregar_vecino(palabra1, peso)

    def obtener_vecinos(self, palabra):
        if palabra in self.nodos:
            return self.nodos[palabra].vecinos
        return None

    def __repr__(self):
        return f"GrafoPalabras({self.nodos})"