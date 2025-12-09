import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { learningAPI } from '../services/api';
import './HomePage.css';

interface Vocabulary {
  word: string;
  definition: string;
}

const HomePage: React.FC = () => {
  const [vocabulary, setVocabulary] = useState<Vocabulary[]>([]);
  const [exercises, setExercises] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMaterials = async () => {
      try {
        const response = await learningAPI.getMaterials();
        setVocabulary(response.data.data.vocabulary);
        setExercises(response.data.data.exercises);
      } catch (err: any) {
        setError(err.message || 'Error al cargar materiales');
      } finally {
        setLoading(false);
      }
    };

    fetchMaterials();
  }, []);

  const handleStartLesson = (index: number) => {
    navigate(`/lesson/${index + 1}`);
  };

  if (loading) return <div className="loading">Cargando materiales...</div>;

  return (
    <div className="home-page">
      <header className="hero">
        <h1>🎓 Bienvenido al Sistema de Aprendizaje de Inglés</h1>
        <p>Aprende vocabulario y gramática de forma interactiva</p>
      </header>

      {error && <div className="error-message">{error}</div>}

      <section className="features">
        <div className="feature-card">
          <h3>📖 Vocabulario</h3>
          <p>{vocabulary.length} palabras para aprender</p>
        </div>
        <div className="feature-card">
          <h3>📝 Ejercicios</h3>
          <p>{exercises.length} ejercicios prácticos</p>
        </div>
        <div className="feature-card">
          <h3>🎯 Progreso</h3>
          <p>Monitorea tu avance en tiempo real</p>
        </div>
      </section>

      <section className="materials">
        <h2>Vocabulario Disponible</h2>
        <div className="materials-grid">
          {vocabulary.map((item, index) => (
            <div key={index} className="material-card">
              <div className="material-header">
                <h3>{item.word.toUpperCase()}</h3>
              </div>
              <p className="material-description">{item.definition}</p>
              <button 
                className="btn btn-primary"
                onClick={() => handleStartLesson(index)}
              >
                Aprender
              </button>
            </div>
          ))}
        </div>
      </section>

      {exercises.length > 0 && (
        <section className="exercises-section">
          <h2>Ejercicios Disponibles</h2>
          <div className="exercises-list">
            {exercises.map((exercise, index) => (
              <div key={index} className="exercise-item">
                <h4>{exercise.question}</h4>
                <p>Tipo: {exercise.type}</p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default HomePage;