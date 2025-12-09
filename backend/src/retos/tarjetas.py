"""
Este archivo gestiona las tarjetas de memoria (flashcards) en el sistema de aprendizaje de inglés.
"""
import random

class Tarjeta:
    def __init__(self, pregunta, respuesta, id=None, dificultad="media"):
        self.id = id
        self.pregunta = pregunta
        self.respuesta = respuesta
        self.dificultad = dificultad
        self.intentos = 0
        self.aciertos = 0

    def mostrar(self):
        return {
            "id": self.id,
            "pregunta": self.pregunta,
            "respuesta": self.respuesta,
            "dificultad": self.dificultad,
            "intentos": self.intentos,
            "aciertos": self.aciertos
        }

    def registrar_intento(self, correcto):
        self.intentos += 1
        if correcto:
            self.aciertos += 1
        
        # Ajustar dificultad
        tasa_exito = self.aciertos / self.intentos if self.intentos > 0 else 0
        if tasa_exito > 0.8:
            self.dificultad = "facil"
        elif tasa_exito < 0.5:
            self.dificultad = "dificil"
        else:
            self.dificultad = "media"

class GestorTarjetas:
    def __init__(self):
        self.tarjetas = []
        self.id_counter = 1

    def agregar_tarjeta(self, pregunta, respuesta, dificultad="media"):
        """Agrega una nueva tarjeta"""
        tarjeta = Tarjeta(pregunta, respuesta, self.id_counter, dificultad)
        self.tarjetas.append(tarjeta)
        self.id_counter += 1
        return tarjeta

    def obtener_tarjetas(self):
        """Obtiene todas las tarjetas"""
        return [t.mostrar() for t in self.tarjetas]

    def obtener_tarjeta_por_id(self, id):
        """Obtiene una tarjeta específica"""
        for t in self.tarjetas:
            if t.id == id:
                return t.mostrar()
        return None

    def mezclar_tarjetas(self):
        """Mezcla las tarjetas aleatoriamente"""
        random.shuffle(self.tarjetas)

    def obtener_tarjetas_por_dificultad(self, dificultad):
        """Obtiene tarjetas de una dificultad específica"""
        return [t.mostrar() for t in self.tarjetas if t.dificultad == dificultad]

    def obtener_proximas_tarjetas(self, cantidad=5):
        """Obtiene las próximas tarjetas a estudiar"""
        # Priorizar tarjetas con baja tasa de éxito
        sorted_tarjetas = sorted(
            self.tarjetas,
            key=lambda t: (t.aciertos / t.intentos if t.intentos > 0 else 0)
        )
        return [t.mostrar() for t in sorted_tarjetas[:cantidad]]

    def registrar_respuesta(self, tarjeta_id, correcto):
        """Registra la respuesta de un usuario"""
        for t in self.tarjetas:
            if t.id == tarjeta_id:
                t.registrar_intento(correcto)
                return True
        return False

    def obtener_estadisticas(self):
        """Obtiene estadísticas generales de las tarjetas"""
        if not self.tarjetas:
            return {"total": 0, "tasa_exito": 0, "tarjetas": []}
        
        total_intentos = sum(t.intentos for t in self.tarjetas)
        total_aciertos = sum(t.aciertos for t in self.tarjetas)
        tasa_exito = (total_aciertos / total_intentos * 100) if total_intentos > 0 else 0
        
        return {
            "total_tarjetas": len(self.tarjetas),
            "total_intentos": total_intentos,
            "total_aciertos": total_aciertos,
            "tasa_exito": round(tasa_exito, 2),
            "tarjetas_estudiadas": len([t for t in self.tarjetas if t.intentos > 0]),
            "tarjetas_sin_estudiar": len([t for t in self.tarjetas if t.intentos == 0])
        }

    def mostrar_tarjetas(self):
        """Muestra todas las tarjetas"""
        for tarjeta in self.tarjetas:
            print(tarjeta.mostrar())