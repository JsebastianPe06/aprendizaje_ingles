"""
Componentes de gráficos personalizados para PyQt6.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QLinearGradient, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
import math


class GraficoProgreso(QWidget):
    """
    Gráfico de línea personalizado para mostrar progreso.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Datos
        self.datos = []
        self.etiquetas = []
        
        # Configuración
        self.color_linea = QColor("#2563EB")
        self.color_punto = QColor("#1D4ED8")
        self.color_fondo = QColor("#FFFFFF")
        self.color_grid = QColor("#E5E7EB")
        
        # Margenes
        self.margen_izquierdo = 50
        self.margen_derecho = 20
        self.margen_superior = 30
        self.margen_inferior = 40
        
        self.setMinimumHeight(200)
    
    def set_datos(self, datos, etiquetas=None):
        """Establece los datos a graficar."""
        self.datos = datos
        
        if etiquetas and len(etiquetas) == len(datos):
            self.etiquetas = etiquetas
        else:
            self.etiquetas = [str(i+1) for i in range(len(datos))]
        
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el gráfico."""
        if not self.datos:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Obtener dimensiones
        ancho = self.width()
        alto = self.height()
        
        # Área de dibujo
        area_dibujo = QRectF(
            self.margen_izquierdo,
            self.margen_superior,
            ancho - self.margen_izquierdo - self.margen_derecho,
            alto - self.margen_superior - self.margen_inferior
        )
        
        # Dibujar fondo
        painter.fillRect(self.rect(), self.color_fondo)
        
        # Dibujar grid
        self._dibujar_grid(painter, area_dibujo)
        
        # Calcular escalas
        max_valor = max(self.datos) if self.datos else 1
        min_valor = min(self.datos) if self.datos else 0
        
        # Asegurar rango mínimo
        rango = max_valor - min_valor
        if rango == 0:
            rango = 1
        
        # Dibujar línea de progreso
        self._dibujar_linea_progreso(painter, area_dibujo, min_valor, rango)
        
        # Dibujar ejes
        self._dibujar_ejes(painter, area_dibujo, min_valor, rango)
        
        # Dibujar etiquetas
        self._dibujar_etiquetas(painter, area_dibujo)
        
        painter.end()
    
    def _dibujar_grid(self, painter, area):
        """Dibuja la cuadrícula del gráfico."""
        pen = QPen(self.color_grid, 1, Qt.PenStyle.DotLine)
        painter.setPen(pen)
        
        # Líneas horizontales
        for i in range(5):
            y = area.top() + (area.height() / 4) * i
            painter.drawLine(int(area.left()), int(y), int(area.right()), int(y))
    
    def _dibujar_linea_progreso(self, painter, area, min_valor, rango):
        """Dibuja la línea de progreso."""
        if len(self.datos) < 2:
            return
        
        # Crear gradiente para la línea
        gradiente = QLinearGradient(area.left(), area.top(), area.left(), area.bottom())
        gradiente.setColorAt(0, QColor("#3B82F6"))
        gradiente.setColorAt(1, QColor("#1D4ED8"))
        
        pen = QPen(gradiente, 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        
        # Calcular puntos
        puntos = []
        for i, valor in enumerate(self.datos):
            x = area.left() + (area.width() / (len(self.datos) - 1)) * i
            y = area.bottom() - ((valor - min_valor) / rango) * area.height()
            puntos.append(QPointF(x, y))
        
        # Dibujar línea
        for i in range(len(puntos) - 1):
            painter.drawLine(puntos[i], puntos[i + 1])
        
        # Dibujar puntos
        painter.setBrush(QBrush(self.color_punto))
        for punto in puntos:
            painter.drawEllipse(punto, 5, 5)
        # Dibujar área bajo la curva
        if len(puntos) >= 2:
            path = QPainterPath()
            path.moveTo(puntos[0])
            for punto in puntos[1:]:
                path.lineTo(punto)
            path.lineTo(puntos[-1].x(), area.bottom())
            path.lineTo(puntos[0].x(), area.bottom())
            path.closeSubpath()
            # Gradiente para el área
            area_gradiente = QLinearGradient(area.left(), area.top(), area.left(), area.bottom())
            area_gradiente.setColorAt(0, QColor(59, 130, 246, 50))
            area_gradiente.setColorAt(1, QColor(29, 78, 216, 30))
            painter.fillPath(path, area_gradiente)
    
    def _dibujar_ejes(self, painter, area, min_valor, rango):
        """Dibuja los ejes del gráfico."""
        pen = QPen(QColor("#374151"), 2)
        painter.setPen(pen)
        # Eje X
        painter.drawLine(int(area.left()), int(area.bottom()), int(area.right()), int(area.bottom()))
        # Eje Y
        painter.drawLine(int(area.left()), int(area.top()), int(area.left()), int(area.bottom()))
        # Marcas del eje Y
        font = QFont("Segoe UI", 8)
        painter.setFont(font)
        for i in range(5):
            valor = min_valor + (rango / 4) * i
            y = area.bottom() - (area.height() / 4) * i
            # Marca
            painter.drawLine(int(area.left() - 5), int(y), int(area.left()), int(y))
            # Texto
            texto = f"{valor:.0f}"
            rect_texto = painter.boundingRect(QRectF(), Qt.TextFlag.TextSingleLine, texto)
            painter.drawText(
                int(area.left() - rect_texto.width() - 10),
                int(y + rect_texto.height() / 3),
                texto
            )
    
    def _dibujar_etiquetas(self, painter, area):
        """Dibuja las etiquetas del eje X."""
        if not self.etiquetas:
            return
        font = QFont("Segoe UI", 9)
        painter.setFont(font)
        painter.setPen(QColor("#6B7280"))
        for i, etiqueta in enumerate(self.etiquetas):
            x = area.left() + (area.width() / (len(self.etiquetas) - 1)) * i
            y = area.bottom() + 20
            rect_texto = painter.boundingRect(QRectF(), Qt.TextFlag.TextSingleLine, etiqueta)
            painter.drawText(
                int(x - rect_texto.width() / 2),
                int(y),
                etiqueta
            )


class GraficoDona(QWidget):
    """
    Gráfico de dona para mostrar proporciones.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Datos
        self.datos = []
        self.etiquetas = []
        self.colores = [
            QColor("#2563EB"),  # Azul
            QColor("#10B981"),  # Verde
            QColor("#F59E0B"),  # Naranja
            QColor("#8B5CF6"),  # Violeta
            QColor("#EF4444"),  # Rojo
            QColor("#6B7280"),  # Gris
        ]
        
        self.setMinimumSize(200, 200)
    
    def set_datos(self, datos, etiquetas=None):
        """Establece los datos a graficar."""
        self.datos = datos
        if etiquetas and len(etiquetas) == len(datos):
            self.etiquetas = etiquetas
        else:
            self.etiquetas = [f"Categoría {i+1}" for i in range(len(datos))]
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el gráfico de dona."""
        if not self.datos or sum(self.datos) == 0:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calcular dimensiones
        lado = min(self.width(), self.height()) - 20
        rect = QRectF(
            (self.width() - lado) / 2,
            (self.height() - lado) / 2,
            lado,
            lado
        )
        # Calcular ángulos
        total = sum(self.datos)
        angulo_inicio = 0
        # Dibujar segmentos
        for i, valor in enumerate(self.datos):
            porcentaje = valor / total
            angulo_span = 360 * porcentaje
            if angulo_span > 0:
                # Color para este segmento
                color = self.colores[i % len(self.colores)]
                
                # Dibujar segmento
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(QColor("#FFFFFF"), 2))
                painter.drawPie(rect, int(angulo_inicio * 16), int(angulo_span * 16))
                
                angulo_inicio += angulo_span
        
        # Dibujar centro blanco (efecto dona)
        radio_interno = lado * 0.4
        rect_interno = QRectF(
            rect.center().x() - radio_interno / 2,
            rect.center().y() - radio_interno / 2,
            radio_interno,
            radio_interno
        )
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(rect_interno)
        # Dibujar texto en el centro
        font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#1F2937"))
        texto = f"{total}"
        rect_texto = painter.boundingRect(rect_interno, Qt.AlignmentFlag.AlignCenter, texto)
        painter.drawText(rect_interno, Qt.AlignmentFlag.AlignCenter, texto)
        # Leyenda
        self._dibujar_leyenda(painter, rect)
        painter.end()
    
    def _dibujar_leyenda(self, painter, rect_grafico):
        """Dibuja la leyenda del gráfico."""
        if not self.etiquetas:
            return
        font = QFont("Segoe UI", 9)
        painter.setFont(font)
        # Posición inicial para la leyenda
        x = rect_grafico.right() + 20
        y = rect_grafico.top()
        total = sum(self.datos)
        for i, (valor, etiqueta) in enumerate(zip(self.datos, self.etiquetas)):
            if valor == 0:
                continue
            # Color
            color = self.colores[i % len(self.colores)]
            # Cuadrado de color
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor("#FFFFFF"), 1))
            painter.drawRect(int(x), int(y), 12, 12)
            # Texto
            porcentaje = (valor / total) * 100
            texto = f"{etiqueta}: {valor} ({porcentaje:.1f}%)"
            painter.setPen(QColor("#374151"))
            painter.drawText(int(x + 20), int(y + 10), texto)
            y += 25
            # Si no cabe, mover a columna siguiente
            if y > rect_grafico.bottom() - 50:
                x += 150
                y = rect_grafico.top()


class GraficoBarras(QWidget):
    """
    Gráfico de barras horizontal.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.datos = []
        self.etiquetas = []
        self.color_barras = QColor("#2563EB")
        self.color_fondo = QColor("#FFFFFF")
        
        self.setMinimumHeight(150)
    
    def set_datos(self, datos, etiquetas=None):
        """Establece los datos a graficar."""
        self.datos = datos
        
        if etiquetas and len(etiquetas) == len(datos):
            self.etiquetas = etiquetas
        else:
            self.etiquetas = [f"Item {i+1}" for i in range(len(datos))]
        
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el gráfico de barras."""
        if not self.datos:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Fondo
        painter.fillRect(self.rect(), self.color_fondo)
        # Dimensiones
        ancho = self.width()
        alto = self.height()
        margen_izquierdo = 100
        margen_derecho = 20
        margen_superior = 30
        margen_inferior = 20
        area_dibujo = QRectF(
            margen_izquierdo,
            margen_superior,
            ancho - margen_izquierdo - margen_derecho,
            alto - margen_superior - margen_inferior
        )
        # Calcular máxima barra
        max_valor = max(self.datos) if self.datos else 1
        # Altura por barra
        altura_barra = area_dibujo.height() / len(self.datos)
        espacio_barra = altura_barra * 0.3
        # Dibujar barras
        for i, (valor, etiqueta) in enumerate(zip(self.datos, self.etiquetas)):
            # Posición Y
            y = area_dibujo.top() + i * altura_barra + espacio_barra / 2
            # Ancho de barra (proporcional)
            ancho_barra = (valor / max_valor) * area_dibujo.width()
            # Rectángulo de la barra
            rect_barra = QRectF(
                area_dibujo.left(),
                y,
                ancho_barra,
                altura_barra - espacio_barra
            )
            # Gradiente para la barra
            gradiente = QLinearGradient(
                rect_barra.left(), rect_barra.top(),
                rect_barra.right(), rect_barra.top()
            )
            gradiente.setColorAt(0, QColor("#3B82F6"))
            gradiente.setColorAt(1, QColor("#1D4ED8"))
            painter.setBrush(QBrush(gradiente))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect_barra, 5, 5)
            # Texto del valor
            painter.setPen(QColor("#FFFFFF"))
            font_valor = QFont("Segoe UI", 10, QFont.Weight.Bold)
            painter.setFont(font_valor)
            texto_valor = str(valor)
            rect_texto_valor = painter.boundingRect(
                rect_barra,
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                texto_valor
            )
            # Ajustar posición si no cabe
            if rect_texto_valor.width() > rect_barra.width() - 10:
                painter.drawText(
                    int(rect_barra.right() - rect_texto_valor.width() - 5),
                    int(rect_barra.center().y() + rect_texto_valor.height() / 3),
                    texto_valor
                )
            else:
                painter.drawText(
                    int(rect_barra.right() - 10),
                    int(rect_barra.center().y() + rect_texto_valor.height() / 3),
                    texto_valor
                )
            
            # Etiqueta
            painter.setPen(QColor("#374151"))
            font_etiqueta = QFont("Segoe UI", 10)
            painter.setFont(font_etiqueta)
            
            rect_texto_etiqueta = painter.boundingRect(
                QRectF(),
                Qt.TextFlag.TextSingleLine,
                etiqueta
            )
            
            painter.drawText(
                int(area_dibujo.left() - rect_texto_etiqueta.width() - 10),
                int(rect_barra.center().y() + rect_texto_etiqueta.height() / 3),
                etiqueta
            )
        
        painter.end()