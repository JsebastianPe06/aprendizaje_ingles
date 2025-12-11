"""
Widget para retos de tarjetas de vocabulario.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QButtonGroup, QRadioButton, 
                            QGroupBox, QFrame, QScrollArea, QSizePolicy, QTextEdit)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

from .reto_base import RetoWidgetBase


class RetoTarjetasWidget(RetoWidgetBase):
    """Widget para retos tipo tarjeta de vocabulario."""
    
    def __init__(self, reto_data, parent=None):
        self.opciones = []
        self.button_group = None
        super().__init__(reto_data, parent)
        self.setStyleSheet("background-color: white;")
    
    def _setup_ui_especifica(self):
        """Configura la UI específica para tarjetas."""
        # Crear un área de desplazamiento principal
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setStyleSheet("""
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
        
        # Widget contenedor para todo el contenido
        content_container = QWidget()
        content_container_layout = QVBoxLayout(content_container)
        content_container_layout.setContentsMargins(20, 20, 20, 20)
        content_container_layout.setSpacing(15)
        
        # Pregunta
        pregunta = self.reto_data.get('pregunta', '¿Qué significa esta palabra?')
        
        pregunta_label = QLabel(pregunta)
        pregunta_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        pregunta_label.setFont(pregunta_font)
        pregunta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pregunta_label.setWordWrap(True)
        pregunta_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        pregunta_label.setStyleSheet("""
            color: #1F2937;
            margin-bottom: 15px;
            padding: 10px;
        """)
        content_container_layout.addWidget(pregunta_label)

        # Mostrar palabra si es tarjeta normal
        if 'palabra' in self.reto_data:
            palabra = self.reto_data['palabra']
            
            # Crear scroll area específica para la palabra
            palabra_scroll = QScrollArea()
            palabra_scroll.setWidgetResizable(True)
            palabra_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            palabra_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            palabra_scroll.setMaximumHeight(120)
            palabra_scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: #EFF6FF;
                    border-radius: 12px;
                }
            """)
            
            palabra_label = QLabel(palabra)
            palabra_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
            palabra_label.setFont(palabra_font)
            palabra_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            palabra_label.setWordWrap(True)
            palabra_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            palabra_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            palabra_label.setStyleSheet("""
                color: #2563EB;
                padding: 25px;
                min-height: 100px;
            """)
            
            palabra_scroll.setWidget(palabra_label)
            content_container_layout.addWidget(palabra_scroll)
        
        # Mostrar significado si es tarjeta inversa
        elif 'pregunta_texto' in self.reto_data:
            significado = self.reto_data['pregunta_texto']
            
            # Crear scroll area específica para el significado
            significado_scroll = QScrollArea()
            significado_scroll.setWidgetResizable(True)
            significado_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            significado_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            significado_scroll.setMaximumHeight(200)
            significado_scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: #F9FAFB;
                    border-radius: 12px;
                }
            """)
            
            significado_label = QLabel(significado)
            significado_font = QFont("Segoe UI", 18)
            significado_label.setFont(significado_font)
            significado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            significado_label.setWordWrap(True)
            significado_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            significado_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            significado_label.setStyleSheet("""
                color: #374151;
                border: 2px solid #E5E7EB;
                padding: 25px;
                font-style: italic;
                min-height: 100px;
            """)
            
            significado_scroll.setWidget(significado_label)
            content_container_layout.addWidget(significado_scroll)
        
        # Opciones de respuesta
        self.opciones = self.reto_data.get('opciones', [])
        
        if self.opciones:
            self._crear_opciones(content_container_layout)
        
        # Establecer el widget contenedor en el scroll area principal
        main_scroll.setWidget(content_container)
        
        # Agregar el scroll area principal al layout del widget base
        self.content_layout.addWidget(main_scroll)
    
    def _crear_opciones(self, parent_layout):
        """Crea los botones de opciones múltiples."""
        # Grupo para botones de radio
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        # Contenedor de opciones
        opciones_widget = QWidget()
        opciones_layout = QVBoxLayout(opciones_widget)
        opciones_layout.setSpacing(12)
        opciones_layout.setContentsMargins(20, 20, 20, 20)
        
        for i, opcion_texto in enumerate(self.opciones):
            # Crear widget para cada opción
            opcion_widget = QWidget()
            opcion_widget.setMinimumHeight(60)
            opcion_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            opcion_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 2px solid #E5E7EB;
                    border-radius: 10px;
                }
                QWidget:hover {
                    border-color: #93C5FD;
                    background-color: #F0F9FF;
                }
            """)
            
            opcion_layout = QHBoxLayout(opcion_widget)
            opcion_layout.setContentsMargins(15, 10, 15, 10)
            opcion_layout.setSpacing(15)
            
            # Radio button
            radio_btn = QRadioButton()
            radio_btn.setFixedSize(24, 24)
            radio_btn.setStyleSheet("""
                QRadioButton {
                    spacing: 15px;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                }
                QRadioButton::indicator:unchecked {
                    border: 2px solid #D1D5DB;
                    border-radius: 10px;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #2563EB;
                    border-radius: 10px;
                    background-color: #2563EB;
                }
            """)
            
            # Etiqueta de la opción con scroll si es necesario
            opcion_label_text = f"{chr(65 + i)}. {opcion_texto}"
            
            # Si la opción es muy larga, usar un QTextEdit en modo solo lectura
            if len(opcion_texto) > 50:
                opcion_label = QTextEdit()
                opcion_label.setPlainText(opcion_label_text)
                opcion_label.setReadOnly(True)
                opcion_label.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                opcion_label.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                opcion_label.setMaximumHeight(80)
                opcion_label.setStyleSheet("""
                    QTextEdit {
                        background-color: transparent;
                        border: none;
                        font-size: 15px;
                        color: #1F2937;
                        padding: 5px;
                        selection-background-color: #DBEAFE;
                    }
                    QScrollBar:vertical {
                        width: 8px;
                        background-color: transparent;
                    }
                    QScrollBar::handle:vertical {
                        background-color: #CBD5E1;
                        border-radius: 4px;
                        min-height: 20px;
                    }
                """)
                opcion_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            else:
                opcion_label = QLabel(opcion_label_text)
                opcion_label.setWordWrap(True)
                opcion_label.setStyleSheet("""
                    font-size: 15px;
                    color: #1F2937;
                    padding: 5px;
                """)
                opcion_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            
            opcion_layout.addWidget(radio_btn)
            opcion_layout.addWidget(opcion_label, 1)  # Factor de estiramiento 1
            opcion_layout.addStretch()
            
            # Agregar al grupo
            self.button_group.addButton(radio_btn, i)
            
            # Conectar click en el widget completo
            opcion_widget.mousePressEvent = lambda e, idx=i: self._seleccionar_opcion(idx)
            
            opciones_layout.addWidget(opcion_widget)
        
        parent_layout.addWidget(opciones_widget)
        
        # Indicador de selección única
        indicador = QLabel("Selecciona una opción")
        indicador.setAlignment(Qt.AlignmentFlag.AlignCenter)
        indicador.setWordWrap(True)
        indicador.setStyleSheet("""
            color: #6B7280;
            font-size: 13px;
            font-style: italic;
            margin-top: 5px;
            padding: 10px;
        """)
        parent_layout.addWidget(indicador)
    
    def _seleccionar_opcion(self, indice):
        """Selecciona una opción al hacer click en el widget."""
        botones = self.button_group.buttons()
        if 0 <= indice < len(botones):
            botones[indice].setChecked(True)
            self.respuesta_usuario = str(indice)
    
    def _validar_respuesta(self):
        """Valida que se haya seleccionado una opción."""
        if not self.button_group.checkedButton():
            # Mostrar mensaje de error
            error_label = QLabel("¡Debes seleccionar una opción!")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setWordWrap(True)
            error_label.setStyleSheet("""
                color: #EF4444;
                font-weight: bold;
                background-color: #FEE2E2;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 20px;
            """)
            
            # Insertar mensaje temporal
            for i in reversed(range(self.content_layout.count())):
                widget = self.content_layout.itemAt(i).widget()
                if widget and isinstance(widget, QScrollArea):
                    # Acceder al layout interno del scroll area
                    content_widget = widget.widget()
                    if content_widget:
                        content_layout = content_widget.layout()
                        content_layout.insertWidget(content_layout.count() - 1, error_label)
                        break
            
            # Remover después de 3 segundos
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(3000, error_label.deleteLater)
            
            return False
        
        self.respuesta_usuario = str(self.button_group.checkedId())
        return True