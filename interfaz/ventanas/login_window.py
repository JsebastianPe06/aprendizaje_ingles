"""
Ventana de login/registro de usuarios.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFrame, QStackedWidget,
                            QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QSize
import os

from usuario.perfil import PerfilUsuario
from utils.validadores import Validadores, FormateadorTexto


class LoginWindow(QWidget):
    """Ventana para login y registro de usuarios."""
    
    # Señales
    login_successful = pyqtSignal(object)  # Emite PerfilUsuario
    
    def __init__(self):
        super().__init__()
        
        # Configurar widget
        self.setStyleSheet("background-color: #F9FAFB;")
        
        # Crear UI
        self._setup_ui()
        
        # Cargar usuarios existentes
        self.load_existing_users()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header decorativo
        header = QWidget()
        header.setFixedHeight(200)
        header.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2563EB, stop: 1 #1D4ED8
            );
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Título
        title = QLabel("ENGLISH_APP")
        title_font = QFont("Segoe UI", 32, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Aprende inglés de forma interactiva")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header)
        
        # Contenido principal
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)
        
        # Stacked widget para login/registro
        self.stack = QStackedWidget()
        
        # Página de selección de usuario
        self.select_page = self._create_select_page()
        
        # Página de registro
        self.register_page = self._create_register_page()
        
        self.stack.addWidget(self.select_page)
        self.stack.addWidget(self.register_page)
        
        content_layout.addWidget(self.stack)
        
        main_layout.addWidget(content)
    
    def _create_select_page(self):
        """Crea la página de selección de usuario."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Selecciona un usuario")
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #1F2937;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Lista de usuarios
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                background-color: #807C7C;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #F3F4F6;
            }
            QListWidget::item:selected {
                background-color: #DBEAFE;
                border-radius: 5px;
            }
        """)
        self.user_list.itemDoubleClicked.connect(self.on_user_selected)
        layout.addWidget(self.user_list)
        
        # Botón nuevo usuario
        btn_new = QPushButton("➕ Crear nuevo usuario")
        btn_new.setFixedHeight(50)
        btn_new.setStyleSheet("""
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
        btn_new.clicked.connect(lambda: self.stack.setCurrentWidget(self.register_page))
        layout.addWidget(btn_new)
        
        return widget
    
    def _create_register_page(self):
        """Crea la página de registro."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Crear nuevo usuario")
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #1F2937;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Campo nombre
        name_layout = QVBoxLayout()
        name_layout.setSpacing(5)
        
        name_label = QLabel("Nombre:")
        name_label.setStyleSheet("color: #4B5563; font-weight: bold;")
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingresa tu nombre")
        self.name_input.setFixedHeight(45)
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #D1D5DB;
                border-radius: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2563EB;
            }
        """)
        name_layout.addWidget(self.name_input)
        
        layout.addLayout(name_layout)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Botón cancelar
        btn_cancel = QPushButton("⬅ Volver")
        btn_cancel.setFixedHeight(45)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #4B5563;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentWidget(self.select_page))
        buttons_layout.addWidget(btn_cancel)
        
        # Botón crear
        btn_create = QPushButton("Crear usuario")
        btn_create.setFixedHeight(45)
        btn_create.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:disabled {
                background-color: #93C5FD;
            }
        """)
        btn_create.clicked.connect(self.create_user)
        buttons_layout.addWidget(btn_create)
        
        layout.addLayout(buttons_layout)
        
        return widget
    
    def load_existing_users(self):
        """Carga los usuarios existentes en la lista."""
        usuarios = PerfilUsuario.listar_usuarios()
        
        if not usuarios:
            item = QListWidgetItem("No hay usuarios registrados")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.user_list.addItem(item)
            return
        
        for uid in usuarios:
            try:
                perfil = PerfilUsuario.cargar(uid)
                if perfil:
                    item_text = f"{perfil.nombre} - Nivel {perfil.nivel_cefr}"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.ItemDataRole.UserRole, uid)
                    self.user_list.addItem(item)
            except:
                item = QListWidgetItem(f"Usuario: {uid}")
                item.setData(Qt.ItemDataRole.UserRole, uid)
                self.user_list.addItem(item)
    
    def on_user_selected(self, item):
        """Maneja la selección de un usuario existente."""
        uid = item.data(Qt.ItemDataRole.UserRole)
        if uid:
            self.load_user(uid)
    
    def load_user(self, usuario_id):
        """Carga un usuario existente."""
        try:
            perfil = PerfilUsuario.cargar(usuario_id)
            if perfil:
                self.login_successful.emit(perfil)
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar el usuario")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando usuario: {str(e)}")
    
    def create_user(self):
        """Crea un nuevo usuario."""
        nombre = self.name_input.text().strip()
        
        # Validar
        valido, mensaje = Validadores.validar_nombre(nombre)
        
        if not valido:
            QMessageBox.warning(self, "Validación", mensaje)
            return
        
        try:
            # Crear perfil
            perfil = PerfilUsuario(nombre)
            perfil.guardar()
            
            # Crear progreso
            from usuario.progreso import SeguimientoProgreso
            progreso = SeguimientoProgreso(perfil.usuario_id)
            progreso.guardar()
            
            # Emitir señal de éxito
            self.login_successful.emit(perfil)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error creando usuario: {str(e)}")