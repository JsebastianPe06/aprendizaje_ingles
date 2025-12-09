from flask import Flask, jsonify, request
import json
import os
import random
from lenguaje.diccionario import Diccionario
from lenguaje.categorias import Categoria, listar_categorias, obtener_categoria
from lenguaje.analizador import analizar_texto, contar_frecuencia
from lenguaje.motor_srs import SpacedRepetitionSystem
from retos.tarjetas import GestorTarjetas
from retos.formar_palabras import generar_reto_formar_palabras, RetoFormarPalabras
from retos.oraciones import generar_reto_oracion, validar_oracion

app = Flask(__name__)

# Rutas de archivos de datos
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Cargar datos del JSON
def cargar_datos_vocabulario():
    ruta_archivo = os.path.join(DATA_DIR, 'a_p.json')
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"vocabulary": [], "exercises": []}

# Inicializar sistemas
diccionario = Diccionario()
gestor_tarjetas = GestorTarjetas()
sistema_srs = SpacedRepetitionSystem()
datos = cargar_datos_vocabulario()

# Poblar diccionario y tarjetas
for palabra_obj in datos.get('vocabulary', []):
    if isinstance(palabra_obj, dict) and 'word' in palabra_obj:
        diccionario.agregar_palabra(palabra_obj['word'], palabra_obj.get('definition', ''))
        gestor_tarjetas.agregar_tarjeta(
            f"¿Qué significa '{palabra_obj['word']}'?",
            palabra_obj.get('definition', ''),
            "media"
        )
        sistema_srs.add_review(palabra_obj['word'])

# ===================== ENDPOINTS DE APRENDIZAJE =====================

@app.route('/api/v1/learn', methods=['GET'])
def get_learning_material():
    """Obtiene todas las palabras y ejercicios"""
    datos = cargar_datos_vocabulario()
    vocabulary = datos.get('vocabulary', [])
    exercises = datos.get('exercises', [])
    
    return jsonify({
        "success": True,
        "data": {
            "vocabulary": vocabulary,
            "exercises": exercises,
            "total_words": len(vocabulary),
            "total_exercises": len(exercises)
        }
    })

@app.route('/api/v1/vocabulary', methods=['GET'])
def get_vocabulary():
    """Obtiene solo el vocabulario"""
    datos = cargar_datos_vocabulario()
    vocabulary = datos.get('vocabulary', [])
    return jsonify({"success": True, "data": vocabulary})

@app.route('/api/v1/word/<word>', methods=['GET'])
def get_word_definition(word):
    """Obtiene la definición de una palabra específica"""
    definicion = diccionario.obtener_significado(word.lower())
    return jsonify({
        "success": True,
        "word": word,
        "definition": definicion
    })

# ===================== ENDPOINTS DE CATEGORÍAS =====================

@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    """Obtiene todas las categorías disponibles"""
    categorias = listar_categorias()
    return jsonify({
        "success": True,
        "data": categorias
    })

@app.route('/api/v1/categories/<categoria_nombre>', methods=['GET'])
def get_categoria_detalle(categoria_nombre):
    """Obtiene una categoría específica"""
    categoria = obtener_categoria(categoria_nombre)
    if categoria:
        return jsonify({"success": True, "data": categoria})
    return jsonify({"success": False, "error": "Categoría no encontrada"}), 404

# ===================== ENDPOINTS DE FLASHCARDS =====================

@app.route('/api/v1/flashcards', methods=['GET'])
def get_flashcards():
    """Obtiene todas las flashcards"""
    return jsonify({
        "success": True,
        "data": {
            "tarjetas": gestor_tarjetas.obtener_tarjetas(),
            "estadisticas": gestor_tarjetas.obtener_estadisticas()
        }
    })

@app.route('/api/v1/flashcards/proximas', methods=['GET'])
def get_proximas_flashcards():
    """Obtiene las próximas flashcards a estudiar"""
    cantidad = request.args.get('cantidad', 5, type=int)
    return jsonify({
        "success": True,
        "data": gestor_tarjetas.obtener_proximas_tarjetas(cantidad)
    })

@app.route('/api/v1/flashcards/<int:tarjeta_id>/responder', methods=['POST'])
def responder_flashcard(tarjeta_id):
    """Registra la respuesta de una flashcard"""
    data = request.json
    correcto = data.get('correcto', False)
    
    if gestor_tarjetas.registrar_respuesta(tarjeta_id, correcto):
        return jsonify({
            "success": True,
            "message": "Respuesta registrada",
            "estadisticas": gestor_tarjetas.obtener_estadisticas()
        })
    return jsonify({"success": False, "error": "Flashcard no encontrada"}), 404

# ===================== ENDPOINTS DE RETOS =====================

@app.route('/api/v1/retos/formar-palabras', methods=['POST'])
def reto_formar_palabras():
    """Genera un reto de formar palabras"""
    data = request.json
    palabra = data.get('palabra', '')
    
    if not palabra:
        return jsonify({"success": False, "error": "Palabra requerida"}), 400
    
    reto = generar_reto_formar_palabras(palabra)
    return jsonify({"success": True, "data": reto})

@app.route('/api/v1/retos/formar-palabras/verificar', methods=['POST'])
def verificar_formar_palabras():
    """Verifica la respuesta del reto de formar palabras"""
    data = request.json
    palabra_objetivo = data.get('palabra', '')
    respuesta_usuario = data.get('respuesta', '')
    
    reto = RetoFormarPalabras(palabra_objetivo)
    resultado = reto.verificar_respuesta(respuesta_usuario)
    
    return jsonify({
        "success": True,
        "data": resultado
    })

