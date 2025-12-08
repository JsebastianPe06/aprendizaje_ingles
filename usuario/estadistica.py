"""
Módulo de estadísticas y análisis de rendimiento.
Genera reportes y visualizaciones del progreso del usuario.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from collections import defaultdict

class AnalizadorEstadisticas:
    """
    Analiza y genera reportes estadísticos sobre el rendimiento del usuario.
    """
    
    def __init__(self, perfil, progreso):
        """
        Inicializa el analizador.
        
        :param perfil: Instancia de PerfilUsuario
        :param progreso: Instancia de SeguimientoProgreso
        """
        self.perfil = perfil
        self.progreso = progreso
    
    def generar_reporte_diario(self) -> Dict[str, Any]:
        """Genera reporte del progreso de hoy."""
        hoy = datetime.now().date()
        
        # Filtrar sesiones de hoy
        sesiones_hoy = [
            s for s in self.progreso.historial_sesiones
            if datetime.fromisoformat(s['fecha']).date() == hoy
        ]
        
        if not sesiones_hoy:
            return {
                'fecha': hoy.isoformat(),
                'sesiones': 0,
                'retos_completados': 0,
                'tiempo_estudio': 0,
                'precision_promedio': 0,
                'objetivo_cumplido': False
            }
        
        retos = sum(s['retos_completados'] for s in sesiones_hoy)
        tiempo = sum(s['duracion'] for s in sesiones_hoy)
        precision = sum(s['precision'] for s in sesiones_hoy) / len(sesiones_hoy)
        
        objetivo = self.perfil.preferencias['objetivo_diario']
        
        return {
            'fecha': hoy.isoformat(),
            'sesiones': len(sesiones_hoy),
            'retos_completados': retos,
            'tiempo_estudio': round(tiempo, 1),
            'precision_promedio': round(precision, 1),
            'objetivo_cumplido': retos >= objetivo,
            'objetivo': objetivo
        }
    
    def generar_reporte_semanal(self) -> Dict[str, Any]:
        """Genera reporte de la última semana."""
        hoy = datetime.now()
        hace_semana = hoy - timedelta(days=7)
        
        # Filtrar sesiones de la última semana
        sesiones_semana = [
            s for s in self.progreso.historial_sesiones
            if datetime.fromisoformat(s['fecha']) >= hace_semana
        ]
        
        if not sesiones_semana:
            return {
                'periodo': 'última semana',
                'sesiones': 0,
                'retos_completados': 0,
                'tiempo_estudio': 0,
                'precision_promedio': 0,
                'dias_activos': 0
            }
        
        # Calcular métricas
        retos = sum(s['retos_completados'] for s in sesiones_semana)
        tiempo = sum(s['duracion'] for s in sesiones_semana)
        precision = sum(s['precision'] for s in sesiones_semana) / len(sesiones_semana)
        
        # Contar días únicos
        dias_unicos = len(set(
            datetime.fromisoformat(s['fecha']).date() 
            for s in sesiones_semana
        ))
        
        # Progreso por día
        retos_por_dia = defaultdict(int)
        for s in sesiones_semana:
            dia = datetime.fromisoformat(s['fecha']).date()
            retos_por_dia[dia] += s['retos_completados']
        
        return {
            'periodo': 'última semana',
            'sesiones': len(sesiones_semana),
            'retos_completados': retos,
            'tiempo_estudio': round(tiempo, 1),
            'precision_promedio': round(precision, 1),
            'dias_activos': dias_unicos,
            'promedio_retos_dia': round(retos / max(dias_unicos, 1), 1),
            'retos_por_dia': dict(retos_por_dia)
        }
    
    def generar_reporte_mensual(self) -> Dict[str, Any]:
        """Genera reporte del último mes."""
        hoy = datetime.now()
        hace_mes = hoy - timedelta(days=30)
        
        sesiones_mes = [
            s for s in self.progreso.historial_sesiones
            if datetime.fromisoformat(s['fecha']) >= hace_mes
        ]
        
        if not sesiones_mes:
            return {
                'periodo': 'último mes',
                'sesiones': 0,
                'retos_completados': 0,
                'tiempo_estudio': 0
            }
        
        retos = sum(s['retos_completados'] for s in sesiones_mes)
        tiempo = sum(s['duracion'] for s in sesiones_mes)
        precision = sum(s['precision'] for s in sesiones_mes) / len(sesiones_mes)
        
        dias_unicos = len(set(
            datetime.fromisoformat(s['fecha']).date() 
            for s in sesiones_mes
        ))
        
        return {
            'periodo': 'último mes',
            'sesiones': len(sesiones_mes),
            'retos_completados': retos,
            'tiempo_estudio': round(tiempo, 1),
            'precision_promedio': round(precision, 1),
            'dias_activos': dias_unicos,
            'consistencia': round((dias_unicos / 30) * 100, 1)
        }
    
    def analizar_fortalezas_debilidades(self) -> Dict[str, List]:
        """Analiza áreas fuertes y débiles del usuario."""
        return {
            'fortalezas': self.progreso.rendimiento.get('fortalezas', []),
            'debilidades': self.progreso.rendimiento.get('debilidades', []),
            'palabras_dificiles': self.progreso.rendimiento.get('palabras_dificiles', [])[:5],
            'recomendaciones': self._generar_recomendaciones()
        }
    
    def _generar_recomendaciones(self) -> List[str]:
        """Genera recomendaciones personalizadas."""
        recomendaciones = []
        
        # Analizar racha
        racha = self.perfil.estadisticas['racha_actual']
        if racha == 0:
            recomendaciones.append("¡Comienza una nueva racha! Practica hoy.")
        elif racha < 3:
            recomendaciones.append(f"¡Vas bien! Mantén tu racha de {racha} días.")
        else:
            recomendaciones.append(f"¡Excelente racha de {racha} días! Sigue así.")
        
        # Analizar precisión
        precision = self.perfil.estadisticas['precision_promedio']
        if precision < 60:
            recomendaciones.append("Tu precisión es baja. Intenta retos más fáciles.")
        elif precision < 80:
            recomendaciones.append("Buena precisión. Sigue practicando para mejorar.")
        else:
            recomendaciones.append("¡Excelente precisión! Prueba retos más difíciles.")
        
        # Analizar debilidades
        debilidades = self.progreso.rendimiento.get('debilidades', [])
        if debilidades:
            tipo = debilidades[0]['tipo']
            recomendaciones.append(f"Practica más retos de tipo '{tipo}'.")
        
        # Analizar palabras difíciles
        dificiles = self.progreso.rendimiento.get('palabras_dificiles', [])
        if dificiles:
            palabra = dificiles[0]['palabra']
            recomendaciones.append(f"Repasa la palabra '{palabra}'.")
        
        return recomendaciones
    
    def generar_grafico_progreso_texto(self, dias: int = 7) -> str:
        """Genera un gráfico ASCII del progreso."""
        hoy = datetime.now()
        
        # Obtener datos de los últimos N días
        datos_dias = []
        for i in range(dias - 1, -1, -1):
            dia = (hoy - timedelta(days=i)).date()
            
            sesiones_dia = [
                s for s in self.progreso.historial_sesiones
                if datetime.fromisoformat(s['fecha']).date() == dia
            ]
            
            retos = sum(s['retos_completados'] for s in sesiones_dia)
            datos_dias.append((dia, retos))
        
        if not any(r for _, r in datos_dias):
            return "Sin datos para mostrar"
        
        # Crear gráfico ASCII
        max_retos = max(r for _, r in datos_dias) if datos_dias else 1
        altura = 10
        
        lineas = []
        lineas.append("\nProgreso últimos {} días:".format(dias))
        lineas.append("─" * 50)
        
        for nivel in range(altura, 0, -1):
            umbral = (max_retos / altura) * nivel
            linea = f"{int(umbral):3d} │"
            
            for _, retos in datos_dias:
                if retos >= umbral:
                    linea += " █"
                else:
                    linea += "  "
            
            lineas.append(linea)
        
        # Eje X
        lineas.append("    └" + "──" * dias)
        
        # Etiquetas de fecha
        etiquetas = "     "
        for dia, _ in datos_dias:
            etiquetas += f"{dia.day:2d}"
        lineas.append(etiquetas)
        
        return "\n".join(lineas)
    
    def obtener_metricas_comparativas(self) -> Dict[str, Any]:
        """Obtiene métricas comparativas del usuario."""
        # Comparar con semana anterior
        hoy = datetime.now()
        esta_semana = hoy - timedelta(days=7)
        semana_anterior = hoy - timedelta(days=14)
        
        sesiones_esta = [
            s for s in self.progreso.historial_sesiones
            if esta_semana <= datetime.fromisoformat(s['fecha']) <= hoy
        ]
        
        sesiones_anterior = [
            s for s in self.progreso.historial_sesiones
            if semana_anterior <= datetime.fromisoformat(s['fecha']) < esta_semana
        ]
        
        retos_esta = sum(s['retos_completados'] for s in sesiones_esta)
        retos_anterior = sum(s['retos_completados'] for s in sesiones_anterior)
        
        cambio_retos = retos_esta - retos_anterior
        cambio_porcentaje = (
            (cambio_retos / retos_anterior * 100) 
            if retos_anterior > 0 else 0
        )
        
        return {
            'retos_esta_semana': retos_esta,
            'retos_semana_anterior': retos_anterior,
            'cambio': cambio_retos,
            'cambio_porcentaje': round(cambio_porcentaje, 1),
            'tendencia': 'mejorando' if cambio_retos > 0 else 'estable' if cambio_retos == 0 else 'bajando'
        }
    
    def generar_resumen_completo(self) -> str:
        """Genera un resumen completo en texto."""
        lineas = []
        
        lineas.append("=" * 60)
        lineas.append(f"  RESUMEN DE PROGRESO - {self.perfil.nombre}")
        lineas.append("=" * 60)
        
        # Información general
        lineas.append(f"\n📊 NIVEL: {self.perfil.nivel_cefr} (Nivel {self.perfil.nivel_actual})")
        lineas.append(f"⚡ EXPERIENCIA: {self.perfil.experiencia} XP")
        lineas.append(f"🔥 RACHA: {self.perfil.estadisticas['racha_actual']} días")
        
        # Estadísticas generales
        stats = self.progreso.obtener_estadisticas_generales()
        lineas.append(f"\n📚 PALABRAS:")
        lineas.append(f"   Total practicadas: {stats['total_palabras']}")
        lineas.append(f"   Aprendidas: {stats['palabras_aprendidas']}")
        lineas.append(f"   Dominadas: {stats['palabras_dominadas']}")
        lineas.append(f"   Precisión: {stats['precision_promedio']:.1f}%")
        
        # Reporte diario
        diario = self.generar_reporte_diario()
        lineas.append(f"\n📅 HOY:")
        lineas.append(f"   Retos: {diario['retos_completados']}/{diario['objetivo']}")
        lineas.append(f"   Tiempo: {diario['tiempo_estudio']:.0f} min")
        lineas.append(f"   {'✅' if diario['objetivo_cumplido'] else '⏳'} Objetivo")
        
        # Gráfico
        lineas.append(self.generar_grafico_progreso_texto())
        
        lineas.append("\n" + "=" * 60)
        
        return "\n".join(lineas)