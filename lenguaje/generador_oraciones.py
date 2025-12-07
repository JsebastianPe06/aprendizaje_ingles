"""
Un generador de oraciones básico con sentido sintáctico y algo de sentido semántico
"""

import random
from typing import Dict, List

from .grafo_palabras import Grafo

class GeneradorGramatical:
    """
    Generador que produce oraciones GRAMATICALMENTE CORRECTAS.
    """
    
    # Plantillas con VERIFICACIÓN GRAMATICAL
    PLANTILLAS_VERIFICADAS = [
        # ========== ORACIONES SIMPLES (A1-A2) ==========
        # Sujeto (singular) + Verbo (3ra persona) + Objeto
        ("The {sustantivo_singular} {verbo_3ra} the {sustantivo2}.", 
        ["sustantivo_singular", "verbo_3ra", "sustantivo2"]),
        
        ("{pronombre} {verbo} {adverbio} in the {lugar}.", 
        ["pronombre", "verbo", "adverbio", "lugar"]),
        
        ("The {sustantivo_singular} is {adjetivo}.", 
        ["sustantivo_singular", "adjetivo"]),
        
        ("{pronombre} {verbo} to {lugar} every day.", 
        ["pronombre", "verbo", "lugar"]),
        
        # ========== ORACIONES INTERMEDIAS (B1-B2) ==========
        ("After {verbo_ing}, {pronombre} {verbo_pasado} {adverbio}.", 
        ["verbo_ing", "pronombre", "verbo_pasado", "adverbio"]),
        
        ("If the {sustantivo_singular} {verbo_3ra}, it will {verbo}.", 
        ["sustantivo_singular", "verbo_3ra", "verbo"]),
        
        ("The {adjetivo} {sustantivo_singular} {verbo_3ra} very {adverbio}.", 
        ["adjetivo", "sustantivo_singular", "verbo_3ra", "adverbio"]),
        
        ("{pronombre} decided to {verbo} because of the {sustantivo_singular}.", 
        ["pronombre", "verbo", "sustantivo_singular"]),
        
        # ========== ORACIONES AVANZADAS (C1-C2) ==========
        ("Despite the {sustantivo_singular}, {pronombre} managed to {verbo}.", 
        ["sustantivo_singular", "pronombre", "verbo"]),
        
        ("The {sustantivo_singular} that {verbo_3ra} in the {lugar} is {adjetivo}.", 
        ["sustantivo_singular", "verbo_3ra", "lugar", "adjetivo"]),
        
        ("Having {verbo_participio} the {sustantivo_singular}, {pronombre} {verbo_pasado}.", 
        ["verbo_participio", "sustantivo_singular", "pronombre", "verbo_pasado"]),
    ]
    
    # Vocabulario BASE por dominio (para máxima coherencia)
    VOCABULARIO_BASE = {
        'education': {
            'sustantivos_singulares': ['student', 'teacher', 'school', 'book', 'lesson', 
                        'class', 'homework', 'exam', 'knowledge', 'university'],
                        'sustantivos_plurales': ['students', 'teachers', 'schools', 'books', 'lessons'],
            'verbos_base': ['study', 'learn', 'teach', 'read', 'write', 'explain', 
                        'understand', 'practice', 'answer', 'attend'],
                        'verbos_3ra': ['studies', 'learns', 'teaches', 'reads', 'writes', 'explains'],
            'adjetivos': ['intelligent', 'educational', 'academic', 'difficult', 
                        'interesting', 'important', 'useful'],
            'lugares': ['school', 'university', 'classroom', 'library', 'campus']
        },
        'health': {
            'sustantivos_singulares': ['doctor', 'patient', 'hospital', 'medicine', 'treatment',
                                    'symptom', 'recovery', 'health', 'illness', 'pain'],
            'sustantivos_plurales': ['doctors', 'patients', 'hospitals', 'medicines'],
            'verbos_base': ['treat', 'heal', 'recover', 'examine', 'prescribe', 
                        'diagnose', 'improve', 'prevent', 'care', 'suffer'],
            'verbos_3ra': ['treats', 'heals', 'recovers', 'examines', 'prescribes'],
            'adjetivos': ['healthy', 'sick', 'medical', 'chronic', 'physical', 
                        'mental', 'severe', 'mild', 'acute'],
            'lugares': ['hospital', 'clinic', 'office', 'pharmacy', 'ward']
        },
        'work': {
            'sustantivos_singulares': ['employee', 'manager', 'office', 'meeting', 'project',
                                    'company', 'business', 'salary', 'deadline', 'colleague'],
            'sustantivos_plurales': ['employees', 'managers', 'offices', 'meetings'],
            'verbos_base': ['work', 'manage', 'organize', 'present', 'create',
                        'collaborate', 'achieve', 'complete', 'attend', 'lead'],
            'verbos_3ra': ['works', 'manages', 'organizes', 'presents', 'creates'],
            'adjetivos': ['professional', 'efficient', 'productive', 'successful',
                        'corporate', 'organized', 'dedicated'],
            'lugares': ['office', 'company', 'meeting_room', 'factory', 'store']
        },
        'general': {
            'sustantivos_singulares': ['person', 'thing', 'place', 'time', 'way', 
                                    'year', 'day', 'man', 'woman', 'child'],
            'sustantivos_plurales': ['people', 'things', 'places', 'times'],
            'verbos_base': ['do', 'make', 'go', 'see', 'know', 
                        'think', 'take', 'come', 'look', 'use'],
            'verbos_3ra': ['does', 'makes', 'goes', 'sees', 'knows'],
            'adjetivos': ['good', 'bad', 'big', 'small', 'new', 
                        'old', 'important', 'different', 'same'],
            'lugares': ['home', 'park', 'store', 'city', 'country']
        }
    }
    
    # Elementos fijos con gramática correcta
    PRONOMBRES_SUJETO = {
        'singular': ['I', 'You', 'He', 'She', 'It'],
        'plural': ['We', 'They', 'You']
    }
    
    ADVERBIOS = ["quickly", "slowly", "carefully", "happily", "easily", 
                "well", "badly", "quietly", "clearly", "regularly"]
    
    def __init__(self, grafo:Grafo):
        self.grafo = grafo
        if not self.grafo.construido:
            self.grafo.construir()
    
    def _adaptar_verbo(self, verbo_base: str, forma: str) -> str:
        """
        Adapta un verbo a la forma gramatical correcta.
        """
        # Si ya está en la forma correcta del vocabulario base
        if forma == "3ra" and verbo_base in self._obtener_todos_verbos_3ra():
            return verbo_base
        if forma == "base":
            return verbo_base
        elif forma == "3ra":
            # Reglas para 3ra persona singular
            if verbo_base.endswith(('s', 'x', 'z', 'ch', 'sh')):
                return verbo_base + 'es'
            elif verbo_base.endswith('y') and len(verbo_base) > 1 and verbo_base[-2] not in 'aeiou':
                return verbo_base[:-1] + 'ies'
            else:
                return verbo_base + 's'
        elif forma == "ing":
            # Gerundio
            if verbo_base.endswith('e'):
                return verbo_base[:-1] + 'ing'
            elif verbo_base.endswith('ie'):
                return verbo_base[:-2] + 'ying'
            else:
                return verbo_base + 'ing'
        elif forma == "pasado":
            # Pasado simple
            if verbo_base.endswith('e'):
                return verbo_base + 'd'
            elif verbo_base.endswith('y') and len(verbo_base) > 1 and verbo_base[-2] not in 'aeiou':
                return verbo_base[:-1] + 'ied'
            else:
                return verbo_base + 'ed'
        elif forma == "participio":
            # Participio pasado (simplificado: igual que pasado)
            return self._adaptar_verbo(verbo_base, "pasado")
        return verbo_base
    
    def _obtener_todos_verbos_3ra(self) -> List[str]:
        """Obtiene todos los verbos en 3ra persona de los vocabularios base."""
        verbos_3ra = []
        for dominio in self.VOCABULARIO_BASE.values():
            verbos_3ra.extend(dominio.get('verbos_3ra', []))
        return list(set(verbos_3ra))
    
    def _obtener_palabra_apropiada(self, tipo: str, dominio: str, 
        evitar: List[str] = None) -> str:
        """
        Obtiene una palabra apropiada para el contexto.
        PRIORIDAD: 1. Vocabulario base, 2. Grafo, 3. Fallback
        """
        if evitar is None:
            evitar = []
        # PRIMERO: Intentar vocabulario base del dominio
        if dominio in self.VOCABULARIO_BASE:
            vocabulario = self.VOCABULARIO_BASE[dominio]
            if tipo == "sustantivo_singular" and "sustantivos_singulares" in vocabulario:
                candidatos = [p for p in vocabulario["sustantivos_singulares"] if p not in evitar]
                if candidatos:
                    return random.choice(candidatos)
            elif tipo == "sustantivo2" and "sustantivos_singulares" in vocabulario:
                candidatos = [p for p in vocabulario["sustantivos_singulares"] if p not in evitar]
                if candidatos:
                    return random.choice(candidatos)
            elif tipo == "verbo_base" and "verbos_base" in vocabulario:
                candidatos = [p for p in vocabulario["verbos_base"] if p not in evitar]
                if candidatos:
                    return random.choice(candidatos)
            elif tipo == "verbo_3ra" and "verbos_3ra" in vocabulario:
                candidatos = [p for p in vocabulario["verbos_3ra"] if p not in evitar]
                if candidatos:
                    return random.choice(candidatos)
            elif tipo == "adjetivo" and "adjetivos" in vocabulario:
                candidatos = [p for p in vocabulario["adjetivos"] if p not in evitar]
                if candidatos:
                    return random.choice(candidatos)
            elif tipo == "lugar" and "lugares" in vocabulario:
                candidatos = [p for p in vocabulario["lugares"] if p not in evitar]
                if candidatos:
                    return random.choice(candidatos)
        # SEGUNDO: Intentar con el grafo (si el tipo corresponde a categoría)
        categoria_grafo = None
        if tipo.startswith("sustantivo"):
            categoria_grafo = "sustantivo"
        elif tipo.startswith("verbo"):
            categoria_grafo = "verbo"
        elif tipo == "adjetivo":
            categoria_grafo = "adjetivo"
        if categoria_grafo:
            try:
                candidatos = self.grafo.obtener_palabras_categoria(categoria_grafo, dominio)
                candidatos = [c for c in candidatos if c not in evitar]
                if candidatos:
                    return random.choice(candidatos)
            except:
                pass
        # TERCERO: Fallback a vocabulario general
        if dominio != "general":
            return self._obtener_palabra_apropiada(tipo, "general", evitar)
        # ÚLTIMO: Palabras muy básicas
        fallbacks = {
            "sustantivo_singular": "person",
            "sustantivo2": "thing",
            "verbo_base": "do",
            "verbo_3ra": "does",
            "adjetivo": "good",
            "lugar": "place",
            "adverbio": "well",
            "pronombre": "He"
        }
        return fallbacks.get(tipo, "thing")
    
    def generar_oracion(self, palabra_clave: str = None, nivel: str = "intermedio") -> Dict:
        """
        Genera una oración GRAMATICALMENTE CORRECTA.
        """
        # Determinar dominio
        dominio = "general"
        if palabra_clave:
            info = self.grafo.obtener_info(palabra_clave)
            if info and 'semantica' in info:
                dominio_info = info['semantica'].get('dominio', 'general')
                if dominio_info in self.VOCABULARIO_BASE:
                    dominio = dominio_info
        # Filtrar plantillas por nivel
        if nivel == "basico":
            plantillas_filtradas = self.PLANTILLAS_VERIFICADAS[:4]
        elif nivel == "avanzado":
            plantillas_filtradas = self.PLANTILLAS_VERIFICADAS[-3:]
        else:
            plantillas_filtradas = self.PLANTILLAS_VERIFICADAS
        plantilla, slots = random.choice(plantillas_filtradas)
        # Generar palabras para cada slot
        mapping = {}
        palabras_usadas = []
        for slot in slots:
            # Elementos fijos
            if slot == "pronombre":
                # Elegir pronombre apropiado
                if any(s in slots for s in ["sustantivo_singular", "verbo_3ra"]):
                    # Si hay sustantivo singular o verbo 3ra, usar pronombre singular
                    pronombre = random.choice(self.PRONOMBRES_SUJETO['singular'])
                else:
                    pronombre = random.choice(self.PRONOMBRES_SUJETO['singular'] + self.PRONOMBRES_SUJETO['plural'])
                
                mapping[slot] = pronombre
                palabras_usadas.append(pronombre.lower())
                continue
            elif slot == "adverbio":
                adverbio = random.choice(self.ADVERBIOS)
                mapping[slot] = adverbio
                palabras_usadas.append(adverbio)
                continue
            # Determinar palabra base según slot
            if slot == "sustantivo_singular" and palabra_clave:
                # Usar palabra clave como primer sustantivo
                palabra_base = palabra_clave
            else:
                # Obtener palabra apropiada
                palabra_base = self._obtener_palabra_apropiada(slot, dominio, palabras_usadas)
            # Adaptar según forma requerida
            if slot.startswith("verbo_"):
                forma = slot.split("_")[1]  # "3ra", "ing", "pasado", etc.
                palabra_adaptada = self._adaptar_verbo(palabra_base, forma)
            else:
                palabra_adaptada = palabra_base
            mapping[slot] = palabra_adaptada
            palabras_usadas.append(palabra_base)
        # Construir oración
        try:
            oracion = plantilla.format(**mapping)
        except KeyError as e:
            print(f"Error en slot {e}, usando oración de respaldo")
            oracion = "The student studies English."
        # Formatear
        oracion = oracion.strip()
        if not oracion.endswith('.'):
            oracion += '.'
        oracion = oracion[0].upper() + oracion[1:]
        return {
            "oracion": oracion,
            "dominio": dominio,
            "palabra_clave": palabra_clave,
            "nivel": nivel,
            "plantilla_usada": plantilla,
            "palabras_usadas": palabras_usadas
        }
    
    def generar_parrafo(self, tema: str = None, num_oraciones: int = 3) -> str:
        """Genera párrafo coherente y gramaticalmente correcto."""
        if tema not in self.VOCABULARIO_BASE:
            tema = random.choice(['education', 'health', 'work'])
        oraciones = []
        # Primera oración establece el tema
        if tema == 'education':
            oraciones.append("Education is important for personal development.")
        elif tema == 'health':
            oraciones.append("Good health is essential for a happy life.")
        elif tema == 'work':
            oraciones.append("Professional work requires dedication and skill.")
        else:
            oraciones.append("Life presents many opportunities for growth.")
        # Oraciones adicionales (coherentes con el tema)
        for i in range(num_oraciones - 1):
            # Elegir palabra clave del tema
            if tema in self.VOCABULARIO_BASE:
                sustantivos = self.VOCABULARIO_BASE[tema]['sustantivos_singulares']
                if sustantivos:
                    palabra_clave = random.choice(sustantivos[:5])
                    resultado = self.generar_oracion(palabra_clave, "intermedio")
                else:
                    resultado = self.generar_oracion(None, "intermedio")
            else:
                resultado = self.generar_oracion(None, "intermedio")
            oraciones.append(resultado["oracion"])
        return " ".join(oraciones)