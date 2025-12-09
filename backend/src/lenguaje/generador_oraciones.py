def generar_oracion(sujeto, verbo, objeto):
    return f"{sujeto} {verbo} {objeto}."

def generar_oraciones(sujetos, verbos, objetos):
    oraciones = []
    for sujeto in sujetos:
        for verbo in verbos:
            for objeto in objetos:
                oraciones.append(generar_oracion(sujeto, verbo, objeto))
    return oraciones

# Ejemplo de uso
if __name__ == "__main__":
    sujetos = ["El perro", "La niña", "El gato"]
    verbos = ["come", "juega", "salta"]
    objetos = ["la pelota", "la comida", "el frisbee"]

    oraciones_generadas = generar_oraciones(sujetos, verbos, objetos)
    for oracion in oraciones_generadas:
        print(oracion)