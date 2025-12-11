"""
Componente de cabecera con información del usuario.
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QVBoxLayout)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QSize


class HeaderWidget(QWidget):
    """Cabecera con información del usuario y controles."""
    
    # Señales
    logout_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.volver = False
        self.back_button = None
        
        # Configurar widget
        self.setFixedHeight(80)
        self.setStyleSheet("""
            HeaderWidget {
                background-color: #FFFFFF;
                border-bottom: 2px solid #E5E7EB;
            }
        """)
        
        # Crear UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Logo/Título a la izquierda
        title_label = QLabel("ENGLISH_APP")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2563EB;")
        layout.addWidget(title_label)
        
        # Espaciador
        layout.addStretch()
        
        # Información del usuario (centro)
        self.user_info_widget = QWidget()
        user_layout = QVBoxLayout(self.user_info_widget)
        user_layout.setSpacing(2)
        user_layout.setContentsMargins(0, 0, 0, 0)
        
        # Nombre y nivel
        self.name_label = QLabel("Usuario")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1F2937;
        """)
        
        self.level_label = QLabel("Nivel: A1")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_label.setStyleSheet("""
            font-size: 14px;
            color: #6B7280;
        """)
        
        user_layout.addWidget(self.name_label)
        user_layout.addWidget(self.level_label)
        
        layout.addWidget(self.user_info_widget)
        
        # Espaciador
        layout.addStretch()
        
        # Controles a la derecha
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setSpacing(10)
        
        # Botón logout
        btn_logout = QPushButton("👤 Cuenta")
        btn_logout.setFixedSize(130, 50)
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #23C6DB;
                border-radius: 20px;
                font-size: 18px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #FECACA;
            }
        """)
        btn_logout.clicked.connect(self.logout_requested.emit)
        controls_layout.addWidget(btn_logout)
        
        layout.addWidget(controls_widget)
    
    def update_user_info(self, perfil):
        """Actualiza la información del usuario en el header."""
        self.name_label.setText(perfil.nombre)
        self.level_label.setText(f"Nivel: {perfil.nivel_cefr} ({perfil.nivel_actual})")

    def add_back_button(self, callback):
        """Agrega un botón de volver al header."""
        # Crear botón de volver
        btn_back = QPushButton("⬅ Volver")
        btn_back.setFixedSize(100, 35)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #4B5563;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        btn_back.clicked.connect(callback)
        # Insertar al principio del layout
        self.layout().insertWidget(0, btn_back)
        self.back_button = btn_back
        self.volver = True

    def remove_back_button(self):
        """Elimina el botón de 'Volver' si existe."""
        if self.volver:
            self.layout().removeWidget(self.back_button)
            self.back_button = None
            self.volver = False