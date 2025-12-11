"""
Aplicación principal PyQt6 para ENGLISH_APP
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QTimer

# Agregar el directorio raíz al path para importar módulos existentes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaz.main_window import MainWindow
from utils.loggers import LoggerConfig


class EnglishApp(QApplication):
    """Aplicación principal del sistema de aprendizaje de inglés."""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Configurar aplicación
        self.setApplicationName("LINGUALEARN")
        self.setApplicationDisplayName("Sistema de Aprendizaje de Inglés")
        self.setOrganizationName("EnglishLearning")
        
        # Configurar estilo global
        self.setStyle("Fusion")
        
        # Configurar fuente
        font = QFont("Segoe UI", 10)
        self.setFont(font)
        
        # Logger
        self.logger = LoggerConfig.configurar_logger('english_app_gui')
        
        # Ventana principal
        self.main_window = MainWindow()
        self.main_window.show()
        
        # Conectar señal de cierre
        self.aboutToQuit.connect(self._on_quit)
    
    def _on_quit(self):
        """Maneja el cierre de la aplicación."""
        self.logger.info("Aplicación finalizada")
    
    def load_stylesheet(self, theme="claro"):
        """Carga una hoja de estilos QSS."""
        try:
            stylesheet_path = os.path.join(
                os.path.dirname(__file__), 
                "estilos", 
                f"tema_{theme}.qss"
            )
            
            if os.path.exists(stylesheet_path):
                with open(stylesheet_path, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                self.setStyleSheet(stylesheet)
                self.logger.info(f"Tema '{theme}' cargado")
                return True
            else:
                self.logger.warning(f"Archivo de tema no encontrado: {stylesheet_path}")
                return False
        except Exception as e:
            self.logger.error(f"Error cargando tema: {e}")
            return False


def main():
    """Función principal para iniciar la aplicación."""
    try:
        # Crear aplicación
        app = EnglishApp(sys.argv)
        
        # Cargar tema por defecto
        app.load_stylesheet("claro")
        
        # Ejecutar loop principal
        exit_code = app.exec()
        
        return exit_code
        
    except Exception as e:
        print(f"Error fatal: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())