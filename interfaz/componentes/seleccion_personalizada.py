"""
Diálogo para configurar sesión personalizada de práctica.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QComboBox, QSpinBox, QFrame,
                            QButtonGroup, QRadioButton, QGroupBox,
                            QGridLayout, QDialog, QScrollArea, QSizePolicy)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal


class DialogoPersonalizado(QDialog):
    """Diálogo para configurar sesión personalizada."""
    
    # Señal que emite la configuración seleccionada
    configuracion_lista = pyqtSignal(dict)
    
    def __init__(self, perfil, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        
        self.perfil = perfil
        
        # Configurar ventana
        self.setWindowTitle("Sesión Personalizada")
        self.setMinimumSize(500, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)
        
        # Crear UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        # Crear área de desplazamiento principal
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
        
        # Widget contenedor
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Título
        title = QLabel("⚙️ Configurar Sesión Personalizada")
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("color: #1F2937;")
        main_layout.addWidget(title)
        
        # Información del usuario
        info_widget = QFrame()
        info_widget.setStyleSheet("""
            QFrame {
                background-color: #EFF6FF;
                border: 2px solid #DBEAFE;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(5)
        
        nivel_label = QLabel(f"👤 {self.perfil.nombre}")
        nivel_label.setStyleSheet("font-weight: bold; color: #1E40AF; font-size: 14px;")
        info_layout.addWidget(nivel_label)
        
        nivel_info = QLabel(f"Nivel actual: {self.perfil.nivel_cefr} (Nivel {self.perfil.nivel_actual})")
        nivel_info.setStyleSheet("color: #4B5563; font-size: 13px;")
        info_layout.addWidget(nivel_info)
        
        main_layout.addWidget(info_widget)
        
        # Selección de tipo de reto
        tipo_group = QGroupBox("🎯 Tipo de Reto")
        tipo_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #1F2937;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding-top: 20px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
            }
        """)
        
        tipo_layout = QVBoxLayout(tipo_group)
        tipo_layout.setSpacing(8)
        
        # Grupo de botones para tipos de reto
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        # Tipos de reto disponibles
        tipos_reto = [
            ("tarjetas", "Tarjetas de Vocabulario", "Aprende palabras nuevas"),
            ("tarjetas_inverso", "Tarjetas Inversas", "Fortalece el reconocimiento"),
            ("formar_palabras", "Formar Palabras", "Mejora la ortografía"),
            ("completar_oracion", "Completar Oración", "Practica en contexto"),
            ("ordenar_oracion", "Ordenar Oración", "Mejora la gramática"),
            ("traducir_oracion", "Traducir Oración", "Desarrollo de traducción")
        ]
        
        for tipo, nombre, desc in tipos_reto:
            tipo_widget = self._crear_opcion_tipo(tipo, nombre, desc)
            tipo_layout.addWidget(tipo_widget)
        
        main_layout.addWidget(tipo_group)
        
        # Configuración de cantidad
        config_group = QGroupBox("📊 Configuración")
        config_group.setStyleSheet(tipo_group.styleSheet())
        
        config_layout = QGridLayout(config_group)
        config_layout.setSpacing(15)
        config_layout.setColumnStretch(0, 1)
        config_layout.setColumnStretch(1, 2)
        
        # Cantidad de retos
        cantidad_label = QLabel("Número de retos:")
        cantidad_label.setStyleSheet("font-weight: bold; color: #4B5563;")
        config_layout.addWidget(cantidad_label, 0, 0)
        
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 50)
        self.spin_cantidad.setValue(10)
        self.spin_cantidad.setMinimumHeight(40)
        self.spin_cantidad.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.spin_cantidad.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 2px solid #D1D5DB;
                border-radius: 8px;
                font-size: 14px;
            }
            QSpinBox:focus {
                border-color: #2563EB;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
            }
        """)
        config_layout.addWidget(self.spin_cantidad, 0, 1)
        
        # Dificultad (información)
        dificultad_label = QLabel("Dificultad:")
        dificultad_label.setStyleSheet("font-weight: bold; color: #4B5563;")
        config_layout.addWidget(dificultad_label, 1, 0)
        
        dificultad_info = QLabel("Se ajustará automáticamente a tu nivel")
        dificultad_info.setWordWrap(True)
        dificultad_info.setStyleSheet("color: #6B7280; font-style: italic;")
        config_layout.addWidget(dificultad_info, 1, 1)
        
        main_layout.addWidget(config_group)
        
        # Botones
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(10)
        
        # Botón cancelar
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setFixedHeight(45)
        btn_cancelar.setStyleSheet("""
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
        btn_cancelar.clicked.connect(self.reject)
        buttons_layout.addWidget(btn_cancelar)
        
        # Botón iniciar
        self.btn_iniciar = QPushButton("🚀 Iniciar Sesión")
        self.btn_iniciar.setFixedHeight(45)
        self.btn_iniciar.setStyleSheet("""
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
        self.btn_iniciar.clicked.connect(self._iniciar_sesion)
        buttons_layout.addWidget(self.btn_iniciar)
        
        main_layout.addWidget(buttons_widget)
        
        main_layout.addStretch()
        
        # Establecer el widget contenedor en el scroll area
        main_scroll.setWidget(container)
        
        # Agregar el scroll area al layout del diálogo
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(main_scroll)
        
        # Seleccionar primer tipo por defecto
        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)
    
    def _crear_opcion_tipo(self, tipo, nombre, descripcion):
        """Crea un widget para una opción de tipo de reto."""
        widget = QWidget()
        widget.setMinimumHeight(70)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        widget.setObjectName(tipo)
        
        widget.setStyleSheet(f"""
            QWidget#{tipo} {{
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
            }}
            QWidget#{tipo}:hover {{
                border-color: #93C5FD;
                background-color: #F0F9FF;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Radio button
        radio_btn = QRadioButton()
        radio_btn.setFixedSize(20, 20)
        radio_btn.setStyleSheet("""
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #D1D5DB;
                border-radius: 9px;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #2563EB;
                border-radius: 9px;
                background-color: #2563EB;
            }
        """)
        
        self.button_group.addButton(radio_btn)
        
        # Información
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(3)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        nombre_label = QLabel(nombre)
        nombre_label.setWordWrap(True)
        nombre_label.setStyleSheet("font-weight: bold; color: #1F2937;")
        
        desc_label = QLabel(descripcion)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #6B7280; font-size: 12px;")
        
        info_layout.addWidget(nombre_label)
        info_layout.addWidget(desc_label)
        
        layout.addWidget(radio_btn)
        layout.addWidget(info_widget, 1)
        layout.addStretch()
        
        # Hacer clickable todo el widget
        widget.mousePressEvent = lambda e: radio_btn.setChecked(True)
        
        return widget
    
    def _iniciar_sesion(self):
        """Recoge la configuración y emite la señal."""
        tipo_seleccionado = None
        
        # Obtener tipo seleccionado
        for btn in self.button_group.buttons():
            if btn.isChecked():
                # Obtener el widget padre que tiene el ID como objectName
                widget_padre = btn.parentWidget()
                if widget_padre:
                    tipo_seleccionado = widget_padre.objectName()
                break
        
        if not tipo_seleccionado:
            return
        
        # Crear configuración
        config = {
            'tipo': tipo_seleccionado,
            'cantidad': self.spin_cantidad.value(),
            'dificultad': 'personalizada',
            'nivel_usuario': self.perfil.nivel_actual
        }
        
        # Emitir señal y cerrar
        self.configuracion_lista.emit(config)
        self.accept()