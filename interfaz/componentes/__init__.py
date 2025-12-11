"""
Exportar componentes para fácil importación.
"""

from .reto_base import RetoWidgetBase
from .reto_tarjetas import RetoTarjetasWidget
from .reto_formar_palabras import RetoFormarPalabrasWidget
from .reto_oraciones import (
    RetoCompletarOracionWidget,
    RetoOrdenarOracionWidget,
    RetoOracionesWidgetBase
)
from .seleccion_personalizada import DialogoPersonalizado
from .repaso_dificiles import RepasoDificilesWindow

from .graficos import (
    GraficoBarras,
    GraficoDona,
    GraficoProgreso,
    QLinearGradient
) 

# Mapa de tipos de reto a widgets
RETO_WIDGETS = {
    'tarjetas': RetoTarjetasWidget,
    'tarjetas_inverso': RetoTarjetasWidget,
    'formar_palabras': RetoFormarPalabrasWidget,
    'completar_oracion': RetoCompletarOracionWidget,
    'ordenar_oracion': RetoOrdenarOracionWidget,
    'traducir_oracion': RetoCompletarOracionWidget  # Temporal, se hará específico
}

__all__ = [
    'RetoWidgetBase',
    'RetoTarjetasWidget',
    'RetoFormarPalabrasWidget',
    'RetoCompletarOracionWidget',
    'RetoOrdenarOracionWidget',
    'RetoOracionesWidgetBase',
    'RETO_WIDGETS'
]