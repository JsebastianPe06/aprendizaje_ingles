# 📚 ENGLISH_APP - Sistema de Aprendizaje de Inglés

## 📖 Descripción

ENGLISH_APP es un sistema avanzado de aprendizaje de inglés basado en **estructuras de grafos** y **algoritmos de repetición espaciada (SRS)**. El sistema utiliza un grafo semántico para establecer relaciones entre palabras y conceptos, permitiendo un aprendizaje contextualizado y personalizado.

### Características Principales

- 🧠 **Grafo Semántico**: Estructura de datos basada en grafos que conecta palabras mediante relaciones semánticas (sinónimos, hipónimos, dominios, temas)
- 📊 **Sistema SRS (Spaced Repetition System)**: Implementación del algoritmo SM-2 (similar a Anki) para optimizar la retención a largo plazo
- 🎮 **Múltiples Tipos de Retos**: Tarjetas de memoria, formar palabras, construcción de oraciones
- 📈 **Seguimiento de Progreso**: Sistema completo de estadísticas y análisis del desempeño del usuario
- 🖥️ **Interfaz Gráfica Moderna**: Desarrollada con PyQt6, intuitiva y fácil de usar
- 👤 **Gestión de Usuarios**: Múltiples perfiles con progreso individual y personalización

---

## 🏗️ Arquitectura del Sistema

### Estructura del Proyecto

```
aprendizaje_ingles/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── data/                   # Datos del sistema
│   ├── a_p.json           # Base de datos de palabras (600k+ palabras)
│   ├── usuarios/          # Perfiles de usuario
│   └── progreso/          # Progreso individual por usuario
├── interfaz/              # Capa de presentación (GUI)
│   ├── app.py            # Aplicación principal PyQt6
│   ├── main_window.py    # Ventana principal
│   ├── componentes/      # Componentes reutilizables
│   ├── ventanas/         # Ventanas secundarias
│   └── estilos/          # Hojas de estilo QSS
├── lenguaje/             # Motor de procesamiento lingüístico
│   ├── grafo_palabras.py # Implementación del grafo semántico
│   ├── motor_srs.py      # Sistema de repetición espaciada
│   ├── diccionario.py    # Gestión del diccionario
│   ├── analizador.py     # Análisis léxico
│   └── generador_oraciones.py # Generación de oraciones
├── retos/                # Sistema de ejercicios
│   ├── base.py          # Clase base abstracta
│   ├── tarjetas.py      # Reto de tarjetas de memoria
│   ├── formar_palabras.py # Reto de formar palabras
│   └── oraciones.py     # Reto de construcción de oraciones
├── usuario/              # Gestión de usuarios
│   ├── perfil.py        # Perfil de usuario
│   ├── progreso.py      # Seguimiento de progreso
│   └── estadistica.py   # Análisis estadístico
└── utils/               # Utilidades generales
    ├── loggers.py       # Sistema de logging
    └── validadores.py   # Validación de datos
```

---

## 🔧 Módulos Principales

### 1. **Lenguaje** (`lenguaje/`)
Motor central del sistema que maneja el procesamiento lingüístico.

- **`grafo_palabras.py`**: Implementa la estructura de grafo que conecta palabras mediante relaciones semánticas. Permite búsquedas por categoría, dominio, tema y nivel.
- **`motor_srs.py`**: Implementación del algoritmo SM-2 para calcular intervalos de repaso óptimos basados en el desempeño del usuario.
- **`diccionario.py`**: Gestiona el acceso a la base de datos de palabras con definiciones, ejemplos, sinónimos y traducciones.
- **`generador_oraciones.py`**: Genera oraciones contextuales usando las relaciones del grafo.
- **`analizador.py`**: Analiza y categoriza palabras según sus propiedades lingüísticas.

### 2. **Retos** (`retos/`)
Sistema modular de ejercicios con diferentes tipos de práctica.

- **`base.py`**: Clase abstracta que define la interfaz común para todos los retos.
- **`tarjetas.py`**: Flashcards tradicionales con modo de reconocimiento o producción.
- **`formar_palabras.py`**: Ejercicio de ordenar letras para formar palabras correctas.
- **`oraciones.py`**: Construcción de oraciones usando palabras relacionadas.
- **`generador.py`**: Factory para crear retos según el nivel y preferencias del usuario.

### 3. **Usuario** (`usuario/`)
Gestión completa de perfiles y progreso.

- **`perfil.py`**: Información del usuario, preferencias y configuración personalizada.
- **`progreso.py`**: Seguimiento detallado del avance por palabra (estado SRS, intentos, aciertos).
- **`estadistica.py`**: Análisis y métricas del desempeño del usuario.

### 4. **Interfaz** (`interfaz/`)
Interfaz gráfica desarrollada con PyQt6.

- **`app.py`**: Aplicación principal y configuración global.
- **`main_window.py`**: Ventana principal con navegación y contenido dinámico.
- **`componentes/`**: Widgets reutilizables (header, gráficos, selectores, retos).
- **`ventanas/`**: Ventanas secundarias (login, práctica, estadísticas).

---

## 📦 Librerías Externas

El proyecto utiliza las siguientes dependencias:

### Obligatorias
- **Python 3.13.5**: Versión requerida del intérprete
- **PyQt6 6.5.0**: Framework para la interfaz gráfica
  - `PyQt6-Qt6 6.5.0`: Bindings de Qt6
  - `PyQt6-sip 13.5.0`: Módulo SIP para PyQt6

### Estándar (incluidas en Python)
- `json`: Manejo de archivos JSON
- `datetime`: Gestión de fechas y tiempos
- `typing`: Anotaciones de tipos
- `abc`: Clases abstractas
- `random`: Generación de contenido aleatorio
- `hashlib`: Generación de IDs únicos

---

## 💻 Requerimientos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Linux, Windows, macOS
- **Python**: 3.13.5 o superior
- **Espacio en Disco**: 150 MB (incluye base de datos de palabras)

### Requisitos de Software
- pip (gestor de paquetes de Python)
- Entorno gráfico (para la interfaz GUI)

---

## 🚀 Instalación y Uso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JsebastianPe06/aprendizaje_ingles.git
cd aprendizaje_ingles
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

#### Interfaz Gráfica (Recomendado)

```bash
python main.py --gui
```

o simplemente:

```bash
python main.py
```

### 5. Primer Uso

1. **Crear Usuario**: En la pantalla de login, ingresa tu nombre para crear un nuevo perfil
2. **Seleccionar Nivel**: Elige tu nivel de inglés (Básico, Intermedio, Avanzado)
3. **Comenzar Práctica**: Selecciona el tipo de reto que deseas realizar
4. **Ver Estadísticas**: Accede a tu progreso y métricas desde el menú principal



## 👨‍💻 Autores

**Sebastián** - [JsebastianPe06](https://github.com/JsebastianPe06)

---

