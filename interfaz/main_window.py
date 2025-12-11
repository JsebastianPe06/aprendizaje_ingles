"""
Ventana principal de la aplicación.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QStackedWidget, QFrame, QMessageBox)
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QSize, pyqtSignal
import os

from interfaz.componentes.header import HeaderWidget
from interfaz.ventanas.login_window import LoginWindow
from interfaz.ventanas.practica_window import PracticaWindow
from interfaz.ventanas.estadisticas_window import EstadisticasWindow
from usuario.perfil import PerfilUsuario


class MainWindow(QMainWindow):
    """Ventana principal que maneja todas las vistas."""
    
    # Señales
    user_logged_in = pyqtSignal(object)  # Emite PerfilUsuario
    user_logged_out = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # Estado
        self.perfil = None
        self.is_logged_in = False
        # Configurar ventana
        self.setWindowTitle("ENGLISH_APP - Sistema de Aprendizaje de Inglés")
        self.setGeometry(100, 100, 1200, 800)
        # Crear widgets
        self._setup_ui()
        # Mostrar ventana de login inicial
        self.show_login()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Header (inicialmente oculto)
        self.header = HeaderWidget()
        self.header.hide()
        self.header.logout_requested.connect(self.logout)
        main_layout.addWidget(self.header)
        # Área de contenido (stacked widget)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        # Páginas
        self.login_page = LoginWindow()
        self.login_page.login_successful.connect(self.on_login_success)
        # Página de bienvenida (placeholder)
        self.welcome_page = self._create_welcome_page()
        self.practica_page = QWidget()
        # Agregar páginas al stack
        self.content_stack.addWidget(self.login_page)
        self.content_stack.addWidget(self.welcome_page)
        self.content_stack.addWidget(self.practica_page)

    
    def _create_welcome_page(self):
        """Crea la página de bienvenida."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Título
        title = QLabel("¡Bienvenido a ENGLISH_APP!")
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2563EB; margin-bottom: 20px;")
        layout.addWidget(title)
        # Mensaje
        message = QLabel("Selecciona una opción del menú para comenzar")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("color: #6B7280; font-size: 16px; margin-bottom: 40px;")
        layout.addWidget(message)
        # Botones de acción
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Botón Práctica Rápida
        btn_practica = QPushButton("Práctica Rápida")
        btn_practica.setFixedSize(200, 60)
        btn_practica.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #1E40AF;
            }
        """)
        btn_practica.clicked.connect(self._iniciar_practica)
        button_layout.addWidget(btn_practica)
        
        # Botón Estadísticas
        btn_stats = QPushButton("Estadísticas")
        btn_stats.setFixedSize(200, 60)
        btn_stats.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #0B8E63;
            }
        """)
        btn_stats.clicked.connect(self._mostrar_estadisticas)
        button_layout.addWidget(btn_stats)
        layout.addLayout(button_layout)
        return widget
    
    def show_login(self):
        """Muestra la página de login."""
        self.header.hide()
        self.content_stack.setCurrentWidget(self.login_page)
        self.is_logged_in = False
    
    def show_main_content(self):
        """Muestra el contenido principal después del login."""
        self.header.show()
        self.content_stack.setCurrentWidget(self.welcome_page)
        self.is_logged_in = True
    
    def on_login_success(self, perfil):
        """Maneja el login exitoso."""
        self.perfil = perfil
        self.header.update_user_info(perfil)
        self.show_main_content()
        
        # Emitir señal
        self.user_logged_in.emit(perfil)
    
    def logout(self):
        """Cierra la sesión del usuario."""
        self.perfil = None
        self.show_login()
        self.user_logged_out.emit()

    def _iniciar_practica(self):
        """Inicia una sesión de práctica."""
        # Verificar que los componentes del sistema estén cargados
        if not hasattr(self, 'generador_retos'):
            # Cargar componentes del sistema (similar a cli.py)
            try:
                self._cargar_componentes_sistema()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el sistema: {e}")
                return
        # Crear ventana de práctica
        practica_window = PracticaWindow(self.generador_retos, self.perfil, self)
        # Conectar señales
        practica_window.sesion_completada.connect(self._on_sesion_completada)
        practica_window.sesion_cancelada.connect(lambda: self.content_stack.setCurrentWidget(self.welcome_page))
        # Reemplazar página de práctica
        old_widget = self.content_stack.widget(2)  # Índice de práctica_page
        if old_widget:
            self.content_stack.removeWidget(old_widget)
            old_widget.deleteLater()
        self.content_stack.addWidget(practica_window)
        self.content_stack.setCurrentWidget(practica_window)
        if hasattr(self.header, 'add_back_button'):
            self.header.add_back_button(lambda: self._volver_a_inicio())
    
    def _cargar_componentes_sistema(self):
        """Carga los componentes del sistema (similar a cli.py)."""
        import os
        from lenguaje.diccionario import Diccionario
        from lenguaje.analizador import Analizador
        from lenguaje.categorias import ClasificadorCategorias
        from lenguaje.grafo_palabras import Grafo
        from lenguaje.generador_oraciones import GeneradorGramatical
        from lenguaje.motor_srs import MotorSRS
        from retos.generador import GeneradorRetos
        
        # Cargar diccionario
        ruta_json = os.path.join('data', 'a_p.json')
        if not os.path.exists(ruta_json):
            raise FileNotFoundError(f"No se encuentra el archivo: {ruta_json}")
        
        diccionario = Diccionario(ruta_json)
        
        # Inicializar analizador
        clasificador = ClasificadorCategorias()
        analizador = Analizador(diccionario, clasificador)
        
        # Construir grafo
        grafo = Grafo(ruta_json)
        grafo.construir()
        
        # Generador de oraciones
        generador_oraciones = GeneradorGramatical(grafo)
        
        # Motor SRS
        motor_srs = MotorSRS()
        
        # Generador de retos
        self.generador_retos = GeneradorRetos(
            diccionario=diccionario,
            analizador=analizador,
            grafo=grafo,
            generador_oraciones=generador_oraciones,
            motor_srs=motor_srs
        )
    
    def _on_sesion_completada(self, resultados):
        """Maneja la finalización de una sesión."""
        # Mostrar mensaje de éxito
        if resultados:
            precision = resultados.get('precision', 0)
            mensaje = f"¡Sesión completada!\nPrecisión: {precision:.1f}%"
            
            if precision >= 80:
                mensaje += "\n¡Excelente trabajo!"
            elif precision >= 60:
                mensaje += "\n¡Buen trabajo!"
            else:
                mensaje += "\n¡Sigue practicando!"
            
            QMessageBox.information(self, "Sesión Finalizada", mensaje)
        # Volver a página de bienvenida
        self.content_stack.setCurrentWidget(self._volver_a_inicio())

    def _mostrar_estadisticas(self):
        """Muestra la ventana de estadísticas."""
        # Cargar progreso del usuario
        try:
            from usuario.progreso import SeguimientoProgreso
            progreso = SeguimientoProgreso.cargar(self.perfil.usuario_id)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"No se pudo cargar el progreso: {e}")
            return
        # Crear ventana de estadísticas
        stats_window = EstadisticasWindow(self.perfil, progreso, self)
        # Reemplazar página actual
        old_widget = self.content_stack.widget(self.content_stack.currentIndex())
        if old_widget and old_widget != self.login_page:
            self.content_stack.removeWidget(old_widget)
        self.content_stack.addWidget(stats_window)
        self.content_stack.setCurrentWidget(stats_window)
        # Agregar botón de volver al header
        if hasattr(self.header, 'add_back_button'):
            self.header.add_back_button(lambda: self._volver_a_inicio())

    def closeEvent(self, event):
        """Maneja el cierre de la ventana."""
        # Guardar progreso si hay usuario logeado
        if self.perfil:
            try:
                self.perfil.guardar()
                print("Progreso guardado exitosamente")
            except Exception as e:
                print(f"Error guardando progreso: {e}")
        event.accept()

    def _volver_a_inicio(self):
        """Vuelve a la página de inicio."""
        current_widget = self.content_stack.currentWidget()
        if current_widget and current_widget != self.welcome_page:
            self.content_stack.removeWidget(current_widget)
            current_widget.deleteLater()
            # Restaurar página de bienvenida si no existe
            self.welcome_page = self._create_welcome_page()
            self.header.remove_back_button()
            if self.content_stack.indexOf(self.welcome_page) == -1:
                self.content_stack.addWidget(self.welcome_page)
            self.content_stack.setCurrentWidget(self.welcome_page)