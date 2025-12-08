"""
Módulo de perfil de usuario.
Maneja información personal, preferencias y configuración del usuario.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

class PerfilUsuario:
    """
    Gestiona el perfil completo del usuario:
    - Información personal
    - Preferencias de aprendizaje
    - Configuración del sistema
    - Historial de sesiones
    """
    
    def __init__(self, nombre: str, usuario_id: str = None):
        """
        Inicializa un perfil de usuario.
        
        :param nombre: Nombre del usuario
        :param usuario_id: ID único (se genera automáticamente si no se provee)
        """
        self.usuario_id = usuario_id or self._generar_id()
        self.nombre = nombre
        self.email = ""
        self.fecha_registro = datetime.now().isoformat()
        self.ultima_sesion = None
        
        # Nivel y progreso
        self.nivel_actual = 0  # 0-100
        self.nivel_cefr = "A1"  # A1, A2, B1, B2, C1, C2
        self.experiencia = 0
        
        # Preferencias
        self.preferencias = {
            'temas_favoritos': ['general'],
            'tipos_reto_favoritos': [],
            'dificultad_preferida': 'intermedio',
            'objetivo_diario': 5,  # número de retos por día
            'notificaciones': True,
            'modo_oscuro': False,
            'idioma_interfaz': 'es'
        }
        
        # Estadísticas generales
        self.estadisticas = {
            'total_sesiones': 0,
            'total_retos_completados': 0,
            'total_palabras_aprendidas': 0,
            'racha_actual': 0,  # días consecutivos
            'racha_maxima': 0,
            'tiempo_total_estudio': 0.0,  # minutos
            'precision_promedio': 0.0
        }
        
        # Objetivos y logros
        self.objetivos = {
            'objetivo_semanal': 25,
            'objetivo_mensual': 100,
            'progreso_semanal': 0,
            'progreso_mensual': 0
        }
        
        self.logros = []  # Lista de logros desbloqueados
        
    def _generar_id(self) -> str:
        """Genera un ID único para el usuario."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def actualizar_nivel(self, experiencia_ganada: int):
        """
        Actualiza el nivel del usuario basado en experiencia ganada.
        
        :param experiencia_ganada: Puntos de experiencia obtenidos
        """
        self.experiencia += experiencia_ganada
        
        # Calcular nuevo nivel (100 XP por nivel, escala cuadrática)
        nuevo_nivel = int((self.experiencia / 100) ** 0.8)
        nuevo_nivel = min(100, nuevo_nivel)  # Máximo nivel 100
        
        if nuevo_nivel > self.nivel_actual:
            self.nivel_actual = nuevo_nivel
            self._actualizar_nivel_cefr()
            return True  # Hubo subida de nivel
        
        return False
    
    def _actualizar_nivel_cefr(self):
        """Actualiza el nivel CEFR basado en el nivel numérico."""
        if self.nivel_actual < 15:
            self.nivel_cefr = "A1"
        elif self.nivel_actual < 30:
            self.nivel_cefr = "A2"
        elif self.nivel_actual < 50:
            self.nivel_cefr = "B1"
        elif self.nivel_actual < 70:
            self.nivel_cefr = "B2"
        elif self.nivel_actual < 85:
            self.nivel_cefr = "C1"
        else:
            self.nivel_cefr = "C2"
    
    def registrar_sesion(self, duracion_minutos: float, retos_completados: int,
                        precision: float):
        """
        Registra una sesión de práctica completada.
        
        :param duracion_minutos: Duración de la sesión
        :param retos_completados: Número de retos completados
        :param precision: Precisión promedio (0-100)
        """
        self.estadisticas['total_sesiones'] += 1
        self.estadisticas['total_retos_completados'] += retos_completados
        self.estadisticas['tiempo_total_estudio'] += duracion_minutos
        
        # Actualizar precisión promedio
        total = self.estadisticas['total_retos_completados']
        actual = self.estadisticas['precision_promedio']
        self.estadisticas['precision_promedio'] = (
            (actual * (total - retos_completados) + precision * retos_completados) / total
        )
        
        # Actualizar progreso de objetivos
        self.objetivos['progreso_semanal'] += retos_completados
        self.objetivos['progreso_mensual'] += retos_completados
        
        self.ultima_sesion = datetime.now().isoformat()
        
        # Actualizar racha
        self._actualizar_racha()
    
    def _actualizar_racha(self):
        """Actualiza la racha de días consecutivos."""
        if self.ultima_sesion:
            ultima = datetime.fromisoformat(self.ultima_sesion)
            hoy = datetime.now()
            diferencia = (hoy - ultima).days
            
            if diferencia == 0:
                # Mismo día, mantener racha
                pass
            elif diferencia == 1:
                # Día consecutivo
                self.estadisticas['racha_actual'] += 1
                if self.estadisticas['racha_actual'] > self.estadisticas['racha_maxima']:
                    self.estadisticas['racha_maxima'] = self.estadisticas['racha_actual']
            else:
                # Racha rota
                self.estadisticas['racha_actual'] = 1
    
    def agregar_logro(self, logro: str, descripcion: str = ""):
        """Agrega un logro al perfil."""
        if logro not in [l['nombre'] for l in self.logros]:
            self.logros.append({
                'nombre': logro,
                'descripcion': descripcion,
                'fecha': datetime.now().isoformat()
            })
            return True
        return False
    
    def actualizar_preferencias(self, **kwargs):
        """Actualiza las preferencias del usuario."""
        for key, value in kwargs.items():
            if key in self.preferencias:
                self.preferencias[key] = value
    
    def obtener_objetivo_diario_cumplido(self) -> bool:
        """Verifica si se cumplió el objetivo diario."""
        if self.ultima_sesion:
            ultima = datetime.fromisoformat(self.ultima_sesion)
            hoy = datetime.now()
            if (hoy - ultima).days == 0:
                # Contar retos de hoy
                return self.objetivos['progreso_semanal'] >= self.preferencias['objetivo_diario']
        return False
    
    def reiniciar_progreso_semanal(self):
        """Reinicia el progreso semanal."""
        self.objetivos['progreso_semanal'] = 0
    
    def reiniciar_progreso_mensual(self):
        """Reinicia el progreso mensual."""
        self.objetivos['progreso_mensual'] = 0
    
    def guardar(self, directorio: str = "data/usuarios"):
        """
        Guarda el perfil en un archivo JSON.
        
        :param directorio: Directorio donde guardar el perfil
        """
        os.makedirs(directorio, exist_ok=True)
        filepath = os.path.join(directorio, f"{self.usuario_id}.json")
        
        data = {
            'usuario_id': self.usuario_id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_registro': self.fecha_registro,
            'ultima_sesion': self.ultima_sesion,
            'nivel_actual': self.nivel_actual,
            'nivel_cefr': self.nivel_cefr,
            'experiencia': self.experiencia,
            'preferencias': self.preferencias,
            'estadisticas': self.estadisticas,
            'objetivos': self.objetivos,
            'logros': self.logros
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def cargar(cls, usuario_id: str, directorio: str = "data/usuarios"):
        """
        Carga un perfil desde un archivo JSON.
        
        :param usuario_id: ID del usuario a cargar
        :param directorio: Directorio donde buscar el perfil
        :return: Instancia de PerfilUsuario o None si no existe
        """
        filepath = os.path.join(directorio, f"{usuario_id}.json")
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        perfil = cls(data['nombre'], data['usuario_id'])
        perfil.email = data.get('email', '')
        perfil.fecha_registro = data.get('fecha_registro')
        perfil.ultima_sesion = data.get('ultima_sesion')
        perfil.nivel_actual = data.get('nivel_actual', 0)
        perfil.nivel_cefr = data.get('nivel_cefr', 'A1')
        perfil.experiencia = data.get('experiencia', 0)
        perfil.preferencias = data.get('preferencias', perfil.preferencias)
        perfil.estadisticas = data.get('estadisticas', perfil.estadisticas)
        perfil.objetivos = data.get('objetivos', perfil.objetivos)
        perfil.logros = data.get('logros', [])
        
        return perfil
    
    @staticmethod
    def listar_usuarios(directorio: str = "data/usuarios") -> List[str]:
        """
        Lista todos los IDs de usuarios guardados.
        
        :param directorio: Directorio donde buscar perfiles
        :return: Lista de IDs de usuario
        """
        if not os.path.exists(directorio):
            return []
        
        usuarios = []
        for filename in os.listdir(directorio):
            if filename.endswith('.json'):
                usuarios.append(filename[:-5])  # Remover .json
        
        return usuarios
    
    def __str__(self) -> str:
        """Representación en string del perfil."""
        return (
            f"Usuario: {self.nombre} ({self.usuario_id})\n"
            f"Nivel: {self.nivel_actual} ({self.nivel_cefr}) - XP: {self.experiencia}\n"
            f"Racha: {self.estadisticas['racha_actual']} días\n"
            f"Retos completados: {self.estadisticas['total_retos_completados']}\n"
            f"Precisión: {self.estadisticas['precision_promedio']:.1f}%"
        )