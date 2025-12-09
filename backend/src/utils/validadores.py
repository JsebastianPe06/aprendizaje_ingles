def validar_email(email):
    import re
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_contrasena(contrasena):
    return len(contrasena) >= 8

def validar_nombre_usuario(nombre_usuario):
    return len(nombre_usuario) >= 3 and len(nombre_usuario) <= 20

def validar_edad(edad):
    return edad.isdigit() and 13 <= int(edad) <= 120

def validar_datos_usuario(email, contrasena, nombre_usuario, edad):
    return (validar_email(email) and
            validar_contrasena(contrasena) and
            validar_nombre_usuario(nombre_usuario) and
            validar_edad(edad))