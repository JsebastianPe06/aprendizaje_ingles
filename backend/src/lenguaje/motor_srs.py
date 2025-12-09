"""
Este archivo implementa un sistema de repetición espaciada (SRS) para el aprendizaje de vocabulario.
"""
from datetime import datetime, timedelta

class SpacedRepetitionSystem:
    """Sistema de Repetición Espaciada para optimizar el aprendizaje"""
    
    def __init__(self):
        self.palabras_en_revision = {}
        self.historial = []
    
    def add_review(self, word, interval=1):
        """
        Agrega una palabra para revisar.
        
        Args:
            word (str): La palabra a revisar
            interval (int): Intervalo en días antes del siguiente repaso
        """
        proxima_revision = datetime.now() + timedelta(days=interval)
        self.palabras_en_revision[word] = {
            "palabra": word,
            "intervalo": interval,
            "proxima_revision": proxima_revision.isoformat(),
            "veces_revisada": 0,
            "dificultad": 1
        }
    
    def get_next_review(self):
        """Obtiene las palabras que necesitan revisión ahora"""
        ahora = datetime.now()
        palabras_a_revisar = []
        
        for word, data in self.palabras_en_revision.items():
            proxima = datetime.fromisoformat(data["proxima_revision"])
            if proxima <= ahora:
                palabras_a_revisar.append(data)
        
        return palabras_a_revisar
    
    def update_review(self, word, correcto=True):
        """
        Actualiza el intervalo de revisión basado en el desempeño.
        
        Args:
            word (str): La palabra revisada
            correcto (bool): Si la respuesta fue correcta
        """
        if word in self.palabras_en_revision:
            data = self.palabras_en_revision[word]
            data["veces_revisada"] += 1
            
            if correcto:
                # Aumentar el intervalo si es correcto
                data["intervalo"] = max(1, int(data["intervalo"] * 1.5))
                data["dificultad"] = max(1, data["dificultad"] - 0.1)
            else:
                # Reducir el intervalo si es incorrecto
                data["intervalo"] = max(1, int(data["intervalo"] * 0.8))
                data["dificultad"] = min(5, data["dificultad"] + 0.2)
            
            # Actualizar próxima revisión
            proxima_revision = datetime.now() + timedelta(days=data["intervalo"])
            data["proxima_revision"] = proxima_revision.isoformat()
            
            self.historial.append({
                "palabra": word,
                "timestamp": datetime.now().isoformat(),
                "correcto": correcto,
                "intervalo": data["intervalo"]
            })
    
    def remove_review(self, word):
        """Elimina una palabra del sistema de revisión"""
        if word in self.palabras_en_revision:
            del self.palabras_en_revision[word]
            return True
        return False
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas del SRS"""
        total_palabras = len(self.palabras_en_revision)
        palabras_a_revisar = len(self.get_next_review())
        
        return {
            "total_palabras": total_palabras,
            "palabras_pendientes": palabras_a_revisar,
            "revisions_completadas": len(self.historial),
            "tasa_exito": self._calcular_tasa_exito()
        }
    
    def _calcular_tasa_exito(self):
        """Calcula la tasa de éxito basada en el historial"""
        if not self.historial:
            return 0
        
        correctas = sum(1 for h in self.historial if h["correcto"])
        return round((correctas / len(self.historial)) * 100, 2)