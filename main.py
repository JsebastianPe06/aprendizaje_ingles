"""
Punto de entrada principal del sistema de aprendizaje de inglés.
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaz.cli import InterfazCLI, main as cli_main

if __name__ == '__main__':
    cli_main()