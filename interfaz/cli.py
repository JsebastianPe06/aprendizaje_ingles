"""
Interfaz de línea de comandos para el sistema de aprendizaje de inglés.
"""

import os
import sys
import time
from datetime import datetime
import random

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lenguaje.diccionario import Diccionario
from lenguaje.analizador import Analizador
from lenguaje.categorias import ClasificadorCategorias
from lenguaje.grafo_palabras import Grafo
from lenguaje.generador_oraciones import GeneradorGramatical
from lenguaje.motor_srs import MotorSRS

from retos.generador import GeneradorRetos

from usuario.perfil import PerfilUsuario
from usuario.progreso import SeguimientoProgreso
from usuario.estadistica import AnalizadorEstadisticas

from utils.validadores import Validadores, FormateadorTexto
from utils.loggers import LoggerConfig, AuditoriaUsuario, EstadisticasSesion


class InterfazCLI:
    """
    Interfaz de línea de comandos principal del sistema.
    """
    
    def __init__(self):
        """Inicializa la interfaz."""
        self.perfil = None
        self.progreso = None
        self.analizador_stats = None
        self.auditoria = None
        self.sesion_actual = None
        
        # Componentes del sistema
        self.diccionario = None
        self.analizador = None
        self.grafo = None
        self.generador_oraciones = None
        self.motor_srs = None
        self.generador_retos = None
        
        # Logger
        self.logger = LoggerConfig.configurar_logger()
        
        # Estado
        self.ejecutando = True
    
    def iniciar(self):
        """Inicia la aplicación."""
        self.limpiar_pantalla()
        self.mostrar_bienvenida()
        
        # Cargar datos
        if not self.cargar_sistema():
            print(FormateadorTexto.error("\n Error cargando el sistema. Saliendo..."))
            return
        
        # Gestión de usuario
        if not self.gestionar_usuario():
            print("\n ¡Hasta pronto!")
            return
        
        # Menú principal
        self.menu_principal()
    
    def cargar_sistema(self) -> bool:
        """
        Carga todos los componentes del sistema.
        
        :return: True si carga exitosa
        """
        try:
            print("\n Cargando sistema...")
            
            # Cargar diccionario
            ruta_json = os.path.join('data', 'a_p.json')
            if not os.path.exists(ruta_json):
                print(FormateadorTexto.error(f"No se encuentra el archivo: {ruta_json}"))
                return False
            
            print(" Cargando diccionario...")
            self.diccionario = Diccionario(ruta_json)
            
            print(" Inicializando analizador...")
            clasificador = ClasificadorCategorias()
            self.analizador = Analizador(self.diccionario, clasificador)
            
            print("  Construyendo grafo semántico...")
            self.grafo = Grafo(ruta_json)
            self.grafo.construir()
            
            print(" Inicializando generador de oraciones...")
            self.generador_oraciones = GeneradorGramatical(self.grafo)
            
            print(" Preparando motor SRS...")
            self.motor_srs = MotorSRS()
            
            print(" Configurando generador de retos...")
            self.generador_retos = GeneradorRetos(
                diccionario=self.diccionario,
                analizador=self.analizador,
                grafo=self.grafo,
                generador_oraciones=self.generador_oraciones,
                motor_srs=self.motor_srs
            )
            
            print(FormateadorTexto.exito("\n Sistema cargado exitosamente"))
            time.sleep(1)
            return True
            
        except Exception as e:
            self.logger.error(f"Error cargando sistema: {e}", exc_info=True)
            print(FormateadorTexto.error(f"\n Error: {e}"))
            return False
    
    def gestionar_usuario(self) -> bool:
        """
        Gestiona login/registro de usuario.
        
        :return: True si hay usuario activo
        """
        self.limpiar_pantalla()
        print(FormateadorTexto.crear_caja("GESTIÓN DE USUARIO", 50, '='))
        
        usuarios = PerfilUsuario.listar_usuarios()
        
        if usuarios:
            print("\n Usuarios existentes:")
            for i, uid in enumerate(usuarios, 1):
                try:
                    perfil = PerfilUsuario.cargar(uid)
                    if perfil:
                        print(f"  {i}. {perfil.nombre} (Nivel {perfil.nivel_cefr})")
                except:
                    print(f"  {i}. {uid}")
            
            print(f"  {len(usuarios) + 1}. Crear nuevo usuario")
            
            while True:
                opcion = input("\n Selecciona una opción: ").strip()
                
                valido, msg = Validadores.validar_numero(opcion, 1, len(usuarios) + 1)
                if not valido:
                    print(FormateadorTexto.error(f"❌ {msg}"))
                    continue
                
                opcion = int(opcion)
                
                if opcion <= len(usuarios):
                    # Cargar usuario existente
                    uid = usuarios[opcion - 1]
                    return self.cargar_usuario(uid)
                else:
                    # Crear nuevo usuario
                    return self.crear_usuario()
        else:
            print("\n No hay usuarios registrados.")
            return self.crear_usuario()
    
    def crear_usuario(self) -> bool:
        """
        Crea un nuevo usuario.
        
        :return: True si creación exitosa
        """
        print("\n" + FormateadorTexto.titulo("=== REGISTRO DE NUEVO USUARIO ==="))
        
        # Solicitar nombre
        while True:
            nombre = input("\n Nombre: ").strip()
            valido, msg = Validadores.validar_nombre(nombre)
            
            if not valido:
                print(FormateadorTexto.error(f" {msg}"))
                continue
            
            break
        
        # Crear perfil
        self.perfil = PerfilUsuario(nombre)
        self.progreso = SeguimientoProgreso(self.perfil.usuario_id)
        self.analizador_stats = AnalizadorEstadisticas(self.perfil, self.progreso)
        self.auditoria = AuditoriaUsuario(self.perfil.usuario_id)
        
        print(FormateadorTexto.exito(f"\n ¡Bienvenido/a, {nombre}!"))
        print(f" Tu ID de usuario es: {self.perfil.usuario_id}")
        
        # Guardar
        self.perfil.guardar()
        self.progreso.guardar()
        
        self.auditoria.registrar_inicio_sesion()
        
        time.sleep(2)
        return True
    
    def cargar_usuario(self, usuario_id: str) -> bool:
        """
        Carga un usuario existente.
        
        :param usuario_id: ID del usuario
        :return: True si carga exitosa
        """
        try:
            self.perfil = PerfilUsuario.cargar(usuario_id)
            self.progreso = SeguimientoProgreso.cargar(usuario_id)
            self.analizador_stats = AnalizadorEstadisticas(self.perfil, self.progreso)
            self.auditoria = AuditoriaUsuario(usuario_id)
            
            if not self.perfil:
                print(FormateadorTexto.error(" Error cargando usuario"))
                return False
            
            print(FormateadorTexto.exito(f"\n ¡Bienvenido/a de nuevo, {self.perfil.nombre}!"))
            
            # Mostrar info rápida
            print(f"\n Nivel: {self.perfil.nivel_cefr} ({self.perfil.nivel_actual})")
            print(f" Racha: {self.perfil.estadisticas['racha_actual']} días")
            
            self.auditoria.registrar_inicio_sesion()
            
            time.sleep(2)
            return True
            
        except Exception as e:
            self.logger.error(f"Error cargando usuario: {e}", exc_info=True)
            print(FormateadorTexto.error(f" Error: {e}"))
            return False
    
    def menu_principal(self):
        """Muestra el menú principal."""
        while self.ejecutando:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            
            print("\n" + FormateadorTexto.titulo("=== MENÚ PRINCIPAL ==="))
            print("\n1.  Practicar retos")
            print("2.  Ver estadísticas")
            print("3.  Progreso de palabras")
            print("4.   Configuración")
            print("5.  Ayuda")
            print("6.  Salir")
            
            opcion = input("\n Selecciona una opción: ").strip()
            
            if opcion == '1':
                self.menu_practica()
            elif opcion == '2':
                self.mostrar_estadisticas()
            elif opcion == '3':
                self.mostrar_progreso_palabras()
            elif opcion == '4':
                self.menu_configuracion()
            elif opcion == '5':
                self.mostrar_ayuda()
            elif opcion == '6':
                self.salir()
            else:
                print(FormateadorTexto.error("\n Opción inválida"))
                time.sleep(1)
    
    def menu_practica(self):
        """Menú de práctica de retos."""
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("=== PRÁCTICA ==="))
        
        print("\n1.  Sesión rápida (5 retos)")
        print("2.  Sesión completa (10 retos)")
        print("3.  Sesión personalizada")
        print("4.  Repasar palabras difíciles")
        print("5. ⬅  Volver")
        
        opcion = input("\n Selecciona una opción: ").strip()
        
        if opcion == '1':
            self.iniciar_sesion_practica(5)
        elif opcion == '2':
            self.iniciar_sesion_practica(10)
        elif opcion == '3':
            self.sesion_personalizada()
        elif opcion == '4':
            self.repasar_dificiles()
        elif opcion == '5':
            return
        else:
            print(FormateadorTexto.error("\n Opción inválida"))
            time.sleep(1)
    
    def iniciar_sesion_practica(self, num_retos: int):
        """
        Inicia una sesión de práctica.
        
        :param num_retos: Número de retos a practicar
        """
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo(f"=== SESIÓN DE PRÁCTICA ({num_retos} RETOS) ==="))
        # Iniciar sesión
        self.sesion_actual = EstadisticasSesion()
        # Generar retos
        print("\n Generando retos...")
        retos = self.generador_retos.generar_sesion_practica(
            nivel_usuario=self.perfil.nivel_actual,
            num_retos=num_retos
        )
        if not retos:
            print(FormateadorTexto.error(" No se pudieron generar retos"))
            input("\nPresiona Enter para continuar...")
            return
        print(FormateadorTexto.exito(f" {len(retos)} retos generados\n"))
        time.sleep(1)
        # Ejecutar retos
        for i, reto in enumerate(retos, 1):
            self.ejecutar_reto(reto, i, len(retos))
        # Resumen de sesión
        self.finalizar_sesion()
    def ejecutar_reto(self, reto, numero: int, total: int):
        """
        Ejecuta un reto individual.
        
        :param reto: Objeto del reto
        :param numero: Número del reto actual
        :param total: Total de retos
        """
        self.limpiar_pantalla()
        # Encabezado
        print(FormateadorTexto.crear_caja(f"RETO {numero}/{total}", 60, '='))
        # Generar y mostrar reto
        reto.iniciar()
        datos_reto = reto.generar()
        tipo = datos_reto.get('tipo_reto', 'desconocido')
        print(f"\n Tipo: {tipo.replace('_', ' ').title()}")
        print(f" Palabra objetivo: {reto.palabra_objetivo}")
        print("\n" + "─" * 60)
        print(f"\n {datos_reto.get('pregunta', '')}")
        # Mostrar contenido específico del reto
        if tipo == 'tarjetas' or tipo == 'tarjetas_inverso':
            self._mostrar_reto_tarjetas(datos_reto)
        elif tipo == 'formar_palabras':
            self._mostrar_reto_formar_palabras(datos_reto)
        elif tipo == 'completar_oracion':
            self._mostrar_reto_completar_oracion(datos_reto)
        elif tipo == 'ordenar_oracion':
            self._mostrar_reto_ordenar_oracion(datos_reto)
        elif tipo == 'traducir_oracion':
            self._mostrar_reto_traducir_oracion(datos_reto)
        # Procesar respuesta
        while not reto.completado:
            respuesta = input(f"\n Tu respuesta: ").strip()
            
            if not respuesta:
                print(FormateadorTexto.advertencia("  La respuesta no puede estar vacía"))
                continue
            
            resultado = reto.verificar(respuesta)
            
            # Mostrar resultado
            if resultado['correcto']:
                print(FormateadorTexto.exito(f"\n {resultado['mensaje']}"))
            else:
                print(FormateadorTexto.error(f"\n {resultado['mensaje']}"))
            
            if resultado['completado']:
                # Registrar en sesión
                tiempo = reto.obtener_tiempo_respuesta()
                self.sesion_actual.registrar_reto(
                    correcto=resultado['correcto'],
                    tiempo=tiempo,
                    palabra=reto.palabra_objetivo,
                    tipo=tipo
                )
                
                # Registrar en progreso
                self.progreso.actualizar_palabra(
                    palabra=reto.palabra_objetivo,
                    correcto=resultado['correcto'],
                    tiempo_segundos=tiempo,
                    quality=resultado.get('quality', 3)
                )
                
                # Actualizar SRS
                self.motor_srs.registrar_resultado(
                    palabra=reto.palabra_objetivo,
                    quality=resultado.get('quality', 3)
                )
                
                # Dar XP
                xp_ganado = resultado['puntaje']
                subio_nivel = self.perfil.actualizar_nivel(xp_ganado)
                
                if subio_nivel:
                    print(FormateadorTexto.exito(
                        f"\n ¡SUBISTE DE NIVEL! Ahora eres nivel {self.perfil.nivel_actual}"
                    ))
                    self.auditoria.registrar_subida_nivel(
                        self.perfil.nivel_actual - 1,
                        self.perfil.nivel_actual
                    )
                
                print(f"\n +{xp_ganado} XP")
                break
        
        input("\nPresiona Enter para continuar...")
    
    def _mostrar_reto_tarjetas(self, datos):
        """Muestra un reto de tarjetas."""
        if 'palabra' in datos:
            print(f"\n Palabra: {datos['palabra']}")
        elif 'pregunta_texto' in datos:
            print(f"\n Significado: {datos['pregunta_texto']}")
        
        print("\nOpciones:")
        for i, opcion in enumerate(datos['opciones']):
            print(f"  {i}. {opcion}")
    
    def _mostrar_reto_formar_palabras(self, datos):
        """Muestra un reto de formar palabras."""
        print(f"\n Letras: {datos['letras_texto']}")
        if datos.get('pista'):
            print(f" Pista: {datos['pista']}")
    
    def _mostrar_reto_completar_oracion(self, datos):
        """Muestra un reto de completar oración."""
        print(f"\n {datos['oracion']}")
        
        if datos.get('con_opciones') and datos.get('opciones'):
            print("\nOpciones:")
            for i, opcion in enumerate(datos['opciones']):
                print(f"  {i}. {opcion}")
    
    def _mostrar_reto_ordenar_oracion(self, datos):
        """Muestra un reto de ordenar oración."""
        print(f"\n Palabras: {datos['palabras_texto']}")
        print("\n(Escribe las palabras en el orden correcto)")
    
    def _mostrar_reto_traducir_oracion(self, datos):
        """Muestra un reto de traducir oración."""
        print(f"\n {datos['oracion']}")
        print(f"   ({datos['direccion']})")
    
    def finalizar_sesion(self):
        """Finaliza la sesión de práctica."""
        self.limpiar_pantalla()
        
        # Mostrar resumen
        self.sesion_actual.imprimir_resumen()
        
        # Registrar en perfil
        resumen = self.sesion_actual.obtener_resumen()
        self.perfil.registrar_sesion(
            duracion_minutos=resumen['duracion'],
            retos_completados=resumen['retos_completados'],
            precision=resumen['precision']
        )
        
        # Registrar en progreso
        self.progreso.registrar_sesion(
            tipo_reto='mixto',
            retos_completados=resumen['retos_completados'],
            precision=resumen['precision'],
            duracion=resumen['duracion']
        )
        
        # Auditoría
        self.auditoria.registrar_fin_sesion(
            duracion=resumen['duracion'],
            retos=resumen['retos_completados']
        )
        
        # Guardar
        self.perfil.guardar()
        self.progreso.guardar()
        
        input("\n Presiona Enter para continuar...")
    
    def mostrar_estadisticas(self):
        """Muestra las estadísticas del usuario."""
        self.limpiar_pantalla()
        
        # Generar resumen completo
        resumen = self.analizador_stats.generar_resumen_completo()
        print(resumen)
        
        # Recomendaciones
        analisis = self.analizador_stats.analizar_fortalezas_debilidades()
        if analisis['recomendaciones']:
            print("\n" + FormateadorTexto.titulo(" RECOMENDACIONES:"))
            for rec in analisis['recomendaciones']:
                print(f"  • {rec}")
        
        input("\n Presiona Enter para continuar...")
    
    def mostrar_progreso_palabras(self):
        """Muestra el progreso detallado de palabras."""
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("=== PROGRESO DE PALABRAS ==="))
        
        stats = self.progreso.obtener_estadisticas_generales()
        
        print(f"\n Total palabras practicadas: {stats['total_palabras']}")
        print(f" Aprendidas: {stats['palabras_aprendidas']}")
        print(f" Dominadas: {stats['palabras_dominadas']}")
        
        # Progreso por categoría
        print("\n" + FormateadorTexto.info("Progreso por categoría:"))
        for cat, datos in stats['progreso_categorias'].items():
            if datos['aprendidas'] > 0:
                print(f"  {cat.capitalize()}: {datos['aprendidas']} aprendidas, {datos['dominadas']} dominadas")
        
        # Palabras débiles
        debiles = self.progreso.obtener_palabras_debiles(5)
        if debiles:
            print("\n" + FormateadorTexto.advertencia(" Palabras que necesitan más práctica:"))
            for palabra in debiles:
                print(f"  • {palabra}")
        
        input("\n Presiona Enter para continuar...")
    
    def menu_configuracion(self):
        """Menú de configuración."""
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("=== CONFIGURACIÓN ==="))
        
        print(f"\n Objetivo diario: {self.perfil.preferencias['objetivo_diario']} retos")
        print(f" Temas favoritos: {', '.join(self.perfil.preferencias['temas_favoritos'])}")
        
        print("\n1. Cambiar objetivo diario")
        print("2. Volver")
        
        opcion = input("\n Selecciona una opción: ").strip()
        
        if opcion == '1':
            nuevo = input("\nNuevo objetivo diario (retos): ").strip()
            valido, msg = Validadores.validar_numero(nuevo, 1, 50)
            
            if valido:
                self.perfil.actualizar_preferencias(objetivo_diario=int(nuevo))
                self.perfil.guardar()
                print(FormateadorTexto.exito("\n Objetivo actualizado"))
            else:
                print(FormateadorTexto.error(f"\n {msg}"))
            
            time.sleep(2)
    
    def mostrar_ayuda(self):
        """Muestra la ayuda del sistema."""
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("=== AYUDA ==="))
        
        print("\n Este sistema te ayuda a aprender inglés mediante:")
        print("\n  • Tarjetas de vocabulario")
        print("  • Formación de palabras")
        print("  • Completar y ordenar oraciones")
        print("  • Traducción de oraciones")
        
        print("\n Consejos:")
        print("  • Practica todos los días para mantener tu racha")
        print("  • Repasa las palabras difíciles frecuentemente")
        print("  • Aumenta gradualmente la dificultad")
        
        input("\n Presiona Enter para continuar...")
    
    def sesion_personalizada(self):
        """
        Sesión de práctica personalizada.
        """
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("=== SESIÓN PERSONALIZADA ==="))
        print("\n Personaliza tu sesión de práctica:")
        # 1. Número de retos
        while True:
            num_retos = input("\n ¿Cuántos retos quieres practicar? (1-20): ").strip()
            valido, msg = Validadores.validar_numero(num_retos, 1, 20)
            if not valido:
                print(FormateadorTexto.error(f" {msg}"))
                continue
            num_retos = int(num_retos)
            break
        # 2. Tipo de retos
        print("\n ¿Qué tipos de retos prefieres?")
        print(" 1. Todos los tipos (recomendado)")
        print(" 2. Solo tarjetas de vocabulario")
        print(" 3. Solo formar palabras")
        print(" 4. Solo ejercicios con oraciones")
        print(" 5. Solo traducción")
        tipo_opcion = input("\n Selecciona (1-5): ").strip()
        tipos_map = {
            '1': None,  # Todos
            '2': ['tarjetas', 'tarjetas_inverso'],
            '3': ['formar_palabras', 'formar_palabras_multiple'],
            '4': ['completar_oracion', 'ordenar_oracion'],
            '5': ['traducir_oracion']
        }
        tipos_permitidos = tipos_map.get(tipo_opcion, None)
        # 3. Dificultad
        print("\n ¿Qué nivel de dificultad?")
        print(" 1. Automático (basado en tu nivel)")
        print(" 2. Fácil (A1-A2)")
        print(" 3. Intermedio (B1-B2)")
        print(" 4. Difícil (C1-C2)")
        dificultad_opcion = input("\n Selecciona (1-4): ").strip()
        dificultad_map = {
            '1': self.perfil.nivel_actual,  # Automático
            '2': 30,  # Fácil
            '3': 60,  # Intermedio
            '4': 80   # Difícil
        }
        nivel = dificultad_map.get(dificultad_opcion, self.perfil.nivel_actual)
        # 4. Temas específicos (opcional)
        print("\n ¿Quieres practicar algún tema específico?")
        print(" 1. No, cualquier tema")
        print(" 2. Comida y restaurantes")
        print(" 3. Trabajo y negocios")
        print(" 4. Salud y medicina")
        print(" 5. Educación y estudio")
        tema_opcion = input("\n Selecciona (1-5): ").strip()
        temas_map = {
            '1': None,  # Cualquier tema
            '2': ['food'],
            '3': ['work', 'business'],
            '4': ['health'],
            '5': ['education']
        }
        # Iniciar sesión
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo(f"=== INICIANDO SESIÓN PERSONALIZADA ==="))
        print(f"\n • Retos: {num_retos}")
        print(f" • Dificultad: 'Automática'")
        print(f" • Tipos: {tipo_opcion}")
        self.sesion_actual = EstadisticasSesion()
        # Generar retos personalizados
        print("\n Generando retos personalizados...")
        time.sleep(1)
        retos_generados = 0
        retos = []
        # Si se especificó tema, usar crear_reto_personalizado para cada reto
        if tema_opcion != '1' and tema_opcion in temas_map:
            tema = temas_map[tema_opcion]
            for i in range(num_retos):
                preferencias = {
                    'temas': tema,
                    'tipos_favoritos': tipos_permitidos,
                    'nivel': nivel
                }
                reto = self.generador_retos.crear_reto_personalizado(preferencias)
                if reto:
                    retos.append(reto)
                    retos_generados += 1
                    print(f" Reto {i+1}/{num_retos} generado ✓")
                else:
                    print(f" No se pudo generar reto {i+1}, usando alternativa...")
                    # Fallback: reto normal
                    reto_fallback = self.generador_retos.crear_reto(
                        tipo=random.choice(tipos_permitidos if tipos_permitidos else ['tarjetas']),
                        palabra=self._obtener_palabra_aleatoria(),
                        nivel_usuario=nivel
                    )
                    if reto_fallback:
                        retos.append(reto_fallback)
                        retos_generados += 1
        else:
            # Generar sesión normal con parámetros personalizados
            retos = self.generador_retos.generar_sesion_practica(
                nivel_usuario=nivel,
                num_retos=num_retos,
                tipos_permitidos=tipos_permitidos
            )
            retos_generados = len(retos) if retos else 0
        if retos_generados == 0:
            print(FormateadorTexto.error("\n No se pudieron generar retos con esos parámetros."))
            print(" Intenta con configuración más flexible.")
            input("\n Presiona Enter para continuar...")
            return
        print(FormateadorTexto.exito(f"\n {retos_generados} retos generados exitosamente!"))
        time.sleep(1.5)
        # Ejecutar retos
        for i, reto in enumerate(retos, 1):
            self.ejecutar_reto(reto, i, len(retos))
        # Finalizar sesión
        self.finalizar_sesion()

    def repasar_dificiles(self):
        """Repasa palabras difíciles."""
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("=== REPASO DE PALABRAS DIFÍCILES ==="))
        # Obtener palabras difíciles del progreso
        palabras_dificiles = self.progreso.obtener_palabras_debiles(limit=10)
        if not palabras_dificiles:
            print("\n ¡Excelente! No tienes palabras difíciles para repasar.")
            print(" Sigue practicando para mantener tu nivel.")
            input("\n Presiona Enter para continuar...")
            return
        print(f"\n Tienes {len(palabras_dificiles)} palabra(s) que necesitan repaso:")
        for i, palabra in enumerate(palabras_dificiles, 1):
            estado = self.progreso.palabras.get(palabra, {})
            veces_practicada = estado.get('veces_practicada', 0)
            veces_correcta = estado.get('veces_correcta', 0)
            if veces_practicada > 0:
                precision = (veces_correcta / veces_practicada) * 100
                print(f" {i}. {palabra} - {precision:.1f}% de precisión")
            else:
                print(f" {i}. {palabra} - Sin datos")
        # Preguntar cuántas palabras repasar
        print(f"\n ¿Cuántas palabras quieres repasar? (1-{len(palabras_dificiles)})")
        while True:
            num_repaso = input(f" Número: ").strip()
            valido, msg = Validadores.validar_numero(num_repaso, 1, len(palabras_dificiles))
            if not valido:
                print(FormateadorTexto.error(f" {msg}"))
                continue
            num_repaso = int(num_repaso)
            break
        # Seleccionar palabras a repasar
        palabras_a_repasar = palabras_dificiles[:num_repaso]
        # Elegir tipo de reto para el repaso
        print("\n ¿Cómo quieres repasar estas palabras?")
        print(" 1. Tarjetas de vocabulario (recomendado para repaso)")
        print(" 2. Formar palabras")
        print(" 3. Completar oraciones")
        print(" 4. Mezcla de todo")
        tipo_repaso = input("\n Selecciona (1-4): ").strip()
        tipo_map = {
            '1': 'tarjetas',
            '2': 'formar_palabras',
            '3': 'completar_oracion',
            '4': 'variado'
        }
        tipo_seleccionado = tipo_map.get(tipo_repaso, 'tarjetas')
        # Iniciar sesión de repaso
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo(f"=== INICIANDO REPASO ==="))
        print(f"\n Repasando {num_repaso} palabra(s) difíciles...")
        self.sesion_actual = EstadisticasSesion()
        # Crear y ejecutar retos para cada palabra difícil
        for i, palabra in enumerate(palabras_a_repasar, 1):
            print(f"\n Palabra {i}/{num_repaso}: {palabra}")
            # Determinar tipo de reto
            if tipo_seleccionado == 'variado':
                # Rotar entre tipos para variedad
                tipos = ['tarjetas', 'formar_palabras', 'completar_oracion']
                tipo = tipos[(i - 1) % len(tipos)]
            else:
                tipo = tipo_seleccionado
            # Crear reto
            try:
                reto = self.generador_retos.crear_reto(
                    tipo=tipo,
                    palabra=palabra,
                    nivel_usuario=self.perfil.nivel_actual
                )
                if reto:
                    self.ejecutar_reto(reto, i, num_repaso)
                else:
                    print(FormateadorTexto.error(f" No se pudo crear reto para '{palabra}'"))
                    continue
                    
            except Exception as e:
                print(FormateadorTexto.error(f" Error con '{palabra}': {e}"))
                continue
        # Mostrar resumen específico del repaso
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("=== RESUMEN DEL REPASO ==="))
        # Recalcular progreso de palabras repasadas
        mejoras = []
        for palabra in palabras_a_repasar:
            if palabra in self.progreso.palabras:
                estado = self.progreso.palabras[palabra]
                veces_practicada = estado.get('veces_practicada', 0)
                veces_correcta = estado.get('veces_correcta', 0)
                
                if veces_practicada > 0:
                    nueva_precision = (veces_correcta / veces_practicada) * 100
                    mejoras.append((palabra, nueva_precision))
        if mejoras:
            print("\n Progreso después del repaso:")
            for palabra, precision in mejoras:
                print(f" • {palabra}: {precision:.1f}% de precisión")
        # Recomendación
        if len(palabras_a_repasar) == len(palabras_dificiles):
            print("\n" + FormateadorTexto.exito("¡Repasaste todas tus palabras difíciles!"))
            print(" Vuelve mañana para seguir mejorando.")
        else:
            print(f"\n Te quedan {len(palabras_dificiles) - len(palabras_a_repasar)}")
            print(" palabras difíciles por repasar.")
        # Guardar progreso
        self.progreso.guardar()
        
        input("\n Presiona Enter para continuar...")

    def _obtener_palabra_aleatoria(self):
        """
        Obtiene una palabra aleatoria del diccionario.
        """
        try:
            todas_palabras = list(self.diccionario.data.get('palabras', {}).keys())
            if todas_palabras:
                return random.choice(todas_palabras)
        except:
            pass
        return "apple"  # Fallback
        
    def salir(self):
        """Sale de la aplicación."""
        self.limpiar_pantalla()
        print(FormateadorTexto.titulo("¡Hasta pronto! "))
        print(f"\n Progreso guardado para {self.perfil.nombre}")
        print(f" Racha actual: {self.perfil.estadisticas['racha_actual']} días")
        print(f" Nivel: {self.perfil.nivel_cefr} ({self.perfil.nivel_actual})")
        print("\n¡Sigue practicando para mejorar tu inglés! \n")
        
        self.ejecutando = False
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida."""
        print(FormateadorTexto.titulo("""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║          SISTEMA DE APRENDIZAJE DE INGLÉS              ║
║                                                        ║
║               ¡Aprende inglés de forma                 ║
║               interactiva y divertida!                 ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
        """))
    
    def mostrar_encabezado(self):
        """Muestra el encabezado con información del usuario."""
        print(FormateadorTexto.info("─" * 60))
        print(f"👤 {self.perfil.nombre} | Nivel {self.perfil.nivel_cefr} ({self.perfil.nivel_actual}) | "
            f"XP: {self.perfil.experiencia} |  {self.perfil.estadisticas['racha_actual']} días")
        print(FormateadorTexto.info("─" * 60))


def main():
    """Función principal."""
    try:
        app = InterfazCLI()
        app.iniciar()
    except KeyboardInterrupt:
        print("\n\n ¡Hasta pronto!")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()