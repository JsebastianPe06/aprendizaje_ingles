"""
Ventana para repaso de palabras difíciles del usuario.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QScrollArea, QProgressBar,
                            QMessageBox, QSizePolicy)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, pyqtSignal
import math


class RepasoDificilesWindow(QWidget):
    """Ventana para repaso de palabras difíciles."""
    
    # Señales
    sesion_iniciada = pyqtSignal(list, int)  # Emite lista de palabras y número de retos
    
    def __init__(self, perfil, progreso, parent=None):
        super().__init__(parent)
        
        self.perfil = perfil
        self.progreso = progreso
        
        # Configurar ventana
        self.setStyleSheet("background-color: #F9FAFB;")
        
        # Crear UI
        self._setup_ui()
        
        # Cargar palabras difíciles
        self.cargar_palabras_dificiles()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._crear_header()
        main_layout.addWidget(header)
        
        # Área de contenido con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #F9FAFB;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F3F4F6;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #9CA3AF;
                border-radius: 5px;
                min-height: 20px;
            }
        """)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # Información
        info_widget = self._crear_widget_info()
        self.content_layout.addWidget(info_widget)
        
        # Lista de palabras
        self.lista_widget = self._crear_widget_lista()
        self.content_layout.addWidget(self.lista_widget)
        
        # Configuración
        config_widget = self._crear_widget_configuracion()
        self.content_layout.addWidget(config_widget)
        
        # Botones
        botones_widget = self._crear_widget_botones()
        self.content_layout.addWidget(botones_widget)
        
        self.content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def _crear_header(self):
        """Crea el header de la ventana."""
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #DC2626, stop: 1 #B91C1C
                );
            }
        """)
        
        layout = QVBoxLayout(header)
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Título
        title = QLabel("🎯 Repaso de Palabras Difíciles")
        title_font = QFont("Segoe UI", 22, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Enfócate en tus áreas de mejora")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 14px;")
        layout.addWidget(subtitle)
        
        return header
    
    def _crear_widget_info(self):
        """Crea el widget de información."""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #FECACA;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        # Título
        title = QLabel("📊 Análisis de tus palabras difíciles")
        title.setStyleSheet("font-weight: bold; color: #DC2626; font-size: 16px;")
        layout.addWidget(title)
        
        # Descripción
        desc = QLabel("""Estas son las palabras con las que has tenido más dificultad. 
        Practicarlas te ayudará a mejorar tu precisión general.""")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #6B7280; line-height: 1.5;")
        layout.addWidget(desc)
        
        return widget
    
    def _crear_widget_lista(self):
        """Crea el widget de lista de palabras."""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título de la sección
        section_title = QLabel("Palabras que necesitan práctica")
        section_title.setStyleSheet("""
            font-weight: bold;
            font-size: 16px;
            color: #1F2937;
            padding: 20px 20px 10px 20px;
        """)
        layout.addWidget(section_title)
        
        # Contenedor para las palabras
        self.palabras_container = QWidget()
        self.palabras_layout = QVBoxLayout(self.palabras_container)
        self.palabras_layout.setSpacing(10)
        self.palabras_layout.setContentsMargins(20, 10, 20, 20)
        
        layout.addWidget(self.palabras_container)
        
        return widget
    
    def _crear_widget_configuracion(self):
        """Crea el widget de configuración."""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("⚙️ Configurar sesión de repaso")
        title.setStyleSheet("font-weight: bold; color: #1F2937; font-size: 16px;")
        layout.addWidget(title)
        
        # Selección de cantidad
        cantidad_widget = QWidget()
        cantidad_layout = QHBoxLayout(cantidad_widget)
        cantidad_layout.setContentsMargins(0, 0, 0, 0)
        
        cantidad_label = QLabel("Número de retos:")
        cantidad_label.setStyleSheet("color: #4B5563; font-weight: bold;")
        cantidad_layout.addWidget(cantidad_label)
        
        cantidad_layout.addStretch()
        
        self.cantidad_info = QLabel("0")
        self.cantidad_info.setStyleSheet("color: #DC2626; font-weight: bold; font-size: 18px;")
        cantidad_layout.addWidget(self.cantidad_info)
        
        layout.addWidget(cantidad_widget)
        
        # Información
        info_label = QLabel("Se generarán retos variados con estas palabras")
        info_label.setStyleSheet("color: #6B7280; font-size: 13px; font-style: italic;")
        layout.addWidget(info_label)
        
        return widget
    
    def _crear_widget_botones(self):
        """Crea el widget con botones de acción."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(15)
        
        # Botón cancelar
        btn_cancelar = QPushButton("⬅ Volver")
        btn_cancelar.setFixedHeight(50)
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
        btn_cancelar.clicked.connect(self.close)
        layout.addWidget(btn_cancelar)
        
        # Botón iniciar
        self.btn_iniciar = QPushButton("🚀 Iniciar Repaso")
        self.btn_iniciar.setFixedHeight(50)
        self.btn_iniciar.setEnabled(False)
        self.btn_iniciar.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
            QPushButton:disabled {
                background-color: #FCA5A5;
            }
        """)
        self.btn_iniciar.clicked.connect(self._iniciar_repaso)
        layout.addWidget(self.btn_iniciar)
        
        return widget
    
    def cargar_palabras_dificiles(self):
        """Carga las palabras difíciles del usuario."""
        # Obtener palabras difíciles del progreso
        palabras_dificiles = self.progreso.obtener_palabras_debiles(limite=15)
        
        if not palabras_dificiles:
            # Mostrar mensaje si no hay palabras difíciles
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            empty_label = QLabel("🎉 ¡Excelente! No tienes palabras difíciles.")
            empty_label.setStyleSheet("""
                color: #10B981;
                font-weight: bold;
                font-size: 16px;
                padding: 30px;
                text-align: center;
            """)
            
            empty_layout.addWidget(empty_label)
            
            # Reemplazar layout de palabras
            for i in reversed(range(self.palabras_layout.count())):
                widget = self.palabras_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            self.palabras_layout.addWidget(empty_widget)
            self.btn_iniciar.setEnabled(False)
            return
        
        # Limpiar layout existente
        for i in reversed(range(self.palabras_layout.count())):
            widget = self.palabras_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Crear widgets para cada palabra difícil
        self.palabras_seleccionadas = []
        
        for i, palabra in enumerate(palabras_dificiles[:10]):  # Máximo 10 palabras
            palabra_widget = self._crear_widget_palabra(palabra, i)
            self.palabras_layout.addWidget(palabra_widget)
            self.palabras_seleccionadas.append(palabra)
        
        # Actualizar cantidad
        cantidad = min(len(palabras_dificiles), 10)
        self.cantidad_info.setText(str(cantidad))
        
        # Habilitar botón
        self.btn_iniciar.setEnabled(cantidad > 0)
    
    def _crear_widget_palabra(self, palabra, indice):
        """Crea un widget para mostrar una palabra difícil."""
        widget = QWidget()
        widget.setFixedHeight(60)
        
        # Color alternado para mejor visibilidad
        if indice % 2 == 0:
            bg_color = "#FEF2F2"
        else:
            bg_color = "#FEE2E2"
        
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border: 1px solid #FECACA;
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        
        # Número
        numero_label = QLabel(f"{indice + 1}.")
        numero_label.setStyleSheet("font-weight: bold; color: #DC2626;")
        layout.addWidget(numero_label)
        
        # Palabra
        palabra_label = QLabel(palabra)
        palabra_label.setStyleSheet("font-weight: bold; color: #1F2937; font-size: 14px;")
        layout.addWidget(palabra_label)
        
        layout.addStretch()
        
        # Información de progreso
        if palabra in self.progreso.palabras:
            estado = self.progreso.palabras[palabra]
            veces = estado.get('veces_practicada', 0)
            correctas = estado.get('veces_correcta', 0)
            
            if veces > 0:
                precision = (correctas / veces) * 100
                
                # Barra de progreso pequeña
                progress_bar = QProgressBar()
                progress_bar.setFixedWidth(100)
                progress_bar.setFixedHeight(8)
                progress_bar.setValue(int(precision))
                progress_bar.setTextVisible(False)
                progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #FCA5A5;
                        border-radius: 4px;
                        background-color: #FEE2E2;
                    }
                    QProgressBar::chunk {
                        background-color: #DC2626;
                        border-radius: 4px;
                    }
                """)
                
                layout.addWidget(progress_bar)
                
                # Porcentaje
                porcentaje_label = QLabel(f"{precision:.0f}%")
                porcentaje_label.setStyleSheet("color: #DC2626; font-size: 12px; font-weight: bold; min-width: 40px;")
                layout.addWidget(porcentaje_label)
        
        return widget
    
    def _iniciar_repaso(self):
        """Inicia la sesión de repaso."""
        if not self.palabras_seleccionadas:
            QMessageBox.warning(self, "Error", "No hay palabras seleccionadas para repasar.")
            return
        
        # Emitir señal con las palabras y cantidad
        cantidad = len(self.palabras_seleccionadas)
        self.sesion_iniciada.emit(self.palabras_seleccionadas, cantidad)
        self.close()