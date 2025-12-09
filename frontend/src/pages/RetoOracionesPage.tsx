import React, { useState } from 'react';
import { learningAPI } from '../services/api';
import './RetoOracionesPage.css';

interface Reto {
  tipo: string;
  palabra_clave: string;
  instruccion: string;
  nivel: string;
  validacion_requerida: boolean;
}

interface Validacion {
  valida: boolean;
  tiene_palabra_clave: boolean;
  mensaje: string;
}

const RetoOracionesPage: React.FC = () => {
  const [nivel, setNivel] = useState<'basico' | 'intermedio' | 'avanzado'>('basico');
  const [palabra, setPalabra] = useState('');
  const [reto, setReto] = useState<Reto | null>(null);
  const [oracion, setOracion] = useState('');
  const [validacion, setValidacion] = useState<Validacion | null>(null);
  const [loading, setLoading] = useState(false);
  const [historial, setHistorial] = useState<{ palabra: string; oracion: string; valida: boolean }[]>([]);

  const generarReto = async () => {
    if (!palabra.trim()) {
      alert('Por favor ingresa una palabra');
      return;
    }

    setLoading(true);
    try {
      const response = await learningAPI.generateOracionReto(palabra, nivel);
      setReto(response.data.data);
      setOracion('');
      setValidacion(null);
    } catch (error) {
      console.error('Error generating reto:', error);
      alert('Error al generar el reto');
    } finally {
      setLoading(false);
    }
  };

  const validarOracion = async () => {
    if (!reto || !oracion.trim()) {
      alert('Por favor escribe una oración');
      return;
    }

    setLoading(true);
    try {
      const response = await learningAPI.validarOracion(oracion, reto.palabra_clave);
      setValidacion(response.data.data);
    } catch (error) {
      console.error('Error validating sentence:', error);
      alert('Error al validar la oración');
    } finally {
      setLoading(false);
    }
  };

  const guardarIntento = () => {
    if (validacion && reto) {
      setHistorial([
        ...historial,
        {
          palabra: reto.palabra_clave,
          oracion: oracion,
          valida: validacion.valida
        }
      ]);
      resetReto();
    }
  };

  const resetReto = () => {
    setReto(null);
    setOracion('');
    setValidacion(null);
    setPalabra('');
  };

  const getNivelColor = (nivelText: string) => {
    switch (nivelText) {
      case 'basico':
        return '#28a745';
      case 'intermedio':
        return '#ffc107';
      case 'avanzado':
        return '#dc3545';
      default:
        return '#667eea';
    }
  };

  return (
    <div className="reto-oraciones-page">
      <div className="reto-header">
        <h1>📝 Reto: Construir Oraciones</h1>
        <p>Crea oraciones correctas en inglés con la palabra indicada</p>
      </div>

      <div className="reto-container">
        {!reto ? (
          // Setup
          <div className="setup-section">
            <div className="setup-card">
              <h2>Configura tu desafío</h2>

              <div className="config-group">
                <label>Nivel de Dificultad:</label>
                <div className="nivel-buttons">
                  {['basico', 'intermedio', 'avanzado'].map((nivelOption) => (
                    <button
                      key={nivelOption}
                      className={`nivel-btn ${nivel === nivelOption ? 'active' : ''}`}
                      onClick={() => setNivel(nivelOption as any)}
                      style={{
                        borderColor: getNivelColor(nivelOption),
                        color: nivel === nivelOption ? 'white' : getNivelColor(nivelOption),
                        background: nivel === nivelOption ? getNivelColor(nivelOption) : 'white'
                      }}
                    >
                      {nivelOption.charAt(0).toUpperCase() + nivelOption.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="config-group">
                <label>Palabra Clave:</label>
                <div className="input-group">
                  <input
                    type="text"
                    placeholder="Ingresa una palabra en inglés..."
                    value={palabra}
                    onChange={(e) => setPalabra(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && generarReto()}
                  />
                  <button
                    className="btn btn-primary"
                    onClick={generarReto}
                    disabled={loading}
                  >
                    {loading ? 'Generando...' : 'Generar Reto'}
                  </button>
                </div>
              </div>

              <div className="palabras-sugeridas">
                <p>Palabras sugeridas:</p>
                <div className="tags">
                  {['happy', 'beautiful', 'run', 'study', 'enjoy'].map((word) => (
                    <button
                      key={word}
                      className="tag"
                      onClick={() => setPalabra(word)}
                    >
                      {word}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {historial.length > 0 && (
              <div className="historial-card">
                <h3>📋 Historial de Intentos</h3>
                <div className="historial-items">
                  {historial.map((item, idx) => (
                    <div key={idx} className={`historial-item ${item.valida ? 'valida' : 'invalida'}`}>
                      <div className="item-header">
                        <span className="palabra-badge">{item.palabra}</span>
                        <span className={`estado ${item.valida ? 'ok' : 'error'}`}>
                          {item.valida ? '✅ Válida' : '❌ Inválida'}
                        </span>
                      </div>
                      <p className="oracion-text">"{item.oracion}"</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          // Game
          <div className="game-section">
            <div className="game-card">
              <div className="game-header">
                <div className="palabra-info">
                  <span className="nivel-badge" style={{ background: getNivelColor(reto.nivel) }}>
                    {reto.nivel.toUpperCase()}
                  </span>
                  <span className="palabra-actual">Palabra: <strong>{reto.palabra_clave}</strong></span>
                </div>
              </div>

              <div className="instruccion">
                <h2>{reto.instruccion}</h2>
              </div>

              <div className="oracion-input-container">
                <textarea
                  placeholder="Escribe tu oración aquí..."
                  value={oracion}
                  onChange={(e) => setOracion(e.target.value)}
                  disabled={validacion !== null}
                  rows={4}
                />
                <div className="char-count">
                  {oracion.length} caracteres
                </div>
                {!validacion && (
                  <button
                    className="btn btn-primary btn-block"
                    onClick={validarOracion}
                    disabled={loading || !oracion.trim()}
                  >
                    {loading ? 'Validando...' : 'Validar Oración'}
                  </button>
                )}
              </div>

              {validacion && (
                <div className={`validacion-resultado ${validacion.valida ? 'valida' : 'invalida'}`}>
                  <div className="resultado-header">
                    <h3>
                      {validacion.valida ? '✅ ¡Excelente!' : '❌ Necesita mejora'}
                    </h3>
                  </div>

                  <div className="validacion-detalles">
                    <p>
                      <strong>Contiene la palabra clave:</strong>{' '}
                      {validacion.tiene_palabra_clave ? '✓ Sí' : '✗ No'}
                    </p>
                    <p>
                      <strong>Mensaje:</strong> {validacion.mensaje}
                    </p>
                  </div>

                  <div className="resultado-buttons">
                    <button className="btn btn-secondary" onClick={resetReto}>
                      Nuevo Reto
                    </button>
                    {validacion.valida && (
                      <>
                        <button className="btn btn-success" onClick={guardarIntento}>
                          💾 Guardar Intento
                        </button>
                      </>
                    )}
                  </div>
                </div>
              )}

              {validacion && !validacion.valida && (
                <div className="sugerencias">
                  <h4>💡 Sugerencias:</h4>
                  <ul>
                    <li>Verifica que la oración tenga al menos 3 palabras</li>
                    <li>Asegúrate de incluir la palabra clave: <strong>{reto.palabra_clave}</strong></li>
                    <li>Termina la oración con puntuación (. ! ?)</li>
                    <li>Revisa la gramática y ortografía</li>
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RetoOracionesPage;