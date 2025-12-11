"""
Widget base para retos con oraciones (completar, ordenar, traducir).
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTextEdit, QLineEdit, QPushButton, QFrame,
                            QScrollArea, QSizePolicy, QButtonGroup, 
                            QRadioButton, QGroupBox)
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from .reto_base import RetoWidgetBase


class RetoOracionesWidgetBase(RetoWidgetBase):
    """
    Widget base para retos con oraciones.
    """
    
    def __init__(self, reto_data, parent=None):
        super().__init__(reto_data, parent)
        self.setStyleSheet("background-color: white;")
    
    def _setup_ui_especifica(self):
        """
        Configura la UI base para retos de oraciones.
        """
        # Este método será extendido por subclases específicas
        pass


class RetoCompletarOracionWidget(RetoOracionesWidgetBase):
    """
    Widget para retos de completar oraciones.
    """
    
    def __init__(self, reto_data, parent=None):
        self.con_opciones = False
        self.opciones = []
        self.button_group = None
        super().__init__(reto_data, parent)
    
    def _setup_ui_especifica(self):
        """
        Configura la UI específica para completar oraciones.
        """
        # Crear área de desplazamiento
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F3F4F6;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #9CA3AF;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6B7280;
            }
            QScrollBar:horizontal {
                height: 12px;
                background-color: #F3F4F6;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #9CA3AF;
                border-radius: 6px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #6B7280;
            }
        """)
        
        # Widget contenedor
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(15)
        
        # Pregunta
        pregunta_label = QLabel("Completa la oración con la palabra correcta:")
        pregunta_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        pregunta_label.setFont(pregunta_font)
        pregunta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pregunta_label.setWordWrap(True)
        pregunta_label.setStyleSheet("color: #1F2937; margin-bottom: 20px;")
        container_layout.addWidget(pregunta_label)
        
        # Oración con espacio en blanco
        oracion = self.reto_data.get('oracion', '')
        
        oracion_widget = QWidget()
        oracion_layout = QVBoxLayout(oracion_widget)
        oracion_layout.setContentsMargins(30, 20, 30, 20)
        
        oracion_label = QLabel(oracion)
        oracion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        oracion_label.setWordWrap(True)
        oracion_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        oracion_label.setStyleSheet("""
            font-size: 18px;
            color: #374151;
            line-height: 1.6;
            background-color: #F9FAFB;
            border-radius: 12px;
            padding: 25px;
            border: 2px dashed #D1D5DB;
        """)
        oracion_layout.addWidget(oracion_label)
        
        container_layout.addWidget(oracion_widget)
        
        # Determinar si hay opciones múltiples
        self.con_opciones = self.reto_data.get('con_opciones', False)
        self.opciones = self.reto_data.get('opciones', [])
        
        if self.con_opciones and self.opciones:
            self._crear_opciones(container_layout)
        else:
            self._crear_input_texto(container_layout)
        
        container_layout.addStretch()
        
        # Establecer el widget contenedor en el scroll area
        scroll.setWidget(container)
        
        # Agregar el scroll area al layout del widget base
        self.content_layout.addWidget(scroll)
    
    def _crear_opciones(self, parent_layout):
        """
        Crea opciones múltiples para completar.
        """
        opciones_widget = QWidget()
        opciones_layout = QVBoxLayout(opciones_widget)
        opciones_layout.setSpacing(8)
        opciones_layout.setContentsMargins(50, 20, 50, 20)
        
        self.button_group = QButtonGroup(self)
        
        for i, opcion in enumerate(self.opciones):
            opcion_widget = QWidget()
            opcion_widget.setMinimumHeight(50)
            opcion_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            opcion_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 2px solid #E5E7EB;
                    border-radius: 8px;
                }
                QWidget:hover {
                    border-color: #93C5FD;
                    background-color: #F0F9FF;
                }
            """)
            
            opcion_layout = QHBoxLayout(opcion_widget)
            opcion_layout.setContentsMargins(15, 0, 15, 0)
            
            radio_btn = QRadioButton()
            radio_btn.setFixedSize(20, 20)
            
            opcion_label = QLabel(opcion)
            opcion_label.setWordWrap(True)
            opcion_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            opcion_label.setStyleSheet("font-size: 15px; color: #1F2937;")
            
            opcion_layout.addWidget(radio_btn)
            opcion_layout.addWidget(opcion_label, 1)
            opcion_layout.addStretch()
            
            self.button_group.addButton(radio_btn, i)
            
            # Click en widget completo
            opcion_widget.mousePressEvent = lambda e, idx=i: self._seleccionar_opcion(idx)
            
            opciones_layout.addWidget(opcion_widget)
        
        parent_layout.addWidget(opciones_widget)
    
    def _crear_input_texto(self, parent_layout):
        """
        Crea un campo de texto para respuesta libre.
        """
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(50, 20, 50, 20)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Escribe la palabra que completa la oración...")
        self.text_input.setMinimumHeight(50)
        self.text_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.text_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px 15px;
                border: 2px solid #D1D5DB;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border-color: #2563EB;
            }
        """)
        
        input_layout.addWidget(self.text_input)
        parent_layout.addWidget(input_widget)
    
    def _seleccionar_opcion(self, indice):
        """
        Selecciona una opción.
        """
        if self.button_group:
            botones = self.button_group.buttons()
            if 0 <= indice < len(botones):
                botones[indice].setChecked(True)
                self.respuesta_usuario = self.opciones[indice]
    
    def _validar_respuesta(self):
        """
        Valida la respuesta.
        """
        if self.con_opciones:
            if not self.button_group.checkedButton():
                self._mostrar_error("¡Debes seleccionar una opción!")
                return False
            self.respuesta_usuario = self.opciones[self.button_group.checkedId()]
        else:
            respuesta = self.text_input.text().strip()
            if not respuesta:
                self._mostrar_error("¡Debes escribir una respuesta!")
                return False
            self.respuesta_usuario = respuesta
        
        return True
    
    def _mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error.
        """
        error_label = QLabel(mensaje)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("""
            color: #EF4444;
            font-weight: bold;
            background-color: #FEE2E2;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 50px;
        """)
        
        # Insertar mensaje
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget and isinstance(widget, QScrollArea):
                # Acceder al layout interno del scroll area
                content_widget = widget.widget()
                if content_widget:
                    content_layout = content_widget.layout()
                    content_layout.insertWidget(content_layout.count() - 1, error_label)
                    break
        
        QTimer.singleShot(3000, error_label.deleteLater)


class RetoOrdenarOracionWidget(RetoOracionesWidgetBase):
    """Widget para retos de ordenar oraciones."""
    
    def __init__(self, reto_data, parent=None):
        self.palabras = []
        self.palabras_seleccionadas = []
        self.botones_palabras = []
        super().__init__(reto_data, parent)
    
    def _setup_ui_especifica(self):
        """Configura la UI específica para ordenar oraciones."""
        # Crear área de desplazamiento
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F3F4F6;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #9CA3AF;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6B7280;
            }
            QScrollBar:horizontal {
                height: 12px;
                background-color: #F3F4F6;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #9CA3AF;
                border-radius: 6px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #6B7280;
            }
        """)
        
        # Widget contenedor
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(15)
        
        # Pregunta
        pregunta_label = QLabel("Ordena las palabras para formar una oración correcta:")
        pregunta_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        pregunta_label.setFont(pregunta_font)
        pregunta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pregunta_label.setWordWrap(True)
        pregunta_label.setStyleSheet("color: #1F2937; margin-bottom: 20px;")
        container_layout.addWidget(pregunta_label)
        
        # Palabras desordenadas
        self.palabras = self.reto_data.get('palabras', [])
        
        # Área de palabras disponibles
        self._crear_area_palabras(container_layout)
        
        # Área de oración formada
        self._crear_area_oracion(container_layout)
        
        # Información
        info_label = QLabel("💡 Arrastra o haz clic en las palabras para ordenarlas")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            color: #6B7280;
            font-size: 13px;
            font-style: italic;
            margin-top: 10px;
        """)
        container_layout.addWidget(info_label)
        
        container_layout.addStretch()
        
        # Establecer el widget contenedor en el scroll area
        scroll.setWidget(container)
        
        # Agregar el scroll area al layout del widget base
        self.content_layout.addWidget(scroll)
    
    def _crear_area_palabras(self, parent_layout):
        """Crea el área con las palabras desordenadas."""
        palabras_widget = QWidget()
        palabras_layout = QVBoxLayout(palabras_widget)
        palabras_layout.setSpacing(10)
        palabras_layout.setContentsMargins(20, 20, 20, 20)
        
        # Widget contenedor scrollable para las palabras
        palabras_scroll = QScrollArea()
        palabras_scroll.setWidgetResizable(True)
        palabras_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        palabras_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        palabras_scroll.setMaximumHeight(100)
        palabras_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                height: 8px;
                background-color: #F3F4F6;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background-color: #9CA3AF;
                border-radius: 4px;
                min-width: 30px;
            }
        """)
        
        # Contenedor interno para los botones
        palabras_container = QWidget()
        palabras_container_layout = QHBoxLayout(palabras_container)
        palabras_container_layout.setSpacing(10)
        palabras_container_layout.setContentsMargins(0, 0, 0, 0)
        palabras_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Crear botones para cada palabra
        self.botones_palabras = []
        
        for i, palabra in enumerate(self.palabras):
            btn = QPushButton(palabra)
            btn.setMinimumHeight(45)
            btn.setMinimumWidth(80)
            btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #10B981;
                    color: white;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    padding: 10px 15px;
                }
                QPushButton:hover {
                    background-color: #0DA271;
                }
                QPushButton:pressed {
                    background-color: #0B8E63;
                }
                QPushButton:disabled {
                    background-color: #9CA3AF;
                }
            """)
            
            btn.clicked.connect(lambda checked, p=palabra: self._agregar_palabra(p))
            
            palabras_container_layout.addWidget(btn)
            self.botones_palabras.append(btn)
        
        palabras_scroll.setWidget(palabras_container)
        palabras_layout.addWidget(palabras_scroll)
        
        parent_layout.addWidget(palabras_widget)
    
    def _crear_area_oracion(self, parent_layout):
        """Crea el área donde se muestra la oración formada."""
        oracion_widget = QWidget()
        oracion_layout = QVBoxLayout(oracion_widget)
        oracion_layout.setSpacing(15)
        
        # Etiqueta
        etiqueta = QLabel("Oración ordenada:")
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        etiqueta.setStyleSheet("color: #4B5563; font-size: 14px;")
        oracion_layout.addWidget(etiqueta)
        
        # Display de la oración
        self.oracion_display = QTextEdit()
        self.oracion_display.setReadOnly(True)
        self.oracion_display.setMinimumHeight(100)
        self.oracion_display.setMaximumHeight(150)
        self.oracion_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #D1D5DB;
                border-radius: 12px;
                font-size: 16px;
                color: #1F2937;
                padding: 15px;
            }
            QTextEdit:focus {
                border-color: #2563EB;
            }
        """)
        oracion_layout.addWidget(self.oracion_display)
        
        # Botones de control
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setSpacing(10)
        
        # Botón borrar última
        btn_borrar = QPushButton("Borrar última")
        btn_borrar.setFixedHeight(40)
        btn_borrar.clicked.connect(self._borrar_ultima)
        
        # Botón reiniciar
        btn_reiniciar = QPushButton("Reiniciar")
        btn_reiniciar.setFixedHeight(40)
        btn_reiniciar.clicked.connect(self._reiniciar_oracion)
        
        for btn in [btn_borrar, btn_reiniciar]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #F3F4F6;
                    color: #4B5563;
                    border-radius: 8px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #E5E7EB;
                }
                QPushButton:disabled {
                    color: #9CA3AF;
                }
            """)
            control_layout.addWidget(btn)
        
        oracion_layout.addWidget(control_widget)
        parent_layout.addWidget(oracion_widget)
    
    def _agregar_palabra(self, palabra):
        """
        Agrega una palabra a la oración.
        """
        self.palabras_seleccionadas.append(palabra)
        self._actualizar_display()
        
        # Deshabilitar botón de la palabra usada
        for btn in self.botones_palabras:
            if btn.text() == palabra and btn.isEnabled():
                btn.setEnabled(False)
                break
    
    def _borrar_ultima(self):
        """
        Borra la última palabra agregada.
        """
        if self.palabras_seleccionadas:
            palabra_borrada = self.palabras_seleccionadas.pop()
            self._actualizar_display()
            
            # Rehabilitar botón
            for btn in self.botones_palabras:
                if btn.text() == palabra_borrada:
                    btn.setEnabled(True)
                    break
    
    def _reiniciar_oracion(self):
        """
        Reinicia la oración completa.
        """
        for btn in self.botones_palabras:
            btn.setEnabled(True)
        
        self.palabras_seleccionadas.clear()
        self._actualizar_display()
    
    def _actualizar_display(self):
        """
        Actualiza el display de la oración.
        """
        oracion = ' '.join(self.palabras_seleccionadas)
        self.oracion_display.setPlainText(oracion)
        self.respuesta_usuario = oracion
    
    def _validar_respuesta(self):
        """
        Valida que se haya formado una oración.
        """
        if not self.respuesta_usuario or len(self.palabras_seleccionadas) == 0:
            self._mostrar_error("¡Debes formar una oración primero!")
            return False
        
        if len(self.palabras_seleccionadas) < len(self.palabras):
            self._mostrar_error(f"Usa todas las palabras ({len(self.palabras)} en total)")
            return False
        
        return True
    
    def _mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error.
        """
        error_label = QLabel(mensaje)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("""
            color: #EF4444;
            font-weight: bold;
            background-color: #FEE2E2;
            padding: 10px;
            border-radius: 8px;
            margin: 10px;
        """)
        
        # Insertar mensaje
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget and isinstance(widget, QScrollArea):
                # Acceder al layout interno del scroll area
                content_widget = widget.widget()
                if content_widget:
                    content_layout = content_widget.layout()
                    content_layout.insertWidget(content_layout.count() - 1, error_label)
                    break
        
        QTimer.singleShot(3000, error_label.deleteLater)