"""
Main entry point of the backend application for the English learning system.
"""

import sys
import os
from flask_cors import CORS

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaz.api import app

# Enable CORS para todas las rutas
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)