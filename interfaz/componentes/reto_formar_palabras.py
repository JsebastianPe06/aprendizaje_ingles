"""
Widget para retos de formar palabras (anagramas).
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFrame, QGridLayout,
                            QScrollArea, QSizePolicy)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
import random

from .reto_base import RetoWidgetBase


class RetoFormarPalabrasWidget(RetoWidgetBase):
    """Widget para retos tipo formar palabras."""
    
    def __init__(self, reto_data, parent=None):
        self.letras = []
        self.letras_seleccionadas = []
        self.botones_letras = []
        super().__init__(reto_data, parent)
        self.setStyleSheet("background-color: white;")
    
    def _setup_ui_especifica(self):
        """Configura la UI específica para formar palabras."""
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
        pregunta_label = QLabel("Ordena las letras para formar una palabra:")
        pregunta_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        pregunta_label.setFont(pregunta_font)
        pregunta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pregunta_label.setWordWrap(True)
        pregunta_label.setStyleSheet("color: #1F2937; margin-bottom: 10px;")
        container_layout.addWidget(pregunta_label)
        
        # Pista si existe
        if 'pista' in self.reto_data and self.reto_data['pista']:
            pista_label = QLabel(f"Pista: {self.reto_data['pista']}")
            pista_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pista_label.setWordWrap(True)
            pista_label.setStyleSheet("""
                color: #F59E0B;
                font-size: 14px;
                font-style: italic;
                background-color: #FEF3C7;
                padding: 8px 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            """)
            container_layout.addWidget(pista_label)
        
        # Letras mezcladas
        self.letras = list(self.reto_data.get('letras', []))
        
        # Crear área de letras
        self._crear_area_letras(container_layout)
        
        # Área de palabra formada
        self._crear_area_palabra(container_layout)
        
        # Contador de letras
        num_letras = self.reto_data.get('num_letras', len(self.letras))
        contador_label = QLabel(f"La palabra tiene {num_letras} letras")
        contador_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contador_label.setStyleSheet("color: #6B7280; font-size: 13px; margin-top: 10px;")
        container_layout.addWidget(contador_label)
        
        # Indicador de letras extra
        if self.reto_data.get('tiene_letras_extra', False):
            extra_label = QLabel("Hay letras extra que no debes usar")
            extra_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            extra_label.setStyleSheet("""
                color: #F59E0B;
                font-size: 12px;
                margin-top: 5px;
            """)
            container_layout.addWidget(extra_label)
        
        container_layout.addStretch()
        
        # Establecer el widget contenedor en el scroll area
        scroll.setWidget(container)
        
        # Agregar el scroll area al layout del widget base
        self.content_layout.addWidget(scroll)
    
    def _crear_area_letras(self, parent_layout):
        """Crea el área con las letras mezcladas."""
        letras_widget = QWidget()
        letras_layout = QGridLayout(letras_widget)
        letras_layout.setSpacing(10)
        letras_layout.setContentsMargins(20, 20, 20, 20)
        
        # Crear botones para cada letra
        self.botones_letras = []
        
        for i, letra in enumerate(self.letras):
            btn = QPushButton(letra.upper())
            btn.setMinimumSize(60, 60)
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            
            # Estilo del botón
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2563EB;
                    color: white;
                    border-radius: 10px;
                    font-size: 24px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1D4ED8;
                }
                QPushButton:pressed {
                    background-color: #1E40AF;
                }
                QPushButton:disabled {
                    background-color: #9CA3AF;
                }
            """)
            
            # Conectar señal
            btn.clicked.connect(lambda checked, l=letra: self._agregar_letra(l))
            
            # Calcular posición en la grid
            fila = i // 6
            columna = i % 6
            
            letras_layout.addWidget(btn, fila, columna)
            self.botones_letras.append(btn)
        
        parent_layout.addWidget(letras_widget)
    
    def _crear_area_palabra(self, parent_layout):
        """Crea el área donde se muestra la palabra formada."""
        # Widget contenedor
        palabra_widget = QWidget()
        palabra_layout = QVBoxLayout(palabra_widget)
        palabra_layout.setSpacing(10)
        
        # Etiqueta
        etiqueta = QLabel("Palabra formada:")
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        etiqueta.setStyleSheet("color: #4B5563; font-size: 14px;")
        palabra_layout.addWidget(etiqueta)
        
        # Display de la palabra
        self.palabra_display = QLineEdit()
        self.palabra_display.setReadOnly(True)
        self.palabra_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.palabra_display.setMinimumHeight(60)
        self.palabra_display.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 3px solid #D1D5DB;
                border-radius: 12px;
                font-size: 24px;
                font-weight: bold;
                color: #1F2937;
                letter-spacing: 5px;
                padding: 10px;
            }
            QLineEdit:focus {
                border-color: #2563EB;
            }
        """)
        palabra_layout.addWidget(self.palabra_display)
        
        # Botones de control
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setSpacing(10)
        
        # Botón borrar última
        btn_borrar = QPushButton("⌫ Borrar última")
        btn_borrar.setFixedHeight(40)
        btn_borrar.setStyleSheet("""
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
        btn_borrar.clicked.connect(self._borrar_ultima)
        control_layout.addWidget(btn_borrar)
        
        # Botón reiniciar
        btn_reiniciar = QPushButton("Reiniciar")
        btn_reiniciar.setFixedHeight(40)
        btn_reiniciar.setStyleSheet("""
            QPushButton {
                background-color: #FEF3C7;
                color: #92400E;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FDE68A;
            }
        """)
        btn_reiniciar.clicked.connect(self._reiniciar_palabra)
        control_layout.addWidget(btn_reiniciar)
        
        palabra_layout.addWidget(control_widget)
        
        parent_layout.addWidget(palabra_widget)
    
    def _agregar_letra(self, letra):
        """Agrega una letra a la palabra formada."""
        if letra in self.letras:
            self.letras_seleccionadas.append(letra)
            self._actualizar_display()
            
            # Deshabilitar botón de la letra usada
            for btn in self.botones_letras:
                if btn.text().lower() == letra and btn.isEnabled():
                    btn.setEnabled(False)
                    break
    
    def _borrar_ultima(self):
        """Borra la última letra agregada."""
        if self.letras_seleccionadas:
            letra_borrada = self.letras_seleccionadas.pop()
            self._actualizar_display()
            
            # Rehabilitar botón de la letra
            for btn in self.botones_letras:
                if btn.text().lower() == letra_borrada:
                    btn.setEnabled(True)
                    break
    
    def _reiniciar_palabra(self):
        """Reinicia la palabra completa."""
        # Rehabilitar todos los botones
        for btn in self.botones_letras:
            btn.setEnabled(True)
        
        # Limpiar letras seleccionadas
        self.letras_seleccionadas.clear()
        self._actualizar_display()
    
    def _actualizar_display(self):
        """Actualiza el display de la palabra."""
        palabra = ''.join(self.letras_seleccionadas).upper()
        self.palabra_display.setText(palabra)
        self.respuesta_usuario = palabra.lower()
    
    def _validar_respuesta(self):
        """Valida que se haya formado una palabra."""
        if not self.respuesta_usuario or len(self.respuesta_usuario) == 0:
            self._mostrar_error("¡Debes formar una palabra primero!")
            return False
        
        # Validar longitud mínima
        num_letras = self.reto_data.get('num_letras', 3)
        if len(self.respuesta_usuario) < num_letras:
            self._mostrar_error(f"La palabra debe tener al menos {num_letras} letras")
            return False
        
        return True
    
    def _mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error temporal.
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
        self.content_layout.insertWidget(self.content_layout.count() - 1, error_label)
        
        # Remover después de 3 segundos
        QTimer.singleShot(3000, error_label.deleteLater)