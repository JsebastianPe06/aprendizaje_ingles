import React, { useState, useEffect } from 'react';
import { learningAPI } from '../services/api';
import './FlashcardsPage.css';

interface Flashcard {
  id: number;
  pregunta: string;
  respuesta: string;
  dificultad: string;
  intentos: number;
  aciertos: number;
}

interface Estadisticas {
  total_tarjetas: number;
  total_intentos: number;
  total_aciertos: number;
  tasa_exito: number;
  tarjetas_estudiadas: number;
  tarjetas_sin_estudiar: number;
}

const FlashcardsPage: React.FC = () => {
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [estadisticas, setEstadisticas] = useState<Estadisticas | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [estudiar, setEstudiar] = useState(false);

  useEffect(() => {
    const fetchFlashcards = async () => {
      try {
        const response = await learningAPI.getFlashcards();
        setFlashcards(response.data.data.tarjetas);
        setEstadisticas(response.data.data.estadisticas);
      } catch (error) {
        console.error('Error fetching flashcards:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFlashcards();
  }, []);

  const handleSubmitAnswer = async (correcto: boolean) => {
    try {
      const tarjeta = flashcards[currentIndex];
      await learningAPI.submitFlashcardAnswer(tarjeta.id, correcto);
      
      if (currentIndex < flashcards.length - 1) {
        setCurrentIndex(currentIndex + 1);
        setIsFlipped(false);
      } else {
        setEstudiar(false);
        // Recargar estadísticas
        const response = await learningAPI.getFlashcards();
        setEstadisticas(response.data.data.estadisticas);
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  const handleNext = () => {
    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setIsFlipped(false);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setIsFlipped(false);
    }
  };

  if (loading) return <div className="loading">Cargando flashcards...</div>;

  if (!estudiar) {
    return (
      <div className="flashcards-page">
        <div className="flashcards-header">
          <h1>📚 Flashcards de Estudio</h1>
          <p>Estudia vocabulario con tarjetas interactivas</p>
        </div>

        {estadisticas && (
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total de Tarjetas</h3>
              <p className="stat-number">{estadisticas.total_tarjetas}</p>
            </div>
            <div className="stat-card">
              <h3>Tarjetas Estudiadas</h3>
              <p className="stat-number">{estadisticas.tarjetas_estudiadas}</p>
            </div>
            <div className="stat-card">
              <h3>Tasa de Éxito</h3>
              <p className="stat-number">{estadisticas.tasa_exito}%</p>
            </div>
            <div className="stat-card">
              <h3>Aciertos</h3>
              <p className="stat-number">{estadisticas.total_aciertos}</p>
            </div>
          </div>
        )}

        <div className="flashcards-container">
          <h2>Tus Flashcards</h2>
          <div className="flashcards-grid">
            {flashcards.map((card, index) => (
              <div key={card.id} className="flashcard-preview">
                <div className="card-number">{index + 1}</div>
                <h4>{card.pregunta}</h4>
                <span className={`difficulty ${card.dificultad}`}>
                  {card.dificultad}
                </span>
                <p className="card-stats">
                  {card.aciertos}/{card.intentos} aciertos
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="action-buttons">
          <button 
            className="btn btn-primary btn-large"
            onClick={() => setEstudiar(true)}
          >
            Comenzar a Estudiar
          </button>
        </div>
      </div>
    );
  }

  // Vista de estudio
  const tarjeta = flashcards[currentIndex];

  return (
    <div className="flashcards-page study-mode">
      <div className="study-header">
        <h1>Estudiando Flashcards</h1>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${((currentIndex + 1) / flashcards.length) * 100}%` }}
          ></div>
        </div>
        <span>{currentIndex + 1} de {flashcards.length}</span>
      </div>

      <div className="flashcard-container">
        <div 
          className={`flashcard ${isFlipped ? 'flipped' : ''}`}
          onClick={() => setIsFlipped(!isFlipped)}
        >
          <div className="flashcard-inner">
            <div className="flashcard-front">
              <p className="label">Pregunta</p>
              <h2>{tarjeta.pregunta}</h2>
              <p className="hint">Haz click para ver la respuesta</p>
            </div>
            <div className="flashcard-back">
              <p className="label">Respuesta</p>
              <h2>{tarjeta.respuesta}</h2>
            </div>
          </div>
        </div>
      </div>

      <div className="difficulty-badge">
        Dificultad: <span className={tarjeta.dificultad}>{tarjeta.dificultad}</span>
      </div>

      {isFlipped && (
        <div className="answer-buttons">
          <button 
            className="btn btn-danger"
            onClick={() => handleSubmitAnswer(false)}
          >
            ❌ Incorrecta
          </button>
          <button 
            className="btn btn-success"
            onClick={() => handleSubmitAnswer(true)}
          >
            ✅ Correcta
          </button>
        </div>
      )}

      <div className="navigation-buttons">
        <button 
          className="btn btn-secondary"
          onClick={handlePrevious}
          disabled={currentIndex === 0}
        >
          ← Anterior
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setEstudiar(false)}
        >
          Salir
        </button>
        <button 
          className="btn btn-secondary"
          onClick={handleNext}
          disabled={currentIndex === flashcards.length - 1}
        >
          Siguiente →
        </button>
      </div>
    </div>
  );
};

export default FlashcardsPage;