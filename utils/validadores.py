"""
Módulo de validadores para datos de entrada del usuario.
"""

import re
from typing import Any, Tuple

class Validadores:
    """
    Clase con métodos estáticos para validar diferentes tipos de entrada.
    """
    
    @staticmethod
    def validar_nombre(nombre: str) -> Tuple[bool, str]:
        """
        Valida un nombre de usuario.
        
        :param nombre: Nombre a validar
        :return: (válido, mensaje_error)
        """
        if not nombre or not nombre.strip():
            return False, "El nombre no puede estar vacío"
        
        nombre = nombre.strip()
        
        if len(nombre) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        # Permitir letras, números, espacios y caracteres acentuados
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            return False, "El nombre solo puede contener letras y espacios"
        
        return True, ""
    
    @staticmethod
    def validar_email(email: str) -> Tuple[bool, str]:
        """
        Valida un email.
        
        :param email: Email a validar
        :return: (válido, mensaje_error)
        """
        if not email or not email.strip():
            return True, ""  # Email es opcional
        
        email = email.strip()
        
        # Patrón básico de email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(patron, email):
            return False, "Email inválido"
        
        return True, ""
    
    @staticmethod
    def validar_numero(valor: Any, minimo: int = None, 
                      maximo: int = None) -> Tuple[bool, str]:
        """
        Valida un número entero.
        
        :param valor: Valor a validar
        :param minimo: Valor mínimo permitido
        :param maximo: Valor máximo permitido
        :return: (válido, mensaje_error)
        """
        try:
            numero = int(valor)
        except (ValueError, TypeError):
            return False, "Debe ser un número entero"
        
        if minimo is not None and numero < minimo:
            return False, f"El número debe ser al menos {minimo}"
        
        if maximo is not None and numero > maximo:
            return False, f"El número no puede exceder {maximo}"
        
        return True, ""
    
    @staticmethod
    def validar_opcion(valor: Any, opciones_validas: list) -> Tuple[bool, str]:
        """
        Valida que un valor esté dentro de opciones válidas.
        
        :param valor: Valor a validar
        :param opciones_validas: Lista de opciones válidas
        :return: (válido, mensaje_error)
        """
        if valor not in opciones_validas:
            opciones_str = ", ".join(map(str, opciones_validas))
            return False, f"Opción inválida. Opciones válidas: {opciones_str}"
        
        return True, ""
    
    @staticmethod
    def validar_nivel_dificultad(nivel: str) -> Tuple[bool, str]:
        """
        Valida un nivel de dificultad.
        
        :param nivel: Nivel a validar
        :return: (válido, mensaje_error)
        """
        niveles_validos = ['basico', 'intermedio', 'avanzado']
        return Validadores.validar_opcion(nivel.lower(), niveles_validos)
    
    @staticmethod
    def validar_tipo_reto(tipo: str) -> Tuple[bool, str]:
        """
        Valida un tipo de reto.
        
        :param tipo: Tipo de reto a validar
        :return: (válido, mensaje_error)
        """
        tipos_validos = [
            'tarjetas', 'tarjetas_inverso', 'formar_palabras',
            'completar_oracion', 'ordenar_oracion', 'traducir_oracion'
        ]
        return Validadores.validar_opcion(tipo, tipos_validos)
    
    @staticmethod
    def validar_respuesta_no_vacia(respuesta: str) -> Tuple[bool, str]:
        """
        Valida que una respuesta no esté vacía.
        
        :param respuesta: Respuesta a validar
        :return: (válido, mensaje_error)
        """
        if not respuesta or not respuesta.strip():
            return False, "La respuesta no puede estar vacía"
        
        return True, ""
    
    @staticmethod
    def normalizar_texto(texto: str) -> str:
        """
        Normaliza texto eliminando espacios extras y convirtiendo a minúsculas.
        
        :param texto: Texto a normalizar
        :return: Texto normalizado
        """
        if not texto:
            return ""
        
        # Eliminar espacios extras
        texto = " ".join(texto.split())
        return texto.strip()
    
    @staticmethod
    def validar_si_no(valor: str) -> Tuple[bool, str]:
        """
        Valida una respuesta sí/no.
        
        :param valor: Valor a validar
        :return: (válido, mensaje_error)
        """
        valor_lower = valor.lower().strip()
        opciones_si = ['s', 'si', 'sí', 'y', 'yes']
        opciones_no = ['n', 'no']
        
        if valor_lower in opciones_si or valor_lower in opciones_no:
            return True, ""
        
        return False, "Responde 'si' o 'no'"
    
    @staticmethod
    def interpretar_si_no(valor: str) -> bool:
        """
        Interpreta una respuesta sí/no como booleano.
        
        :param valor: Valor a interpretar
        :return: True si es afirmativo, False en caso contrario
        """
        valor_lower = valor.lower().strip()
        opciones_si = ['s', 'si', 'sí', 'y', 'yes']
        return valor_lower in opciones_si


