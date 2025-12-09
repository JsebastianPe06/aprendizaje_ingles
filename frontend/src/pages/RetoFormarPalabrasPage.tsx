import React, { useState } from 'react';
import { learningAPI } from '../services/api';
import './RetoFormarPalabrasPage.css';

interface Reto {
  tipo: string;
  palabra_objetivo: string;
  letras_desordenadas: string[];
  dificultad: string;
}

interface ResultadoVerificacion {
  correcto: boolean;
  respuesta_correcta: string;
  respuesta_usuario: string;
  intentos: number;
}

const RetoFormarPalabrasPage: React.FC = () => {
  const [palabra, setPalabra] = useState('');
  const [reto, setReto] = useState<Reto | null>(null);
  const [respuesta, setRespuesta] = useState('');
  const [resultado, setResultado] = useState<ResultadoVerificacion | null>(null);
  const [loading, setLoading] = useState(false);
  const [historialRetos, setHistorialRetos] = useState<ResultadoVerificacion[]>([]);

  const generarReto = async () => {
    if (!palabra.trim()) {
      alert('Por favor ingresa una palabra');
      return;
    }

    setLoading(true);
    try {
      const response = await learningAPI.generateFormarPalabrasReto(palabra);
      setReto(response.data.data);
      setRespuesta('');
      setResultado(null);
    } catch (error) {
      console.error('Error generating reto:', error);
      alert('Error al generar el reto');
    } finally {
      setLoading(false);
    }
  };

  const verificarRespuesta = async () => {
    if (!reto || !respuesta.trim()) {
      alert('Por favor ingresa una respuesta');
      return;
    }

    setLoading(true);
    try {
      const response = await learningAPI.verifyFormarPalabras(
        reto.palabra_objetivo,
        respuesta
      );
      const resultData = response.data.data;
      setResultado(resultData);
      setHistorialRetos([...historialRetos, resultData]);
    } catch (error) {
      console.error('Error verifying answer:', error);
      alert('Error al verificar la respuesta');
    } finally {
      setLoading(false);
    }
  };

  const resetReto = () => {
    setReto(null);
    setRespuesta('');
    setResultado(null);
    setPalabra('');
  };

  const getDificultadColor = (dificultad: string) => {
    switch (dificultad) {
      case 'facil':
        return '#28a745';
      case 'media':
        return '#ffc107';
      case 'dificil':
        return '#dc3545';
      default:
        return '#667eea';
    }
  };

  return (
    <div className="reto-formar-palabras-page">
      <div className="reto-header">
        <h1>🔤 Reto: Formar Palabras</h1>
        <p>Ordena las letras para formar la palabra correcta</p>
      </div>

      <div className="reto-container">
        {!reto ? (
          // Formulario para generar reto
          <div className="reto-setup">
            <div className="setup-card">
              <h2>Elige una palabra para el reto</h2>
              <div className="input-group">
                <input
                  type="text"
                  placeholder="Ingresa una palabra en inglés..."
                  value={palabra}
                  onChange={(e) => setPalabra(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && generarReto()}
                  disabled={loading}
                />
                <button
                  className="btn btn-primary"
                  onClick={generarReto}
                  disabled={loading}
                >
                  {loading ? 'Generando...' : 'Generar Reto'}
                </button>
              </div>

              <div className="ejemplos">
                <h3>Palabras sugeridas:</h3>
                <div className="ejemplo-tags">
                  {['hello', 'world', 'learning', 'english', 'computer'].map((word) => (
                    <button
                      key={word}
                      className="ejemplo-tag"
                      onClick={() => {
                        setPalabra(word);
                      }}
                    >
                      {word}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {historialRetos.length > 0 && (
              <div className="historial">
                <h3>Historial de Retos</h3>
                <div className="historial-list">
                  {historialRetos.map((item, idx) => (
                    <div key={idx} className={`historial-item ${item.correcto ? 'correcto' : 'incorrecto'}`}>
                      <span className="resultado-icon">
                        {item.correcto ? '✅' : '❌'}
                      </span>
                      <div className="resultado-info">
                        <p className="respuesta-correcta">
                          Palabra: <strong>{item.respuesta_correcta}</strong>
                        </p>
                        <p className="intentos">
                          Intentos: <strong>{item.intentos}</strong>
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          // Reto activo
          <div className="reto-game">
            <div className="game-header">
              <div className="dificultad-badge" style={{ background: getDificultadColor(reto.dificultad) }}>
                Dificultad: {reto.dificultad}
              </div>
              {resultado && (
                <div className={`resultado-badge ${resultado.correcto ? 'correcto' : 'incorrecto'}`}>
                  {resultado.correcto ? '✅ ¡Correcto!' : '❌ Incorrecto'}
                </div>
              )}
            </div>

            <div className="letras-container">
              <h2>Ordena estas letras:</h2>
              <div className="letras-grid">
                {reto.letras_desordenadas.map((letra, idx) => (
                  <div key={idx} className="letra-card">
                    {letra.toUpperCase()}
                  </div>
                ))}
              </div>
            </div>

            <div className="respuesta-input">
              <input
                type="text"
                placeholder="Escribe la palabra aquí..."
                value={respuesta}
                onChange={(e) => setRespuesta(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !resultado && verificarRespuesta()}
                disabled={resultado !== null}
              />
              {!resultado && (
                <button
                  className="btn btn-primary"
                  onClick={verificarRespuesta}
                  disabled={loading}
                >
                  {loading ? 'Verificando...' : 'Verificar'}
                </button>
              )}
            </div>

            {resultado && (
              <div className={`resultado-card ${resultado.correcto ? 'correcto' : 'incorrecto'}`}>
                <h3>{resultado.correcto ? '¡Excelente!' : 'Intenta nuevamente'}</h3>
                <p>Palabra correcta: <strong>{resultado.respuesta_correcta}</strong></p>
                <p>Tu respuesta: <strong>{resultado.respuesta_usuario}</strong></p>
                <p>Intentos: <strong>{resultado.intentos}</strong></p>

                <div className="resultado-buttons">
                  <button className="btn btn-secondary" onClick={resetReto}>
                    Nuevo Reto
                  </button>
                  {resultado.correcto && (
                    <button className="btn btn-success">
                      ⭐ Siguiente Desafío
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default RetoFormarPalabrasPage;