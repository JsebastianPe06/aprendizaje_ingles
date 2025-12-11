"""
Punto de entrada principal del sistema de aprendizaje de inglés.
"""
"""
Punto de entrada principal para ENGLISH_APP.
Permite elegir entre interfaz CLI o GUI.
"""
import sys
import os
import argparse


def run_gui():
    """Ejecuta la interfaz gráfica."""
    # Verificar si PyQt6 está instalado
    from interfaz.app import main as gui_main
    sys.exit(gui_main())


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='ENGLISH_APP - Sistema de aprendizaje de inglés')
    parser.add_argument('--gui', action='store_true', help='Usar interfaz gráfica (PyQt6)')
    
    args = parser.parse_args()
    
    print("Iniciando interfaz gráfica...")
    run_gui()


if __name__ == '__main__':
    main()