class FormateadorTexto:
    """
    Clase para formatear texto en la consola.
    """
    
    # Códigos ANSI para colores
    COLORES = {
        'reset': '\033[0m',
        'negro': '\033[30m',
        'rojo': '\033[31m',
        'verde': '\033[32m',
        'amarillo': '\033[33m',
        'azul': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'blanco': '\033[37m',
        'negro_brillante': '\033[90m',
        'rojo_brillante': '\033[91m',
        'verde_brillante': '\033[92m',
        'amarillo_brillante': '\033[93m',
        'azul_brillante': '\033[94m',
        'magenta_brillante': '\033[95m',
        'cyan_brillante': '\033[96m',
        'blanco_brillante': '\033[97m'
    }
    
    ESTILOS = {
        'negrita': '\033[1m',
        'tenue': '\033[2m',
        'cursiva': '\033[3m',
        'subrayado': '\033[4m'
    }
    
    @staticmethod
    def colorear(texto: str, color: str, estilo: str = None) -> str:
        """
        Colorea un texto.
        
        :param texto: Texto a colorear
        :param color: Color a aplicar
        :param estilo: Estilo adicional (opcional)
        :return: Texto con código de color
        """
        codigo_color = FormateadorTexto.COLORES.get(color, '')
        codigo_estilo = FormateadorTexto.ESTILOS.get(estilo, '') if estilo else ''
        reset = FormateadorTexto.COLORES['reset']
        
        return f"{codigo_estilo}{codigo_color}{texto}{reset}"
    
    @staticmethod
    def exito(texto: str) -> str:
        """Formatea texto como éxito (verde)."""
        return FormateadorTexto.colorear(texto, 'verde_brillante', 'negrita')
    
    @staticmethod
    def error(texto: str) -> str:
        """Formatea texto como error (rojo)."""
        return FormateadorTexto.colorear(texto, 'rojo_brillante', 'negrita')
    
    @staticmethod
    def advertencia(texto: str) -> str:
        """Formatea texto como advertencia (amarillo)."""
        return FormateadorTexto.colorear(texto, 'amarillo_brillante')
    
    @staticmethod
    def info(texto: str) -> str:
        """Formatea texto como información (cyan)."""
        return FormateadorTexto.colorear(texto, 'cyan_brillante')
    
    @staticmethod
    def titulo(texto: str) -> str:
        """Formatea texto como título."""
        return FormateadorTexto.colorear(texto, 'magenta_brillante', 'negrita')
    
    @staticmethod
    def crear_caja(texto: str, ancho: int = 60, caracter: str = '=') -> str:
        """
        Crea una caja de texto.
        
        :param texto: Texto a encajar
        :param ancho: Ancho de la caja
        :param caracter: Carácter para los bordes
        :return: Texto en caja
        """
        lineas = []
        lineas.append(caracter * ancho)
        
        # Centrar texto
        padding = (ancho - len(texto) - 2) // 2
        linea_texto = f"{caracter}{' ' * padding}{texto}{' ' * padding}{caracter}"
        
        # Ajustar si el ancho es impar
        if len(linea_texto) < ancho:
            linea_texto += ' ' * (ancho - len(linea_texto) - 1) + caracter
        
        lineas.append(linea_texto)
        lineas.append(caracter * ancho)
        
        return '\n'.join(lineas)
    
    @staticmethod
    def crear_barra_progreso(progreso: float, ancho: int = 30, 
                            completo: str = '█', vacio: str = '░') -> str:
        """
        Crea una barra de progreso.
        
        :param progreso: Progreso (0.0 a 1.0)
        :param ancho: Ancho de la barra
        :param completo: Carácter para parte completa
        :param vacio: Carácter para parte vacía
        :return: Barra de progreso
        """
        progreso = max(0.0, min(1.0, progreso))
        completado = int(ancho * progreso)
        
        barra = completo * completado + vacio * (ancho - completado)
        porcentaje = int(progreso * 100)
        
        return f"[{barra}] {porcentaje}%"