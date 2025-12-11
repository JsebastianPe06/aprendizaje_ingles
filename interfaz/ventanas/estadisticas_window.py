"""
Ventana de estadísticas con gráficos visuales.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QScrollArea, QTabWidget,
                            QGridLayout, QGroupBox, QSizePolicy)
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QDate

from interfaz.componentes.graficos import GraficoProgreso, GraficoDona, GraficoBarras


class EstadisticasWindow(QWidget):
    """Ventana completa de estadísticas del usuario."""
    
    def __init__(self, perfil, progreso, parent=None):
        super().__init__(parent)
        
        # Componentes del sistema
        self.perfil = perfil
        self.progreso = progreso
        
        # Configurar UI
        self._setup_ui()
        
        # Cargar datos
        self.cargar_datos()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
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
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        
        # Pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F3F4F6;
                color: #4B5563;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2563EB;
                border-bottom: 2px solid #2563EB;
            }
            QTabBar::tab:hover:!selected {
                background-color: #E5E7EB;
            }
        """)
        
        # Crear pestañas
        self._crear_tab_resumen()
        self._crear_tab_progreso()
        self._crear_tab_palabras()
        self._crear_tab_rendimiento()
        
        self.content_layout.addWidget(self.tabs)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def _crear_header(self):
        """Crea el header de la ventana."""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2563EB, stop: 1 #1D4ED8
                );
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 10, 30, 10)
        
        # Título
        title = QLabel("Estadísticas Detalladas")
        title_font = QFont("Segoe UI", 22, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Espaciador
        layout.addStretch()
        
        # Botón actualizar
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.setFixedSize(120, 40)
        btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border-radius: 8px;
                font-weight: bold;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        btn_actualizar.clicked.connect(self.cargar_datos)
        layout.addWidget(btn_actualizar)
        
        return header
    
    def _crear_tab_resumen(self):
        """Crea la pestaña de resumen general."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Estadísticas rápidas
        stats_grid = self._crear_grid_estadisticas()
        layout.addLayout(stats_grid)
        
        # Objetivos
        objetivos_widget = self._crear_widget_objetivos()
        layout.addWidget(objetivos_widget)
        
        # Logros recientes
        logros_widget = self._crear_widget_logros()
        layout.addWidget(logros_widget)
        
        layout.addStretch()
        
        self.tabs.addTab(widget, "Resumen")
    
    def _crear_grid_estadisticas(self):
        """Crea un grid con estadísticas clave."""
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Estadísticas del perfil
        stats = self.perfil.estadisticas
        
        # 1. Racha actual
        card_racha = self._crear_tarjeta_estadistica(
            "Racha Actual",
            f"{stats['racha_actual']} días",
            f"Máxima: {stats['racha_maxima']} días",
            "#F59E0B"
        )
        grid.addWidget(card_racha, 0, 0)
        
        # 2. Precisión
        card_precision = self._crear_tarjeta_estadistica(
            "Precisión",
            f"{stats['precision_promedio']:.1f}%",
            "Promedio de respuestas correctas",
            "#10B981"
        )
        grid.addWidget(card_precision, 0, 1)
        
        # 3. Retos completados
        card_retos = self._crear_tarjeta_estadistica(
            "Retos Completados",
            f"{stats['total_retos_completados']}",
            f"Sesiones: {stats['total_sesiones']}",
            "#2563EB"
        )
        grid.addWidget(card_retos, 0, 2)
        
        # 4. Tiempo de estudio
        horas = stats['tiempo_total_estudio'] / 60
        card_tiempo = self._crear_tarjeta_estadistica(
            "Tiempo de Estudio",
            f"{horas:.1f} horas",
            "Tiempo total invertido",
            "#8B5CF6"
        )
        grid.addWidget(card_tiempo, 0, 3)
        
        return grid
    
    def _crear_tarjeta_estadistica(self, titulo, valor, subtitulo, color):
        widget = QFrame()
        widget.setObjectName("statCard")
        widget.setMinimumHeight(120)

        widget.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
                padding: 20px;
            }}
        """)

        layout = QVBoxLayout(widget)
        layout.setSpacing(5)

        title_label = QLabel(titulo)
        title_label.setStyleSheet(f"""
            color: {color};
            font-size: 14px;
            font-weight: bold;
        """)
        layout.addWidget(title_label)

        value_label = QLabel(valor)
        value_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #1F2937;")
        layout.addWidget(value_label)

        if subtitulo:
            subtitle_label = QLabel(subtitulo)
            subtitle_label.setStyleSheet("color: #6B7280; font-size: 12px;")
            layout.addWidget(subtitle_label)

        layout.addStretch()

        return widget

    
    def _crear_widget_objetivos(self):
        """Crea un widget para mostrar objetivos."""
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
        
        # Título
        title = QLabel("Objetivos")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #1F2937; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Objetivo diario
        objetivo_diario = self.perfil.preferencias['objetivo_diario']
        progreso_semanal = self.perfil.objetivos['progreso_semanal']
        
        diario_widget = self._crear_barra_progreso(
            "Objetivo Diario",
            progreso_semanal,
            objetivo_diario,
            "#2563EB"
        )
        layout.addWidget(diario_widget)
        
        # Objetivo semanal
        objetivo_semanal = self.perfil.objetivos['objetivo_semanal']
        
        semanal_widget = self._crear_barra_progreso(
            "Objetivo Semanal",
            progreso_semanal,
            objetivo_semanal,
            "#10B981"
        )
        layout.addWidget(semanal_widget)
        
        # Objetivo mensual
        objetivo_mensual = self.perfil.objetivos['objetivo_mensual']
        progreso_mensual = self.perfil.objetivos['progreso_mensual']
        
        mensual_widget = self._crear_barra_progreso(
            "Objetivo Mensual",
            progreso_mensual,
            objetivo_mensual,
            "#8B5CF6"
        )
        layout.addWidget(mensual_widget)
        
        return widget
    
    def _crear_barra_progreso(self, texto, actual, total, color):
        """Crea una barra de progreso personalizada."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        
        # Texto y valores
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        text_label = QLabel(texto)
        text_label.setStyleSheet("font-weight: bold; color: #4B5563;")
        top_layout.addWidget(text_label)
        
        top_layout.addStretch()
        
        value_label = QLabel(f"{actual}/{total}")
        value_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        top_layout.addWidget(value_label)
        
        layout.addWidget(top_widget)
        
        # Barra de progreso
        bar_widget = QWidget()
        bar_widget.setFixedHeight(10)
        bar_widget.setStyleSheet(f"""
            QWidget {{
                background-color: #E5E7EB;
                border-radius: 5px;
            }}
        """)
        
        # Barra de progreso interna
        if total > 0:
            porcentaje = min(actual / total, 1.0)
            
            inner_bar = QWidget(bar_widget)
            inner_bar.setStyleSheet(f"""
                QWidget {{
                    background-color: {color};
                    border-radius: 5px;
                }}
            """)
            
            # Posicionar dinámicamente (se ajustará en resizeEvent)
            inner_bar.porcentaje = porcentaje
            inner_bar.setFixedHeight(10)
        
        layout.addWidget(bar_widget)
        
        return widget
    
    def _crear_widget_logros(self):
        """Crea un widget para mostrar logros."""
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
        
        # Título
        title = QLabel("Logros Desbloqueados")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #1F2937; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Logros
        logros = self.perfil.logros
        
        if not logros:
            empty_label = QLabel("Aún no has desbloqueado logros. ¡Sigue practicando!")
            empty_label.setStyleSheet("color: #9CA3AF; font-style: italic; text-align: center; padding: 20px;")
            layout.addWidget(empty_label)
        else:
            # Mostrar últimos 5 logros
            for logro in logros[-5:]:
                logro_widget = self._crear_widget_logro(logro)
                layout.addWidget(logro_widget)
        
        return widget
    
    def _crear_widget_logro(self, logro):
        """Crea un widget para un logro individual."""
        widget = QWidget()
        widget.setFixedHeight(60)
        widget.setStyleSheet("""
            QWidget {
                background-color: #FEF3C7;
                border-radius: 8px;
                border: 2px solid #F59E0B;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Icono
        icon_label = QLabel("🏆")
        icon_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(icon_label)
        
        # Información
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(2)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        name_label = QLabel(logro.get('nombre', 'Logro'))
        name_label.setStyleSheet("font-weight: bold; color: #92400E;")
        
        date_label = QLabel(logro.get('fecha', ''))
        date_label.setStyleSheet("color: #B45309; font-size: 11px;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(date_label)
        
        layout.addWidget(info_widget)
        layout.addStretch()
        
        return widget
    
    def _crear_tab_progreso(self):
        """Crea la pestaña de progreso detallado."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Gráfico de progreso semanal
        grupo_progreso = QGroupBox("Progreso Semanal")
        grupo_progreso.setStyleSheet("""
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
        
        grupo_layout = QVBoxLayout(grupo_progreso)
        
        self.grafico_progreso = GraficoProgreso()
        self.grafico_progreso.setMinimumHeight(300)
        grupo_layout.addWidget(self.grafico_progreso)
        
        layout.addWidget(grupo_progreso)
        
        # Gráfico de distribución por categoría
        grupo_categorias = QGroupBox("Distribución por Categoría")
        grupo_categorias.setStyleSheet(grupo_progreso.styleSheet())
        
        grupo_cat_layout = QHBoxLayout(grupo_categorias)
        
        self.grafico_categorias = GraficoDona()
        self.grafico_categorias.setMinimumSize(300, 300)
        grupo_cat_layout.addWidget(self.grafico_categorias)
        
        layout.addWidget(grupo_categorias)
        
        layout.addStretch()
        
        self.tabs.addTab(widget, "Progreso")
    
    def _crear_tab_palabras(self):
        """Crea la pestaña de progreso de palabras."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Estadísticas generales de palabras
        stats = self.progreso.obtener_estadisticas_generales()
        
        # Tarjetas de resumen
        resumen_widget = QWidget()
        resumen_layout = QHBoxLayout(resumen_widget)
        resumen_layout.setSpacing(15)
        
        # Total palabras
        card_total = self._crear_tarjeta_estadistica(
            "Total Palabras",
            str(stats['total_palabras']),
            "Practicadas en total",
            "#2563EB"
        )
        resumen_layout.addWidget(card_total)
        
        # Aprendidas
        card_aprendidas = self._crear_tarjeta_estadistica(
            "Aprendidas",
            str(stats['palabras_aprendidas']),
            f"{stats['palabras_aprendidas']/max(stats['total_palabras'],1)*100:.1f}%",
            "#10B981"
        )
        resumen_layout.addWidget(card_aprendidas)
        
        # Dominadas
        card_dominadas = self._crear_tarjeta_estadistica(
            "Dominadas",
            str(stats['palabras_dominadas']),
            f"{stats['palabras_dominadas']/max(stats['total_palabras'],1)*100:.1f}%",
            "#F59E0B"
        )
        resumen_layout.addWidget(card_dominadas)
        
        layout.addWidget(resumen_widget)
        
        # Gráfico de palabras por categoría
        grupo_cat = QGroupBox("Palabras por Categoría")
        grupo_cat.setStyleSheet(self._get_groupbox_style())
        
        grupo_cat_layout = QVBoxLayout(grupo_cat)
        
        self.grafico_barras_cat = GraficoBarras()
        self.grafico_barras_cat.setMinimumHeight(200)
        grupo_cat_layout.addWidget(self.grafico_barras_cat)
        
        layout.addWidget(grupo_cat)
        
        # Palabras difíciles
        grupo_dificiles = QGroupBox("Palabras que Necesitan Práctica")
        grupo_dificiles.setStyleSheet(self._get_groupbox_style())
        
        grupo_dif_layout = QVBoxLayout(grupo_dificiles)
        
        # Lista de palabras difíciles
        dificiles = self.progreso.obtener_palabras_debiles(limite=10)
        
        if dificiles:
            for palabra in dificiles:
                palabra_widget = self._crear_widget_palabra_dificil(palabra)
                grupo_dif_layout.addWidget(palabra_widget)
        else:
            empty_label = QLabel("¡Excelente! No tienes palabras difíciles.")
            empty_label.setStyleSheet("color: #9CA3AF; font-style: italic; text-align: center; padding: 20px;")
            grupo_dif_layout.addWidget(empty_label)
        
        layout.addWidget(grupo_dificiles)
        
        layout.addStretch()
        
        self.tabs.addTab(widget, "Palabras")
    
    def _crear_widget_palabra_dificil(self, palabra):
        """Crea un widget para una palabra difícil."""
        widget = QWidget()
        widget.setFixedHeight(50)
        widget.setStyleSheet("""
            QWidget {
                background-color: #FEF2F2;
                border: 1px solid #FECACA;
                border-radius: 8px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Palabra
        palabra_label = QLabel(palabra)
        palabra_label.setStyleSheet("font-weight: bold; color: #DC2626;")
        layout.addWidget(palabra_label)
        
        # Información de progreso
        if palabra in self.progreso.palabras:
            estado = self.progreso.palabras[palabra]
            veces = estado.get('veces_practicada', 0)
            correctas = estado.get('veces_correcta', 0)
            
            if veces > 0:
                precision = (correctas / veces) * 100
                info_label = QLabel(f"Precisión: {precision:.1f}% ({correctas}/{veces})")
                info_label.setStyleSheet("color: #92400E; font-size: 12px;")
                layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Botón para practicar
        btn_practicar = QPushButton("Practicar")
        btn_practicar.setFixedSize(100, 30)
        btn_practicar.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        layout.addWidget(btn_practicar)
        
        return widget
    
    def _crear_tab_rendimiento(self):
        """Crea la pestaña de análisis de rendimiento."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Análisis de fortalezas y debilidades
        analisis = self.progreso.rendimiento
        
        # Fortalezas
        grupo_fortalezas = QGroupBox("Fortalezas")
        grupo_fortalezas.setStyleSheet(self._get_groupbox_style())
        
        grupo_fort_layout = QVBoxLayout(grupo_fortalezas)
        
        if analisis.get('fortalezas'):
            for fortaleza in analisis['fortalezas'][:3]:
                fort_widget = self._crear_widget_habilidad(fortaleza, True)
                grupo_fort_layout.addWidget(fort_widget)
        else:
            empty_label = QLabel("Aún no hay datos suficientes")
            empty_label.setStyleSheet("color: #9CA3AF; font-style: italic; text-align: center; padding: 20px;")
            grupo_fort_layout.addWidget(empty_label)
        
        layout.addWidget(grupo_fortalezas)
        
        # Debilidades
        grupo_debilidades = QGroupBox(" Áreas a Mejorar")
        grupo_debilidades.setStyleSheet(self._get_groupbox_style())
        
        grupo_deb_layout = QVBoxLayout(grupo_debilidades)
        
        if analisis.get('debilidades'):
            for debilidad in analisis['debilidades'][:3]:
                deb_widget = self._crear_widget_habilidad(debilidad, False)
                grupo_deb_layout.addWidget(deb_widget)
        else:
            empty_label = QLabel("¡Todo parece estar en orden!")
            empty_label.setStyleSheet("color: #9CA3AF; font-style: italic; text-align: center; padding: 20px;")
            grupo_deb_layout.addWidget(empty_label)
        
        layout.addWidget(grupo_debilidades)
        
        # Recomendaciones
        grupo_recomendaciones = QGroupBox(" Recomendaciones")
        grupo_recomendaciones.setStyleSheet(self._get_groupbox_style())
        
        grupo_rec_layout = QVBoxLayout(grupo_recomendaciones)
        
        recomendaciones = analisis.get('recomendaciones', [])
        
        if recomendaciones:
            for rec in recomendaciones:
                rec_widget = self._crear_widget_recomendacion(rec)
                grupo_rec_layout.addWidget(rec_widget)
        else:
            empty_label = QLabel("Sigue practicando regularmente")
            empty_label.setStyleSheet("color: #9CA3AF; font-style: italic; text-align: center; padding: 20px;")
            grupo_rec_layout.addWidget(empty_label)
        
        layout.addWidget(grupo_recomendaciones)
        
        layout.addStretch()
        
        self.tabs.addTab(widget, " Rendimiento")
    
    def _crear_widget_habilidad(self, habilidad, es_fortaleza):
        """Crea un widget para mostrar una habilidad (fortaleza/debilidad)."""
        widget = QWidget()
        widget.setFixedHeight(60)
        
        color = "#10B981" if es_fortaleza else "#EF4444"
        bg_color = "#D1FAE5" if es_fortaleza else "#FEE2E2"
        border_color = "#10B981" if es_fortaleza else "#EF4444"
        
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Tipo de reto
        tipo = habilidad.get('tipo', 'Desconocido')
        tipo_label = QLabel(tipo.replace('_', ' ').title())
        tipo_label.setStyleSheet("font-weight: bold; color: #1F2937;")
        layout.addWidget(tipo_label)
        
        layout.addStretch()
        
        # Precisión
        precision = habilidad.get('precision', 0)
        precision_label = QLabel(f"{precision:.1f}%")
        precision_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        layout.addWidget(precision_label)
        
        return widget
    
    def _crear_widget_recomendacion(self, texto):
        """Crea un widget para una recomendación."""
        widget = QWidget()
        widget.setFixedHeight(50)
        widget.setStyleSheet("""
            QWidget {
                background-color: #EFF6FF;
                border: 2px solid #DBEAFE;
                border-radius: 8px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Icono
        icon_label = QLabel("💡")
        layout.addWidget(icon_label)
        
        # Texto
        texto_label = QLabel(texto)
        texto_label.setStyleSheet("color: #1E40AF;")
        texto_label.setWordWrap(True)
        layout.addWidget(texto_label)
        
        return widget
    
    def _get_groupbox_style(self):
        """Retorna el estilo para los QGroupBox."""
        return """
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
        """
    
    def cargar_datos(self):
        """Carga y actualiza todos los datos."""
        # Datos de progreso semanal (simulados por ahora)
        datos_semana = [5, 7, 3, 8, 6, 9, 4]
        etiquetas_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        
        self.grafico_progreso.set_datos(datos_semana, etiquetas_semana)
        
        # Datos de categorías (simulados)
        categorias = ['Sustantivos', 'Verbos', 'Adjetivos', 'Adverbios']
        valores_cat = [25, 18, 12, 8]
        
        self.grafico_categorias.set_datos(valores_cat, categorias)
        
        # Datos para gráfico de barras
        self.grafico_barras_cat.set_datos(valores_cat, categorias)