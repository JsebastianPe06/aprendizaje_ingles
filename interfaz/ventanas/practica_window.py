"""
Ventana para sesiones de práctica con retos.
"""

import random

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QStackedWidget, QProgressBar,
                            QMessageBox)
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
import time

from interfaz.componentes.reto_factory import RetoWidgetFactory
from interfaz.componentes.seleccion_personalizada import DialogoPersonalizado
from interfaz.componentes.repaso_dificiles import RepasoDificilesWindow

class PracticaWindow(QWidget):
    """Ventana para sesiones de práctica con múltiples retos."""
    
    # Señales
    sesion_completada = pyqtSignal(dict)  # Emite resultados de la sesión
    sesion_cancelada = pyqtSignal()
    
    def __init__(self, generador_retos, perfil, parent=None):
        super().__init__(parent)
        
        # Componentes del sistema
        self.generador_retos = generador_retos
        self.perfil = perfil
        self.progreso = None  # Se establecerá más tarde
        
        # Estado de la sesión
        self.retos = []
        self.reto_actual = None
        self.indice_reto_actual = 0
        self.resultados = []
        self.sesion_iniciada = False
        self.tiempo_inicio_sesion = None
        
        # Widgets de reto
        self.reto_widget = None
        
        # Configurar UI
        self._setup_ui()
        
        # Conectar señales
        self._conectar_señales()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header de la sesión
        self.header_widget = self._crear_header()
        main_layout.addWidget(self.header_widget)
        
        # Área de contenido (stacked widget)
        self.content_stack = QStackedWidget()
        
        # Página de inicio
        self.inicio_page = self._crear_pagina_inicio()
        
        # Página de reto
        self.reto_page = self._crear_pagina_reto()
        
        # Página de resultados
        self.resultados_page = self._crear_pagina_resultados()
        
        self.content_stack.addWidget(self.inicio_page)
        self.content_stack.addWidget(self.reto_page)
        self.content_stack.addWidget(self.resultados_page)
        
        main_layout.addWidget(self.content_stack)
        
        # Inicialmente mostrar página de inicio
        self.content_stack.setCurrentWidget(self.inicio_page)
    
    def _crear_header(self):
        """Crea el header de la sesión."""
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 2px solid #E5E7EB;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Información del usuario
        user_widget = QWidget()
        user_layout = QVBoxLayout(user_widget)
        user_layout.setSpacing(2)
        
        self.user_name_label = QLabel(self.perfil.nombre)
        self.user_name_label.setStyleSheet("font-weight: bold; color: #1F2937;")
        
        self.user_level_label = QLabel(f"Nivel {self.perfil.nivel_cefr}")
        self.user_level_label.setStyleSheet("color: #6B7280; font-size: 12px;")
        
        user_layout.addWidget(self.user_name_label)
        user_layout.addWidget(self.user_level_label)
        
        layout.addWidget(user_widget)
        
        # Espaciador
        layout.addStretch()
        
        # Progreso de la sesión
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.setSpacing(2)
        
        self.progress_label = QLabel("Sesión no iniciada")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("color: #6B7280; font-size: 12px;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E5E7EB;
                border-radius: 4px;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #2563EB;
                border-radius: 2px;
            }
        """)
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_widget)
        
        # Espaciador
        layout.addStretch()
        
        return header
    
    def _crear_pagina_inicio(self):
        """Crea la página de inicio de sesión."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("🏁 Iniciar Sesión de Práctica")
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #1F2937;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Opciones de sesión
        options_widget = QWidget()
        options_layout = QVBoxLayout(options_widget)
        options_layout.setSpacing(15)
        options_layout.setContentsMargins(5, 0, 5, 0)
        
        # Sesión rápida (5 retos)
        btn_rapida = self._crear_boton_opcion("🚀 Práctica Rápida", "5 retos • 10-15 min", "#2563EB")
        btn_rapida.clicked.connect(lambda: self.iniciar_sesion(5))
        options_layout.addWidget(btn_rapida)
        
        # Sesión completa (10 retos)
        btn_completa = self._crear_boton_opcion("📚 Sesión Completa", "10 retos • 20-30 min", "#10B981")
        btn_completa.clicked.connect(lambda: self.iniciar_sesion(10))
        options_layout.addWidget(btn_completa)
        
        # Sesión personalizada
        btn_personalizada = self._crear_boton_opcion("⚙️ Personalizada", "Elige número y tipo", "#8B5CF6")
        btn_personalizada.clicked.connect(self._abrir_personalizada)
        options_layout.addWidget(btn_personalizada)
        
        # Repaso de palabras difíciles
        btn_dificiles = self._crear_boton_opcion("🎯 Repasar Difíciles", "Enfócate en tus debilidades", "#F59E0B")
        btn_dificiles.clicked.connect(self._repasar_dificiles)
        options_layout.addWidget(btn_dificiles)
        
        layout.addWidget(options_widget)
        
        return widget
    
    def _crear_boton_opcion(self, titulo, descripcion, color):
        """Crea un botón de opción de sesión."""
        btn = QPushButton()
        btn.setFixedHeight(80)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
                text-align: left;
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: {color}10;
                border-width: 3px;
            }}
        """)
        
        btn_layout = QVBoxLayout(btn)
        btn_layout.setSpacing(5)
        btn_layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        title_label = QLabel(titulo)
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {color};")
        
        # Descripción
        desc_label = QLabel(descripcion)
        desc_label.setStyleSheet("color: #6B7280; font-size: 13px;")
        
        btn_layout.addWidget(title_label)
        btn_layout.addWidget(desc_label)
        
        return btn
    
    def _crear_pagina_reto(self):
        """Crea la página donde se muestra un reto."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Este widget será llenado dinámicamente con el widget del reto
        self.reto_container = QWidget()
        reto_container_layout = QVBoxLayout(self.reto_container)
        reto_container_layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.reto_container)
        
        return widget
    
    def _crear_pagina_resultados(self):
        """Crea la página de resultados finales."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Este contenido será generado dinámicamente
        self.resultados_container = QWidget()
        resultados_layout = QVBoxLayout(self.resultados_container)
        resultados_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.resultados_container)
        
        # Botón para finalizar
        self.finalizar_btn = QPushButton("🏁 Finalizar Sesión")
        self.finalizar_btn.setFixedHeight(50)
        self.finalizar_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0DA271;
            }
        """)
        self.finalizar_btn.clicked.connect(self._finalizar_sesion)
        layout.addWidget(self.finalizar_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        return widget
    
    def _conectar_señales(self):
        """Conecta las señales internas."""
        # Las señales de los widgets de reto se conectarán dinámicamente
    
    def iniciar_sesion(self, num_retos):
        """Inicia una nueva sesión de práctica."""
        try:
            # Generar retos
            self.retos = self.generador_retos.generar_sesion_practica(
                nivel_usuario=self.perfil.nivel_actual,
                num_retos=num_retos
            )
            
            if not self.retos:
                QMessageBox.warning(self, "Error", "No se pudieron generar retos.")
                return
            
            # Inicializar estado
            self.indice_reto_actual = 0
            self.resultados = []
            self.sesion_iniciada = True
            self.tiempo_inicio_sesion = time.time()
            
            # Actualizar UI
            self.progress_label.setText(f"Reto 1/{len(self.retos)}")
            self.progress_bar.setMaximum(len(self.retos))
            self.progress_bar.setValue(0)
            
            # Mostrar primer reto
            self.mostrar_reto_actual()
            
            # Cambiar a página de reto
            self.content_stack.setCurrentWidget(self.reto_page)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error iniciando sesión: {str(e)}")
    
    def mostrar_reto_actual(self):
        """Muestra el reto actual."""
        if self.indice_reto_actual >= len(self.retos):
            self._mostrar_resultados()
            return
        
        # Obtener reto actual
        self.reto_actual = self.retos[self.indice_reto_actual]
        
        # Limpiar contenedor anterior
        for i in reversed(range(self.reto_container.layout().count())):
            widget = self.reto_container.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Crear widget para el reto
        try:
            self.reto_widget = RetoWidgetFactory.crear_widget_desde_reto(
                self.reto_actual,
                self.reto_container
            )
            
            # Conectar señales
            self.reto_widget.respuesta_enviada.connect(self._procesar_respuesta)
            self.reto_widget.tiempo_agotado.connect(self._on_tiempo_agotado)
            
            # Agregar al contenedor
            self.reto_container.layout().addWidget(self.reto_widget)
            
            # Actualizar progreso
            self.progress_label.setText(f"Reto {self.indice_reto_actual + 1}/{len(self.retos)}")
            self.progress_bar.setValue(self.indice_reto_actual)
            
        except Exception as e:
            print(f"Error creando widget de reto: {e}")
            # Saltar este reto
            self.indice_reto_actual += 1
            self.mostrar_reto_actual()
    
    def _procesar_respuesta(self, respuesta):
        """Procesa la respuesta del usuario."""
        if not self.reto_actual or not self.reto_widget:
            return
        
        try:
            # Verificar respuesta
            resultado = self.reto_actual.verificar(respuesta)
            
            # Agregar información adicional
            resultado['palabra'] = self.reto_actual.palabra_objetivo
            resultado['tipo_reto'] = self.reto_actual.__class__.__name__
            resultado['tiempo'] = self.reto_widget.obtener_tiempo_transcurrido()
            
            # Guardar resultado
            self.resultados.append(resultado)
            
            # Mostrar resultado en el widget
            self.reto_widget.mostrar_resultado(resultado)
            
            # Esperar 2 segundos y pasar al siguiente reto
            QTimer.singleShot(2000, self._siguiente_reto)
            
        except Exception as e:
            print(f"Error procesando respuesta: {e}")
            self._siguiente_reto()
    
    def _siguiente_reto(self):
        """Pasa al siguiente reto."""
        self.indice_reto_actual += 1
        
        if self.indice_reto_actual < len(self.retos):
            self.mostrar_reto_actual()
        else:
            self._mostrar_resultados()
    
    def _mostrar_resultados(self):
        """Muestra los resultados finales de la sesión."""
        # Calcular estadísticas
        total_retos = len(self.resultados)
        correctos = sum(1 for r in self.resultados if r.get('correcto', False))
        incorrectos = total_retos - correctos
        precision = (correctos / total_retos * 100) if total_retos > 0 else 0
        
        # Tiempo total
        tiempo_total = time.time() - self.tiempo_inicio_sesion if self.tiempo_inicio_sesion else 0
        
        # Limpiar contenedor de resultados
        for i in reversed(range(self.resultados_container.layout().count())):
            widget = self.resultados_container.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Crear contenido de resultados
        resultados_layout = QVBoxLayout()
        resultados_layout.setSpacing(20)
        resultados_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Título
        title = QLabel("🎉 Sesión Completada")
        title_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #10B981;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        resultados_layout.addWidget(title)
        
        # Estadísticas
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setSpacing(10)
        
        # Precisión
        precision_label = QLabel(f"Precisión: {precision:.1f}%")
        precision_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        precision_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1F2937;
        """)
        stats_layout.addWidget(precision_label)
        
        # Correctos/Incorrectos
        correctos_label = QLabel(f"✅ Correctos: {correctos} | ❌ Incorrectos: {incorrectos}")
        correctos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        correctos_label.setStyleSheet("font-size: 16px; color: #4B5563;")
        stats_layout.addWidget(correctos_label)
        
        # Tiempo
        tiempo_label = QLabel(f"⏱️ Tiempo total: {tiempo_total:.1f} segundos")
        tiempo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tiempo_label.setStyleSheet("font-size: 14px; color: #6B7280;")
        stats_layout.addWidget(tiempo_label)
        
        resultados_layout.addWidget(stats_widget)
        
        # Detalles por reto
        if total_retos > 0:
            detalles_label = QLabel("📋 Detalles por reto:")
            detalles_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F2937;")
            detalles_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            resultados_layout.addWidget(detalles_label)
            
            # Lista de resultados
            for i, resultado in enumerate(self.resultados, 1):
                reto_widget = self._crear_widget_resultado_reto(i, resultado)
                resultados_layout.addWidget(reto_widget)
        
        # Agregar layout al contenedor
        self.resultados_container.layout().addLayout(resultados_layout)
        
        # Cambiar a página de resultados
        self.content_stack.setCurrentWidget(self.resultados_page)
        
        # Emitir señal con resultados
        resultados_sesion = {
            'total_retos': total_retos,
            'correctos': correctos,
            'incorrectos': incorrectos,
            'precision': precision,
            'tiempo_total': tiempo_total,
            'detalles': self.resultados
        }
        self.sesion_completada.emit(resultados_sesion)
    
    def _crear_widget_resultado_reto(self, numero, resultado):
        """Crea un widget para mostrar el resultado de un reto individual."""
        widget = QWidget()
        widget.setFixedHeight(50)
        
        # Color según resultado
        if resultado.get('correcto', False):
            bg_color = "#D1FAE5"
            border_color = "#10B981"
            icon = "✅"
        else:
            bg_color = "#FEE2E2"
            border_color = "#EF4444"
            icon = "❌"
        
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Número e icono
        numero_label = QLabel(f"{numero}. {icon}")
        layout.addWidget(numero_label)
        
        # Palabra
        palabra = resultado.get('palabra', 'N/A')
        palabra_label = QLabel(palabra)
        palabra_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(palabra_label)
        
        # Espaciador
        layout.addStretch()
        
        # Puntos
        puntaje = resultado.get('puntaje', 0)
        puntos_label = QLabel(f"{puntaje} pts")
        layout.addWidget(puntos_label)
        
        # Tiempo
        tiempo = resultado.get('tiempo', 0)
        tiempo_label = QLabel(f"{tiempo:.1f}s")
        tiempo_label.setStyleSheet("color: #6B7280; font-size: 12px;")
        layout.addWidget(tiempo_label)
        
        return widget
    
    def _cancelar_sesion(self):
        """Cancela la sesión actual."""
        if self.sesion_iniciada:
            reply = QMessageBox.question(
                self, 'Cancelar Sesión',
                '¿Estás seguro de que quieres cancelar la sesión?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.sesion_cancelada.emit()
                self.content_stack.setCurrentWidget(self.inicio_page)
                self.sesion_iniciada = False
    
    def _finalizar_sesion(self):
        """Finaliza la sesión y regresa al menú principal."""
        self.sesion_completada.emit({})
    
    def _on_tiempo_agotado(self):
        """Maneja cuando se agota el tiempo en un reto."""
        if self.reto_widget and not self.reto_widget.completado:
            # Procesar como respuesta incorrecta
            self._procesar_respuesta("")

    def _abrir_personalizada(self):
        """Abre diálogo para sesión personalizada."""
        dialogo = DialogoPersonalizado(self.perfil, self)
        dialogo.configuracion_lista.connect(self._iniciar_sesion_personalizada)
        dialogo.exec()

    def _iniciar_sesion_personalizada(self, config):
        """Inicia una sesión personalizada basada en la configuración."""
        try:
            # Extraer configuración
            tipo_reto = config['tipo']
            cantidad = config['cantidad']
            nivel_usuario = config['nivel_usuario']
            
            # Obtener palabras pendientes del SRS
            palabras_pendientes = self.generador_retos.motor_srs.obtener_deberes()
            
            if len(palabras_pendientes) < cantidad:
                # Obtener más palabras del grafo según nivel
                from lenguaje.grafo_palabras import Grafo
                grafo = self.generador_retos.grafo
                
                # Obtener palabras del nivel apropiado
                palabras_nivel = []
                for categoria in ['sustantivo', 'verbo', 'adjetivo']:
                    palabras_cat = grafo.obtener_palabras_categoria(categoria)
                    palabras_nivel.extend(palabras_cat[:20])
                
                import random
                random.shuffle(palabras_nivel)
                adicionales = palabras_nivel[:cantidad - len(palabras_pendientes)]
                palabras_pendientes.extend(adicionales)
            
            # Limitar a la cantidad solicitada
            palabras_a_practicar = list(set(palabras_pendientes))[:cantidad]
            
            # Generar retos del tipo específico
            self.retos = []
            for palabra in palabras_a_practicar:
                reto = self.generador_retos.crear_reto(
                    tipo=tipo_reto,
                    palabra=palabra,
                    nivel_usuario=nivel_usuario
                )
                if reto:
                    self.retos.append(reto)
            
            if not self.retos:
                QMessageBox.warning(self, "Error", "No se pudieron generar retos del tipo seleccionado.")
                return
            
            # Iniciar sesión
            self._iniciar_sesion_con_retos()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error iniciando sesión personalizada: {str(e)}")

    def _repasar_dificiles(self):
        """Inicia sesión de repaso de palabras difíciles."""
        try:
            # Cargar progreso del usuario
            from usuario.progreso import SeguimientoProgreso
            progreso = SeguimientoProgreso.cargar(self.perfil.usuario_id)
            if not progreso:
                QMessageBox.information(self, "Información", "No hay datos de progreso disponibles.")
                return
            # Crear ventana de repaso
            repaso_window = RepasoDificilesWindow(self.perfil, progreso, self)
            repaso_window.sesion_iniciada.connect(self._iniciar_sesion_dificiles)
            repaso_window.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando palabras difíciles: {str(e)}")
    
    def _iniciar_sesion_dificiles(self, palabras, cantidad):
        """Inicia sesión con palabras difíciles."""
        try:
            if not palabras:
                QMessageBox.warning(self, "Error", "No hay palabras para repasar.")
                return
            # Generar retos variados para las palabras difíciles
            self.retos = []
            tipos_reto = ['tarjetas', 'tarjetas_inverso', 'formar_palabras', 'completar_oracion']
            for palabra in palabras:
                # Seleccionar tipo de reto aleatorio
                tipo = random.choice(tipos_reto)
                
                # Crear reto
                reto = self.generador_retos.crear_reto(
                    tipo=tipo,
                    palabra=palabra,
                    nivel_usuario=self.perfil.nivel_actual
                )
                
                if reto:
                    self.retos.append(reto)
            if not self.retos:
                QMessageBox.warning(self, "Error", "No se pudieron generar retos para las palabras seleccionadas.")
                return
            # Limitar a la cantidad solicitada
            if len(self.retos) > cantidad:
                self.retos = self.retos[:cantidad]
            # Iniciar sesión
            self._iniciar_sesion_con_retos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error iniciando sesión de repaso: {str(e)}")
    
    def _iniciar_sesion_con_retos(self):
        """Inicia sesión con los retos ya generados."""
        if not self.retos:
            return
        # Inicializar estado
        self.indice_reto_actual = 0
        self.resultados = []
        self.sesion_iniciada = True
        self.tiempo_inicio_sesion = time.time()
        # Actualizar UI
        self.progress_label.setText(f"Reto 1/{len(self.retos)}")
        self.progress_bar.setMaximum(len(self.retos))
        self.progress_bar.setValue(0)
        # Mostrar primer reto
        self.mostrar_reto_actual()
        # Cambiar a página de reto
        self.content_stack.setCurrentWidget(self.reto_page)