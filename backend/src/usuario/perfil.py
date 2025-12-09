"""
Este archivo gestiona los perfiles de usuario y sus configuraciones.
"""

class Perfil:
    def __init__(self, usuario_id, nombre, email, preferencias):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.email = email
        self.preferencias = preferencias

    def actualizar_nombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre

    def actualizar_email(self, nuevo_email):
        self.email = nuevo_email

    def actualizar_preferencias(self, nuevas_preferencias):
        self.preferencias = nuevas_preferencias

    def obtener_info(self):
        return {
            "usuario_id": self.usuario_id,
            "nombre": self.nombre,
            "email": self.email,
            "preferencias": self.preferencias
        }