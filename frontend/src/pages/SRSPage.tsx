import React, { useState, useEffect } from 'react';
import { learningAPI } from '../services/api';
import './SRSPage.css';

interface PalabraRevision {
  palabra: string;
  intervalo: number;
  proxima_revision: string;
  veces_revisada: number;
  dificultad: number;
}

interface EstadisticasSRS {
  total_palabras: number;
  palabras_pendientes: number;
  revisions_completadas: number;
  tasa_exito: number;
}

const SRSPage: React.FC = () => {
  const [estadisticas, setEstadisticas] = useState<EstadisticasSRS | null>(null);
  const [proximasPalabras, setProximasPalabras] = useState<PalabraRevision[]>([]);
  const [loading, setLoading] = useState(true);
  const [estudiando, setEstudiando] = useState(false);
  const [indexActual, setIndexActual] = useState(0);
  const [mostrarRespuesta, setMostrarRespuesta] = useState(false);

  useEffect(() => {
    fetchEstadisticas();
  }, []);

  const fetchEstadisticas = async () => {
    try {
      const [estResponse, proximasResponse] = await Promise.all([
        learningAPI.getEstadisticasSRS(),
        learningAPI.getProximasRevisiones()
      ]);
      setEstadisticas(estResponse.data.data);
      setProximasPalabras(proximasResponse.data.data.palabras);
    } catch (error) {
      console.error('Error fetching SRS data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRespuesta = async (correcto: boolean) => {
    try {
      const palabra = proximasPalabras[indexActual];
      await learningAPI.actualizarRevisionSRS(palabra.palabra, correcto);

      if (indexActual < proximasPalabras.length - 1) {
        setIndexActual(indexActual + 1);
        setMostrarRespuesta(false);
      } else {
        setEstudiando(false);
        await fetchEstadisticas();
        setIndexActual(0);
      }
    } catch (error) {
      console.error('Error updating SRS:', error);
    }
  };

  if (loading) return <div className="loading">Cargando sistema SRS...</div>;

  if (!estudiando) {
    return (
      <div className="srs-page">
        <div className="srs-header">
          <h1>🔄 Sistema de Repetición Espaciada</h1>
          <p>Revisa vocabulario de forma inteligente basada en tu desempeño</p>
        </div>

        {estadisticas && (
          <div className="estadisticas-srs">
            <div className="stat-card">
              <h3>Total de Palabras</h3>
              <p className="stat-number">{estadisticas.total_palabras}</p>
            </div>
            <div className="stat-card">
              <h3>Pendientes de Revisar</h3>
              <p className="stat-number">{estadisticas.palabras_pendientes}</p>
            </div>
            <div className="stat-card">
              <h3>Revisiones Completadas</h3>
              <p className="stat-number">{estadisticas.revisions_completadas}</p>
            </div>
            <div className="stat-card">
              <h3>Tasa de Éxito</h3>
              <p className="stat-number">{estadisticas.tasa_exito}%</p>
            </div>
          </div>
        )}

        {proximasPalabras.length > 0 ? (
          <>
            <div className="proximas-palabras">
              <h3>Palabras para revisar hoy ({proximasPalabras.length})</h3>
              <div className="palabras-list">
                {proximasPalabras.slice(0, 10).map((palabra, idx) => (
                  <div key={idx} className="palabra-item">
                    <span className="palabra">{palabra.palabra}</span>
                    <div className="palabra-info">
                      <span className={`dificultad-${Math.min(5, Math.ceil(palabra.dificultad))}`}>
                        Dificultad: {palabra.dificultad.toFixed(1)}
                      </span>
                      <span className="revisiones">
                        Revisiones: {palabra.veces_revisada}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="action-buttons">
              <button 
                className="btn btn-primary btn-grande"
                onClick={() => setEstudiando(true)}
              >
                Comenzar Revisión SRS
              </button>
            </div>
          </>
        ) : (
          <div className="no-content">
            <p>✓ No hay palabras pendientes de revisar en este momento</p>
            <p>¡Vuelve más tarde para continuar con tu aprendizaje!</p>
          </div>
        )}
      </div>
    );
  }

  // Modo estudio
  const palabra = proximasPalabras[indexActual];

  return (
    <div className="srs-page study-mode">
      <div className="srs-study-header">
        <h1>Revisión SRS</h1>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${((indexActual + 1) / proximasPalabras.length) * 100}%` }}
          ></div>
        </div>
        <span>{indexActual + 1} de {proximasPalabras.length}</span>
      </div>

      <div className="srs-card-container">
        <div className="srs-card">
          <div className="card-header">
            <h2>{palabra.palabra.toUpperCase()}</h2>
            <span className={`difficulty-badge difficulty-${Math.min(5, Math.ceil(palabra.dificultad))}`}>
              {palabra.dificultad.toFixed(1)} ★
            </span>
          </div>
          <div className="card-body">
            <p className="revisiones-info">
              Revisada {palabra.veces_revisada} veces
            </p>
            <p className="proximarevision-info">
              Próxima revisión: {new Date(palabra.proxima_revision).toLocaleDateString()}
            </p>
          </div>
        </div>

        {!mostrarRespuesta && (
          <button 
            className="btn btn-primary btn-reveal"
            onClick={() => setMostrarRespuesta(true)}
          >
            Ver Definición
          </button>
        )}

        {mostrarRespuesta && (
          <div className="srs-buttons">
            <button 
              className="btn btn-danger"
              onClick={() => handleRespuesta(false)}
            >
              ❌ Olvidé
            </button>
            <button 
              className="btn btn-warning"
              onClick={() => handleRespuesta(false)}
            >
              ⚠️ Difícil
            </button>
            <button 
              className="btn btn-success"
              onClick={() => handleRespuesta(true)}
            >
              ✅ Bien
            </button>
          </div>
        )}
      </div>

      <button 
        className="btn btn-secondary btn-exit"
        onClick={() => setEstudiando(false)}
      >
        Salir
      </button>
    </div>
  );
};

export default SRSPage;