@app.route('/api/v1/retos/oracion', methods=['POST'])
def reto_construccion_oracion():
    """Genera un reto de construcción de oraciones"""
    data = request.json
    palabra_clave = data.get('palabra', '')
    nivel = data.get('nivel', 'basico')
    
    if not palabra_clave:
        return jsonify({"success": False, "error": "Palabra requerida"}), 400
    
    reto = generar_reto_oracion(palabra_clave, nivel)
    return jsonify({"success": True, "data": reto})

@app.route('/api/v1/retos/oracion/validar', methods=['POST'])
def validar_oracion_reto():
    """Valida una oración del reto"""
    data = request.json
    oracion = data.get('oracion', '')
    palabra_clave = data.get('palabra_clave', '')
    
    es_valida = validar_oracion(oracion) and palabra_clave.lower() in oracion.lower()
    
    return jsonify({
        "success": True,
        "data": {
            "valida": es_valida,
            "tiene_palabra_clave": palabra_clave.lower() in oracion.lower(),
            "mensaje": "Oración válida" if es_valida else "La oración debe tener al menos 3 palabras, incluir la palabra clave y terminar con puntuación"
        }
    })

# ===================== ENDPOINTS DE SRS =====================

@app.route('/api/v1/srs/proximas-revisiones', methods=['GET'])
def get_proximas_revisiones():
    """Obtiene palabras que necesitan revisión"""
    proximas = sistema_srs.get_next_review()
    return jsonify({
        "success": True,
        "data": {
            "palabras": proximas,
            "cantidad": len(proximas),
            "estadisticas": sistema_srs.obtener_estadisticas()
        }
    })

@app.route('/api/v1/srs/actualizar-revision', methods=['POST'])
def actualizar_revision_srs():
    """Actualiza la revisión SRS basada en el desempeño"""
    data = request.json
    palabra = data.get('palabra', '')
    correcto = data.get('correcto', False)
    
    if not palabra:
        return jsonify({"success": False, "error": "Palabra requerida"}), 400
    
    sistema_srs.update_review(palabra, correcto)
    
    return jsonify({
        "success": True,
        "message": "Revisión actualizada",
        "estadisticas": sistema_srs.obtener_estadisticas()
    })

@app.route('/api/v1/srs/estadisticas', methods=['GET'])
def obtener_estadisticas_srs():
    """Obtiene estadísticas del SRS"""
    return jsonify({
        "success": True,
        "data": sistema_srs.obtener_estadisticas()
    })

# ===================== ENDPOINTS DE PROGRESO Y USUARIO =====================

@app.route('/api/v1/progress', methods=['GET', 'POST'])
def update_progress():
    """Obtiene o actualiza el progreso del usuario"""
    if request.method == 'POST':
        data = request.json
        return jsonify({
            "success": True,
            "message": "Progreso actualizado",
            "data": data
        })
    
    datos = cargar_datos_vocabulario()
    progress = {
        "userId": 1,
        "totalLessons": len(datos.get('vocabulary', [])),
        "completedLessons": 3,
        "percentage": 30,
        "streak": 7,
        "categories": {
            "vocabulary": {
                "completed": 3,
                "total": len(datos.get('vocabulary', [])),
                "percentage": 60
            },
            "flashcards": gestor_tarjetas.obtener_estadisticas(),
            "srs": sistema_srs.obtener_estadisticas()
        }
    }
    return jsonify({"success": True, "data": progress})

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Obtiene información del usuario"""
    users = {
        "id": 1,
        "name": "Juan",
        "email": "juan@example.com",
        "level": "Principiante",
        "joinDate": "2024-01-15",
        "totalXP": 2450,
        "badges": ["Primer paso", "Una semana", "100 palabras aprendidas"],
        "estadisticas": {
            "palabras_aprendidas": len(datos.get('vocabulary', [])),
            "retos_completados": 15,
            "racha": 7
        }
    }
    return jsonify({"success": True, "data": users})

# ===================== ENDPOINTS DE EJERCICIOS =====================

@app.route('/api/v1/lesson/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Obtiene una lección específica"""
    datos_vocab = cargar_datos_vocabulario()
    vocabulary = datos_vocab.get('vocabulary', [])
    
    if lesson_id <= 0 or lesson_id > len(vocabulary):
        return jsonify({"success": False, "error": "Lección no encontrada"}), 404
    
    palabra_actual = vocabulary[lesson_id - 1]
    
    lesson = {
        "id": lesson_id,
        "title": f"Lección {lesson_id}: {palabra_actual.get('word', '').capitalize()}",
        "content": palabra_actual.get('definition', ''),
        "word": palabra_actual.get('word', ''),
        "exercises": [
            {
                "question": f"¿Cuál es la definición de '{palabra_actual.get('word', '')}'?",
                "options": [
                    palabra_actual.get('definition', ''),
                    "Una fruta cítrica",
                    "Un animal doméstico",
                    "Un objeto de madera"
                ],
                "answer": palabra_actual.get('definition', '')
            }
        ]
    }
    return jsonify({"success": True, "data": lesson})

@app.route('/api/v1/quiz', methods=['POST'])
def submit_quiz():
    """Envía respuestas del quiz"""
    data = request.json
    return jsonify({
        "success": True,
        "message": "Quiz enviado exitosamente",
        "score": data.get('score', 0),
        "total": data.get('total', 0)
    })

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_text():
    """Analiza un texto proporcionado"""
    data = request.json
    texto = data.get('texto', '')
    
    if not texto:
        return jsonify({"success": False, "error": "Texto vacío"}), 400
    
    analisis = analizar_texto(texto)
    return jsonify({
        "success": True,
        "data": analisis
    })

if __name__ == '__main__':
    app.run(debug=True)