"""
Generador de retos: selecciona y crea retos apropiados según contexto.
VERSIÓN CON DEBUG MEJORADO
"""

import random
from typing import List, Dict, Any, Optional
from .tarjetas import RetoTarjetas, RetoTarjetasInverso
from .formar_palabras import RetoFormarPalabras, RetoFormarPalabrasMultiple
from .oraciones import RetoCompletarOracion, RetoOrdenarOracion, RetoTraducirOracion

class GeneradorRetos:
    """
    Factoría de retos que selecciona el tipo apropiado según:
    - Nivel del usuario
    - Palabras pendientes (del motor SRS)
    - Variedad (no repetir el mismo tipo)
    - Dificultad progresiva
    """
    
    TIPOS_RETO = [
        'tarjetas',
        'tarjetas_inverso',
        'formar_palabras',
        'completar_oracion',
        'ordenar_oracion',
        'traducir_oracion'
    ]
    
    # Dificultad por tipo (1-5)
    DIFICULTAD_TIPOS = {
        'tarjetas': 1,
        'tarjetas_inverso': 2,
        'formar_palabras': 2,
        'completar_oracion': 3,
        'ordenar_oracion': 3,
        'traducir_oracion': 4,
        'formar_palabras_multiple': 5
    }
    
    def __init__(self, diccionario, analizador, grafo, generador_oraciones, motor_srs):
        """
        :param diccionario: Instancia de Diccionario
        :param analizador: Instancia de Analizador
        :param grafo: Instancia de Grafo
        :param generador_oraciones: Instancia de GeneradorGramatical
        :param motor_srs: Instancia de MotorSRS
        """
        self.diccionario = diccionario
        self.analizador = analizador
        self.grafo = grafo
        self.generador_oraciones = generador_oraciones
        self.motor_srs = motor_srs
        self.historial_tipos = []  # Para evitar repetición
        
        # Verificar que el grafo esté construido
        if not self.grafo.construido:
            print("⚠️  Grafo no construido, construyendo ahora...")
            self.grafo.construir()
        
    def generar_sesion_practica(self, nivel_usuario: int = 50, 
                               num_retos: int = 5,
                               tipos_permitidos: List[str] = None) -> List:
        """
        Genera una sesión completa de práctica con múltiples retos.
        
        :param nivel_usuario: Nivel del usuario (0-100)
        :param num_retos: Número de retos a generar
        :param tipos_permitidos: Lista de tipos permitidos (None = todos)
        :return: Lista de objetos de reto
        """
        print(f"📋 DEBUG: Generando sesión - nivel={nivel_usuario}, num_retos={num_retos}")
        
        # Obtener palabras pendientes del SRS
        palabras_pendientes = self.motor_srs.obtener_deberes()
        print(f"📚 DEBUG: Palabras pendientes del SRS: {len(palabras_pendientes)}")
        
        # Si no hay suficientes palabras pendientes, obtener del grafo
        if len(palabras_pendientes) < num_retos:
            print(f"⚠️  DEBUG: Pocas palabras en SRS, obteniendo del grafo...")
            
            # Obtener palabras del grafo según nivel
            palabras_grafo = []
            
            # Intentar obtener palabras de diferentes categorías
            categorias = ['sustantivo', 'verbo', 'adjetivo']
            for categoria in categorias:
                try:
                    palabras_cat = self.grafo.obtener_palabras_categoria(categoria)
                    if palabras_cat:
                        palabras_grafo.extend(palabras_cat[:20])  # Tomar hasta 20 de cada categoría
                except Exception as e:
                    print(f"⚠️  DEBUG: Error obteniendo categoría {categoria}: {e}")
            
            if not palabras_grafo:
                print("⚠️  DEBUG: No se pudieron obtener palabras del grafo, usando lista básica")
                # Fallback: usar palabras directamente del diccionario
                palabras_grafo = list(self.diccionario.data.get('palabras', {}).keys())[:50]
            
            print(f"✅ DEBUG: Palabras disponibles del grafo: {len(palabras_grafo)}")
            
            # Mezclar y tomar las necesarias
            random.shuffle(palabras_grafo)
            adicionales_necesarias = num_retos - len(palabras_pendientes)
            adicionales = palabras_grafo[:adicionales_necesarias]
            
            palabras_pendientes.extend(adicionales)
            print(f"✅ DEBUG: Total palabras después de agregar del grafo: {len(palabras_pendientes)}")
        
        # Asegurar que no haya duplicados y limitar
        palabras_a_practicar = list(set(palabras_pendientes))[:num_retos]
        print(f"🎯 DEBUG: Palabras seleccionadas para práctica: {palabras_a_practicar}")
        
        if len(palabras_a_practicar) < num_retos:
            print(f"⚠️  DEBUG: Solo se generarán {len(palabras_a_practicar)} retos (menos de los {num_retos} solicitados)")
        
        # Generar retos variados
        retos = []
        for i, palabra in enumerate(palabras_a_practicar):
            print(f"\n🔧 DEBUG: Generando reto {i+1}/{len(palabras_a_practicar)} para '{palabra}'")
            
            tipo_reto = self._seleccionar_tipo_reto(
                nivel_usuario=nivel_usuario,
                posicion_sesion=i,
                total_sesion=len(palabras_a_practicar),
                tipos_permitidos=tipos_permitidos
            )
            
            print(f"   Tipo seleccionado: {tipo_reto}")
            
            try:
                reto = self.crear_reto(
                    tipo=tipo_reto,
                    palabra=palabra,
                    nivel_usuario=nivel_usuario
                )
                
                if reto:
                    retos.append(reto)
                    print(f"   ✅ Reto creado exitosamente")
                else:
                    print(f"   ❌ No se pudo crear el reto (retornó None)")
            except Exception as e:
                print(f"   ❌ Error creando reto: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n✅ DEBUG: Total de retos generados: {len(retos)}")
        return retos
    
    def _seleccionar_tipo_reto(self, nivel_usuario: int, 
                               posicion_sesion: int,
                               total_sesion: int,
                               tipos_permitidos: List[str] = None) -> str:
        """
        Selecciona el tipo de reto más apropiado.
        
        Estrategia:
        - Empezar con retos más fáciles
        - Aumentar dificultad gradualmente
        - Variar tipos para mantener interés
        - Respetar nivel del usuario
        """
        if tipos_permitidos is None:
            tipos_permitidos = self.TIPOS_RETO
        
        # Filtrar por dificultad según nivel
        tipos_disponibles = []
        for tipo in tipos_permitidos:
            dificultad = self.DIFICULTAD_TIPOS.get(tipo, 3)
            
            # Mapear nivel usuario (0-100) a dificultad reto (1-5)
            dificultad_maxima = 1 + (nivel_usuario / 20)  # 0→1, 20→2, 40→3, etc.
            
            if dificultad <= dificultad_maxima:
                tipos_disponibles.append(tipo)
        
        if not tipos_disponibles:
            tipos_disponibles = ['tarjetas']  # Fallback
        
        # Evitar repetir el último tipo usado
        if self.historial_tipos:
            tipos_sin_repetir = [t for t in tipos_disponibles 
                                if t != self.historial_tipos[-1]]
            if tipos_sin_repetir:
                tipos_disponibles = tipos_sin_repetir
        
        # Aumentar dificultad gradualmente en la sesión
        if posicion_sesion > total_sesion / 2:
            # Segunda mitad: preferir tipos más difíciles
            tipos_dificiles = sorted(tipos_disponibles, 
                                    key=lambda t: self.DIFICULTAD_TIPOS.get(t, 3),
                                    reverse=True)
            tipos_disponibles = tipos_dificiles[:max(2, len(tipos_dificiles)//2)]
        
        # Seleccionar aleatoriamente
        tipo_seleccionado = random.choice(tipos_disponibles)
        self.historial_tipos.append(tipo_seleccionado)
        
        # Mantener historial limitado
        if len(self.historial_tipos) > 5:
            self.historial_tipos.pop(0)
        
        return tipo_seleccionado
    
    def crear_reto(self, tipo: str, palabra: str, 
                  nivel_usuario: int = 50,
                  **kwargs) -> Optional[Any]:
        """
        Crea un reto específico del tipo indicado.
        
        :param tipo: Tipo de reto a crear
        :param palabra: Palabra objetivo
        :param nivel_usuario: Nivel del usuario
        :param kwargs: Parámetros adicionales específicos del reto
        :return: Instancia del reto o None si hay error
        """
        # Verificar que la palabra existe en el diccionario
        info_palabra = self.diccionario.obtener_info(palabra)
        if not info_palabra:
            print(f"      ⚠️  Palabra '{palabra}' no encontrada en diccionario, intentando con otra...")
            # Obtener una palabra aleatoria del diccionario
            todas_palabras = list(self.diccionario.data.get('palabras', {}).keys())
            if todas_palabras:
                palabra = random.choice(todas_palabras[:100])
                print(f"      → Usando palabra alternativa: '{palabra}'")
            else:
                print(f"      ❌ No hay palabras disponibles en el diccionario")
                return None
        
        # Mapear nivel numérico a string
        if nivel_usuario < 30:
            nivel_str = "basico"
        elif nivel_usuario < 70:
            nivel_str = "intermedio"
        else:
            nivel_str = "avanzado"
        
        print(f"      Creando reto {tipo} para '{palabra}' (nivel: {nivel_str})")
        
        try:
            if tipo == 'tarjetas':
                return RetoTarjetas(
                    palabra_objetivo=palabra,
                    diccionario=self.diccionario,
                    nivel_dificultad=nivel_str,
                    tipo=kwargs.get('tipo_tarjeta', 'traduccion'),
                    num_opciones=kwargs.get('num_opciones', 4)
                )
            
            elif tipo == 'tarjetas_inverso':
                return RetoTarjetasInverso(
                    palabra_objetivo=palabra,
                    diccionario=self.diccionario,
                    nivel_dificultad=nivel_str,
                    tipo=kwargs.get('tipo_tarjeta', 'traduccion'),
                    num_opciones=kwargs.get('num_opciones', 4)
                )
            
            elif tipo == 'formar_palabras':
                letras_extra = 0 if nivel_usuario < 40 else 1 if nivel_usuario < 70 else 2
                return RetoFormarPalabras(
                    palabra_objetivo=palabra,
                    diccionario=self.diccionario,
                    analizador=self.analizador,
                    nivel_dificultad=nivel_str,
                    con_pista=nivel_usuario < 60,
                    letras_extra=letras_extra
                )
            
            elif tipo == 'completar_oracion':
                return RetoCompletarOracion(
                    palabra_objetivo=palabra,
                    generador=self.generador_oraciones,
                    diccionario=self.diccionario,
                    analizador=self.analizador,
                    nivel_dificultad=nivel_str,
                    con_opciones=nivel_usuario < 50
                )
            
            elif tipo == 'ordenar_oracion':
                return RetoOrdenarOracion(
                    palabra_objetivo=palabra,
                    generador=self.generador_oraciones,
                    analizador=self.analizador,
                    nivel_dificultad=nivel_str
                )
            
            elif tipo == 'traducir_oracion':
                return RetoTraducirOracion(
                    palabra_objetivo=palabra,
                    generador=self.generador_oraciones,
                    diccionario=self.diccionario,
                    analizador=self.analizador,
                    nivel_dificultad=nivel_str,
                    ingles_a_espanol=kwargs.get('ingles_a_espanol', True)
                )
            
            elif tipo == 'formar_palabras_multiple':
                # Obtener palabras relacionadas
                vecinos = self.grafo.obtener_vecinos(palabra, max_vecinos=3)
                palabras_objetivo = [palabra] + vecinos[:2]
                
                return RetoFormarPalabrasMultiple(
                    palabras_objetivo=palabras_objetivo,
                    diccionario=self.diccionario,
                    analizador=self.analizador,
                    nivel_dificultad="avanzado"
                )
            
            else:
                print(f"      ❌ Tipo de reto desconocido: {tipo}")
                return None
                
        except Exception as e:
            print(f"      ❌ Error creando reto {tipo} para '{palabra}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def crear_reto_personalizado(self, preferencias_usuario: Dict[str, Any]) -> Optional[Any]:
        """
        Crea un reto basado en las preferencias del usuario.
        
        :param preferencias_usuario: Diccionario con preferencias
            - 'temas': lista de temas preferidos
            - 'tipos_favoritos': lista de tipos de reto favoritos
            - 'nivel': nivel del usuario
        """
        nivel = preferencias_usuario.get('nivel', 50)
        temas = preferencias_usuario.get('temas', ['general'])
        tipos_favoritos = preferencias_usuario.get('tipos_favoritos', self.TIPOS_RETO)
        
        # Seleccionar tema aleatorio
        tema = random.choice(temas)
        
        # Obtener palabra del tema
        palabras_tema = self.diccionario.buscar_por_tema(tema)
        if not palabras_tema:
            # Fallback a palabras del nivel
            palabras_tema = self.diccionario.buscar_por_nivel(nivel)
        
        if not palabras_tema:
            # Último fallback: palabras aleatorias del diccionario
            palabras_tema = list(self.diccionario.data.get('palabras', {}).keys())[:50]
        
        if not palabras_tema:
            return None
        
        palabra = random.choice(palabras_tema)
        
        # Seleccionar tipo de reto de los favoritos
        tipo = self._seleccionar_tipo_reto(
            nivel_usuario=nivel,
            posicion_sesion=0,
            total_sesion=1,
            tipos_permitidos=tipos_favoritos
        )
        
        return self.crear_reto(tipo, palabra, nivel)
    
    def obtener_estadisticas_tipos(self) -> Dict[str, int]:
        """Retorna estadísticas de tipos de reto usados."""
        stats = {}
        for tipo in self.historial_tipos:
            stats[tipo] = stats.get(tipo, 0) + 1
        return stats
    
    def reiniciar_historial(self):
        """Reinicia el historial de tipos usados."""
        self.historial_tipos = []