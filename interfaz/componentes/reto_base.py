"""
Widget base abstracto para todos los tipos de reto.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QProgressBar, QSizePolicy)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
import time


class RetoWidgetBase(QWidget):
    """
    Widget base que define la interfaz común para todos los retos.
    """
    
    # Señales
    respuesta_enviada = pyqtSignal(str)  # Emite la respuesta del usuario
    reto_completado = pyqtSignal(dict)   # Emite resultado completo
    tiempo_agotado = pyqtSignal()        # Emite cuando se acaba el tiempo
    
    def __init__(self, reto_data, parent=None):
        super().__init__(parent)
        
        # Datos del reto
        self.reto_data = reto_data
        self.palabra_objetivo = reto_data.get('palabra_objetivo', '')
        self.tipo_reto = reto_data.get('tipo_reto', '')
        self.nivel_dificultad = reto_data.get('nivel_dificultad', 'intermedio')
        
        # Estado
        self.respuesta_usuario = None
        self.completado = False
        self.correcto = False
        self.tiempo_inicio = None
        self.tiempo_limite = None
        self.tiempo_restante = None
        
        # Timer para límite de tiempo (opcional)
        self.timer = QTimer()
        self.timer.timeout.connect(self._actualizar_tiempo)
        
        # Configurar UI base
        self._setup_ui_base()
        
        # Configurar UI específica (implementada por subclases)
        self._setup_ui_especifica()
    
    def _setup_ui_base(self):
        """
        Configura la UI común a todos los retos.
        """
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.main_layout.setSpacing(15)
        
        # Header del reto
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Información del reto
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(2)
        
        # Tipo de reto
        self.tipo_label = QLabel(self._formatear_tipo_reto())
        tipo_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        self.tipo_label.setFont(tipo_font)
        self.tipo_label.setStyleSheet("color: #2563EB;")
        info_layout.addWidget(self.tipo_label)
        
        # Palabra objetivo
        self.palabra_label = QLabel(f"Palabra: {self.palabra_objetivo}")
        self.palabra_label.setStyleSheet("color: #6B7280; font-size: 14px;")
        info_layout.addWidget(self.palabra_label)
        
        header_layout.addWidget(info_widget)
        
        # Espaciador
        header_layout.addStretch()
        
        # Dificultad
        dificultad_widget = QWidget()
        dificultad_layout = QVBoxLayout(dificultad_widget)
        dificultad_layout.setSpacing(2)
        
        self.dificultad_label = QLabel(self._formatear_dificultad())
        self.dificultad_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dificultad_label.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 12px;
        """)
        
        # Color según dificultad
        if self.nivel_dificultad == "basico":
            self.dificultad_label.setStyleSheet(self.dificultad_label.styleSheet() + 
                "background-color: #10B981; color: white;")
        elif self.nivel_dificultad == "avanzado":
            self.dificultad_label.setStyleSheet(self.dificultad_label.styleSheet() + 
                "background-color: #EF4444; color: white;")
        else:
            self.dificultad_label.setStyleSheet(self.dificultad_label.styleSheet() + 
                "background-color: #F59E0B; color: white;")
        
        dificultad_layout.addWidget(self.dificultad_label)
        
        # Puntos
        self.puntos_label = QLabel("Puntos: 100")
        self.puntos_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.puntos_label.setStyleSheet("color: #6B7280; font-size: 12px;")
        dificultad_layout.addWidget(self.puntos_label)
        
        header_layout.addWidget(dificultad_widget)
        
        self.main_layout.addWidget(header_widget)
        
        # Línea separadora
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #E5E7EB;")
        self.main_layout.addWidget(separator)
        
        # Área de contenido (será llenada por subclases)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 10, 0, 10)
        self.main_layout.addWidget(self.content_widget)
        
        # Footer con botones
        self._setup_footer()
    
    def _setup_footer(self):
        """Configura el footer con botones de acción."""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 10, 0, 0)
        
        # Botón para enviar respuesta
        self.btn_enviar = QPushButton("Enviar respuesta")
        self.btn_enviar.setFixedHeight(45)
        self.btn_enviar.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:disabled {
                background-color: #93C5FD;
            }
        """)
        self.btn_enviar.clicked.connect(self._on_enviar_respuesta)
        footer_layout.addWidget(self.btn_enviar)
        
        # Botón para saltar (opcional)
        self.btn_omitir = QPushButton("Omitir")
        self.btn_omitir.setFixedHeight(45)
        self.btn_omitir.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        self.btn_omitir.clicked.connect(self._on_omitir)
        footer_layout.addWidget(self.btn_omitir)
        
        self.main_layout.addWidget(footer_widget)
    
    def _setup_ui_especifica(self):
        """
        Método abstracto que deben implementar las subclases
        para configurar la UI específica del tipo de reto.
        """
        raise NotImplementedError("Las subclases deben implementar este método")
    
    def _formatear_tipo_reto(self):
        """Formatea el tipo de reto para mostrar."""
        tipo_map = {
            'tarjetas': ' Tarjetas de vocabulario',
            'tarjetas_inverso': 'Tarjetas inversas',
            'formar_palabras': 'Formar palabras',
            'completar_oracion': 'Completar oración',
            'ordenar_oracion': 'Ordenar oración',
            'traducir_oracion': 'Traducir oración'
        }
        return tipo_map.get(self.tipo_reto, self.tipo_reto.replace('_', ' ').title())
    
    def _formatear_dificultad(self):
        """Formatea la dificultad para mostrar."""
        dificultad_map = {
            'basico': 'FÁCIL',
            'intermedio': 'INTERMEDIO',
            'avanzado': 'AVANZADO'
        }
        return dificultad_map.get(self.nivel_dificultad, self.nivel_dificultad.upper())
    
    def _on_enviar_respuesta(self):
        """Maneja el envío de respuesta."""
        if self._validar_respuesta():
            self.respuesta_enviada.emit(self.respuesta_usuario)
    
    def _on_omitir(self):
        """Maneja la omisión del reto."""
        self.respuesta_usuario = "_omitido_"
        self.respuesta_enviada.emit(self.respuesta_usuario)
    
    def _validar_respuesta(self):
        """
        Valida la respuesta antes de enviar.
        Retorna True si es válida.
        """
        return True  # Implementar en subclases
    
    def _actualizar_tiempo(self):
        """Actualiza el tiempo restante."""
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            # Actualizar UI del tiempo si existe
        else:
            self.timer.stop()
            self.tiempo_agotado.emit()
    
    def iniciar_temporizador(self, segundos):
        """Inicia un temporizador para el reto."""
        self.tiempo_limite = segundos
        self.tiempo_restante = segundos
        self.tiempo_inicio = time.time()
        
        if segundos > 0:
            self.timer.start(1000)  # Actualizar cada segundo
    
    def detener_temporizador(self):
        """Detiene el temporizador."""
        self.timer.stop()
    
    def obtener_tiempo_transcurrido(self):
        """Retorna el tiempo transcurrido en segundos."""
        if self.tiempo_inicio:
            return time.time() - self.tiempo_inicio
        return 0
    
    def mostrar_resultado(self, resultado):
        """
        Muestra el resultado de la respuesta.
        
        :param resultado: Diccionario con resultado de la verificación
        """
        self.completado = True
        self.correcto = resultado.get('correcto', False)
        
        # Deshabilitar botones
        self.btn_enviar.setEnabled(False)
        self.btn_omitir.setEnabled(False)
        
        # Mostrar mensaje
        mensaje = resultado.get('mensaje', '')
        
        # Crear widget de resultado
        resultado_widget = QWidget()
        resultado_layout = QVBoxLayout(resultado_widget)
        resultado_layout.setSpacing(10)
        
        # Icono según resultado
        icono_label = QLabel()
        icono_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if self.correcto:
            icono_label.setText("✅")
            resultado_widget.setStyleSheet("""
                background-color: #D1FAE5;
                border: 2px solid #10B981;
                border-radius: 10px;
                padding: 15px;
            """)
        else:
            icono_label.setText("❌")
            resultado_widget.setStyleSheet("""
                background-color: #FEE2E2;
                border: 2px solid #EF4444;
                border-radius: 10px;
                padding: 15px;
            """)
        
        icono_font = QFont("Segoe UI", 48)
        icono_label.setFont(icono_font)
        resultado_layout.addWidget(icono_label)
        
        # Mensaje
        mensaje_label = QLabel(mensaje)
        mensaje_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mensaje_label.setWordWrap(True)
        mensaje_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1F2937;
        """)
        resultado_layout.addWidget(mensaje_label)
        
        # Puntos obtenidos
        if 'puntaje' in resultado:
            puntos_label = QLabel(f"Puntos: {resultado['puntaje']}")
            puntos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            puntos_label.setStyleSheet("""
                font-size: 14px;
                color: #6B7280;
            """)
            resultado_layout.addWidget(puntos_label)
        
        # Insertar widget de resultado
        self.main_layout.insertWidget(3, resultado_widget)
        
        # Animación de entrada
        self._animar_resultado(resultado_widget)
    
    def _animar_resultado(self, widget):
        """Animación para mostrar el resultado."""
        animacion = QPropertyAnimation(widget, b"windowOpacity")
        animacion.setDuration(500)
        animacion.setStartValue(0)
        animacion.setEndValue(1)
        animacion.setEasingCurve(QEasingCurve.Type.OutCubic)
        animacion.start()
    
    def reset(self):
        """Reinicia el widget para un nuevo reto."""
        self.completado = False
        self.correcto = False
        self.respuesta_usuario = None
        self.tiempo_inicio = None
        
        # Restaurar botones
        self.btn_enviar.setEnabled(True)
        self.btn_omitir.setEnabled(True)
        
        # Limpiar resultado anterior
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget and widget != self.content_widget:
                widget.deleteLater()