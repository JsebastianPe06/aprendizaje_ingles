"""
Módulo de retos para evaluación de usuarios.

Este módulo contiene diferentes tipos de ejercicios/retos:
- Tarjetas (flashcards): asociar palabra con significado
- Formar palabras: ordenar letras para formar palabras
- Oraciones: completar, ordenar, traducir oraciones

Todos los retos heredan de RetoBase y se integran con el motor SRS.
"""

from .base import RetoBase
from .tarjetas import RetoTarjetas, RetoTarjetasInverso
from .formar_palabras import RetoFormarPalabras, RetoFormarPalabrasMultiple
from .oraciones import (
    RetoCompletarOracion,
    RetoOrdenarOracion,
    RetoTraducirOracion
)
from .generador import GeneradorRetos

__all__ = [
    'RetoBase',
    'RetoTarjetas',
    'RetoTarjetasInverso',
    'RetoFormarPalabras',
    'RetoFormarPalabrasMultiple',
    'RetoCompletarOracion',
    'RetoOrdenarOracion',
    'RetoTraducirOracion',
    'GeneradorRetos'
]