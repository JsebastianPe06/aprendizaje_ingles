import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { learningAPI } from '../services/api';
import './LessonPage.css';

interface Exercise {
  question: string;
  options: string[];
  answer: string;
}

interface Lesson {
  id: number;
  title: string;
  content: string;
  word: string;
  exercises: Exercise[];
}

const LessonPage: React.FC = () => {
  const { lessonId } = useParams<{ lessonId: string }>();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [currentExercise, setCurrentExercise] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [score, setScore] = useState(0);
  const [completed, setCompleted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLesson = async () => {
      try {
        const id = lessonId || '1';
        const response = await learningAPI.getLesson(id);
        setLesson(response.data.data);
      } catch (error) {
        console.error('Error fetching lesson:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLesson();
  }, [lessonId]);

  const handleSubmitAnswer = () => {
    if (!lesson) return;

    const exercise = lesson.exercises[currentExercise];
    const correct = selectedAnswer === exercise.answer;
    
    setIsCorrect(correct);
    setShowFeedback(true);

    if (correct) {
      setScore(score + 1);
    }

    setTimeout(() => {
      if (currentExercise < lesson.exercises.length - 1) {
        setCurrentExercise(currentExercise + 1);
        setSelectedAnswer('');
        setShowFeedback(false);
      } else {
        setCompleted(true);
        // Enviar resultados del quiz
        const finalScore = correct ? score + 1 : score;
        learningAPI.submitQuiz({ 
          lessonId: lesson.id, 
          score: finalScore, 
          total: lesson.exercises.length 
        }).catch(error => console.error('Error submitting quiz:', error));
      }
    }, 1500);
  };

  if (loading) return <div className="loading">Cargando lección...</div>;
  if (!lesson) return <div className="error">Lección no encontrada</div>;

  if (completed) {
    const finalScore = showFeedback && isCorrect ? score : score;
    const percentage = ((finalScore / lesson.exercises.length) * 100).toFixed(0);
    
    return (
      <div className="lesson-page">
        <div className="completion-card">
          <h2>¡Lección Completada! 🎉</h2>
          <p className="word-learned">Palabra aprendida: <strong>{lesson.word.toUpperCase()}</strong></p>
          <div className="score-display">
            <div className="score-circle">
              <span className="percentage">{percentage}%</span>
            </div>
          </div>
          <p>Obtuviste {finalScore} de {lesson.exercises.length} respuestas correctas</p>
          <div className="button-group">
            <button className="btn btn-primary" onClick={() => navigate('/')}>
              Volver al Inicio
            </button>
            <button className="btn btn-secondary" onClick={() => navigate('/progress')}>
              Ver Progreso
            </button>
          </div>
        </div>
      </div>
    );
  }

  const exercise = lesson.exercises[currentExercise];

  return (
    <div className="lesson-page">
      <div className="lesson-header">
        <h1>{lesson.title}</h1>
        <p className="lesson-definition">{lesson.content}</p>
        <div className="progress-indicator">
          <span>{currentExercise + 1} de {lesson.exercises.length}</span>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${((currentExercise + 1) / lesson.exercises.length) * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      <div className="exercise-card">
        <h3>{exercise.question}</h3>
        <div className="options">
          {exercise.options.map((option) => (
            <label 
              key={option} 
              className={`option ${selectedAnswer === option ? 'selected' : ''}`}
            >
              <input
                type="radio"
                name="answer"
                value={option}
                checked={selectedAnswer === option}
                onChange={(e) => setSelectedAnswer(e.target.value)}
                disabled={showFeedback}
              />
              <span className="option-text">{option}</span>
            </label>
          ))}
        </div>

        {showFeedback && (
          <div className={`feedback ${isCorrect ? 'correct' : 'incorrect'}`}>
            {isCorrect ? '✓ ¡Correcto!' : '✗ Incorrecto'}
            {!isCorrect && <p>La respuesta correcta es: {exercise.answer}</p>}
          </div>
        )}
      </div>

      <div className="button-group">
        <button 
          className="btn btn-primary"
          onClick={handleSubmitAnswer}
          disabled={!selectedAnswer || showFeedback}
        >
          {currentExercise === lesson.exercises.length - 1 ? 'Finalizar' : 'Siguiente'}
        </button>
      </div>
    </div>
  );
};

export default LessonPage;