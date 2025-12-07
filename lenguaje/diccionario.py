"""
Clase referente al diccionario cn todoas las palabras (4800)
"""
import json

class Diccionario:
    """
    Manejo del diccionario en memoria.
    - Carga desde un JSON con estructura:
    { "palabras": { "word": { ... } } }
    No es una representación de un grafo
    """

    def __init__(self, path_json:str=None, data_obj=None):
        """
        Inicializa el diccionario desde un archivo o desde objeto ya cargado.
        Si se proporciona data_obj, se usa directamente (útil para tests).

        :param path_json: dirección del json
        :param data_obj: si se le dá información directamente la puede cargar sin el path
        """
        self.path = path_json
        self.data = {}
        if data_obj is not None:
            self.data = data_obj
        elif path_json:
            self.cargar(path_json)

    def cargar(self, path:str):
        """
        Carga la información de json
        
        :param path: Dirección de json
        """
        with open(path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        # Asegura estructura mínima
        if 'palabras' not in self.data:
            raise ValueError("JSON de diccionario debe tener clave 'palabras'")
        return self.data

    def obtener_info(self, palabra:str):
        """
        Devuelve la información de una palabra si se encuentra en el json
        
        :param palabra: Palabra en inglés
        """
        if not palabra:
            return None
        return self.data.get('palabras', {}).get(palabra.lower())

    def iterar_palabras(self):
        """
        Itera sobre todas las palabras, es un método de test por lo que no se
        recomienda usar
        
        """
        for w, info in self.data.get('palabras', {}).items():
            yield w, info

    def palabras_por_categoria(self, categoria):
        """
        Devuelve lista de palabras cuya lista 'categorias' contiene la categoría.
        """
        res = []
        for w, info in self.iterar_palabras():
            cats = info.get('categorias') or []
            if categoria in cats:
                res.append(w)
        return res

    def buscar_por_tema(self, tema):
        """
        Devuelve lista de palabras cuya lista 'tema' contiene el tema.
        """
        res = []
        for w, info in self.iterar_palabras():
            temas = info.get('temas') or []
            if tema in temas:
                res.append(w)
        return res

    def buscar_por_nivel(self, max_nivel):
        """
        Recibe un valor numérico o CEFR. Si CEFR (A1..C2) lo mapea a número.
        Para tu sistema usamos niveles 0..100; si el diccionario tiene CEFR, quien
        llama debe convertirlo o usar un mapa external.

        :param max_nivel: valor numérico o string referene al nivle de las palabras
        """
        res = []
        for w, info in self.iterar_palabras():
            lvl = info.get('nivel')
            if lvl is None:
                continue
            try:
                # si el nivel está en formato entero (0-100)
                lvl_num = int(lvl)
            except Exception:
                # mapear CEFR a número mínimo - por defecto ignorar
                lvl_num = None
            if lvl_num is not None and lvl_num <= max_nivel:
                res.append(w)
        return res