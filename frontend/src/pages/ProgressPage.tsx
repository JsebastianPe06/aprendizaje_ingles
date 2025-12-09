import React, { useState, useEffect } from 'react';
import { learningAPI } from '../services/api';
import './ProgressPage.css';

interface CategoriaProgreso {
  completed: number;
  total: number;
  percentage: number;
}

interface Progreso {
  userId: number;
  totalLessons: number;
  completedLessons: number;
  percentage: number;
  streak: number;
  categories: {
    vocabulary: CategoriaProgreso;
    flashcards: any;
    srs: any;
  };
}

const ProgressPage: React.FC = () => {
  const [progreso, setProgreso] = useState<Progreso | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const response = await learningAPI.getProgress();
        setProgreso(response.data.data);
      } catch (error) {
        console.error('Error fetching progress:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, []);

  if (loading) return <div className="loading">Cargando progreso...</div>;

  if (!progreso) return <div className="error">Error al cargar el progreso</div>;

  const getStreakEmoji = (streak: number) => {
    if (streak >= 30) return '🔥';
    if (streak >= 14) return '🌟';
    if (streak >= 7) return '⭐';
    return '📝';
  };

  return (
    <div className="progress-page">
      <h1>📊 Mi Progreso</h1>

      <div className="progress-container">
        {/* Tarjeta Principal */}
        <div className="main-progress">
          <div className="progress-circle">
            <svg viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="45" className="bg-circle" />
              <circle 
                cx="50" 
                cy="50" 
                r="45" 
                className="progress-circle-fill"
                style={{
                  strokeDasharray: `${progreso.percentage * 2.827} 282.7`
                }}
              />
            </svg>
            <div className="circle-text">
              <span className="percentage">{progreso.percentage}%</span>
              <span className="label">Progreso Total</span>
            </div>
          </div>

          <div className="progress-stats">
            <div className="progress-item">
              <span className="label">Lecciones Completadas</span>
              <span className="value">
                {progreso.completedLessons} de {progreso.totalLessons}
              </span>
              <div className="mini-bar">
                <div 
                  className="mini-bar-fill"
                  style={{
                    width: `${(progreso.completedLessons / progreso.totalLessons) * 100}%`
                  }}
                ></div>
              </div>
            </div>

            <div className="progress-item">
              <span className="label">Racha</span>
              <span className="value streak">
                {getStreakEmoji(progreso.streak)} {progreso.streak} días
              </span>
            </div>
          </div>
        </div>

        {/* Categorías */}
        <div className="categories-progress">
          <h2>Categorías de Aprendizaje</h2>

          <div className="category-card">
            <div className="category-header">
              <h3>📖 Vocabulario</h3>
              <span className="percentage-badge">
                {progreso.categories.vocabulary.percentage}%
              </span>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-bar-fill"
                style={{
                  width: `${progreso.categories.vocabulary.percentage}%`
                }}
              ></div>
            </div>
            <p className="category-stat">
              {progreso.categories.vocabulary.completed} de {progreso.categories.vocabulary.total} palabras
            </p>
          </div>

          <div className="category-card">
            <div className="category-header">
              <h3>📚 Flashcards</h3>
              <span className="percentage-badge">
                {progreso.categories.flashcards.tasa_exito}%
              </span>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-bar-fill"
                style={{
                  width: `${progreso.categories.flashcards.tasa_exito}%`
                }}
              ></div>
            </div>
            <p className="category-stat">
              {progreso.categories.flashcards.tarjetas_estudiadas} de {progreso.categories.flashcards.total_tarjetas} tarjetas estudiadas
            </p>
          </div>

          <div className="category-card">
            <div className="category-header">
              <h3>🔄 SRS</h3>
              <span className="percentage-badge">
                {progreso.categories.srs.tasa_exito}%
              </span>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-bar-fill"
                style={{
                  width: `${progreso.categories.srs.tasa_exito}%`
                }}
              ></div>
            </div>
            <p className="category-stat">
              {progreso.categories.srs.revisions_completadas} revisiones completadas
            </p>
          </div>
        </div>

        {/* Estadísticas Detalladas */}
        <div className="detailed-stats">
          <h2>Estadísticas Detalladas</h2>
          <div className="stats-grid">
            <div className="stat-box">
              <span className="icon">📝</span>
              <span className="title">Total de Lecciones</span>
              <span className="value">{progreso.totalLessons}</span>
            </div>
            <div className="stat-box">
              <span className="icon">✅</span>
              <span className="title">Lecciones Completadas</span>
              <span className="value">{progreso.completedLessons}</span>
            </div>
            <div className="stat-box">
              <span className="icon">📚</span>
              <span className="title">Tarjetas Estudiadas</span>
              <span className="value">
                {progreso.categories.flashcards.tarjetas_estudiadas}
              </span>
            </div>
            <div className="stat-box">
              <span className="icon">🔄</span>
              <span className="title">Revisiones SRS</span>
              <span className="value">
                {progreso.categories.srs.revisions_completadas}
              </span>
            </div>
          </div>
        </div>

        {/* Consejos */}
        <div className="tips-section">
          <h2>💡 Consejos para Mejorar</h2>
          <div className="tips-grid">
            {progreso.percentage < 25 && (
              <div className="tip">
                <p>¡Acabas de empezar! Continúa estudiando regularmente para alcanzar tus objetivos.</p>
              </div>
            )}
            {progreso.percentage >= 25 && progreso.percentage < 50 && (
              <div className="tip">
                <p>¡Buen comienzo! Mantén la consistencia y verás resultados cada vez mejores.</p>
              </div>
            )}
            {progreso.percentage >= 50 && progreso.percentage < 75 && (
              <div className="tip">
                <p>¡Vas muy bien! Ya tienes una buena base. Aumenta la dificultad para avanzar más.</p>
              </div>
            )}
            {progreso.percentage >= 75 && (
              <div className="tip">
                <p>¡Excelente progreso! Casi estás en la meta. Sigue adelante con determinación.</p>
              </div>
            )}

            {progreso.streak >= 7 && (
              <div className="tip">
                <p>🔥 ¡Racha de {progreso.streak} días! Mantén la consistencia para llegar a 30 días.</p>
              </div>
            )}

            {progreso.categories.srs.tasa_exito < 60 && (
              <div className="tip">
                <p>Considera revisar las palabras del SRS más frecuentemente. ¡Refuerza lo aprendido!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressPage;