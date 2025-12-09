import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const learningAPI = {
  // Home
  getHome: () => api.get('/home'),

  // Lecciones
  getLessons: () => api.get('/lessons'),
  getLesson: (id: string | number) => api.get(`/lessons/${id}`),
  submitQuiz: (data: { lessonId: string | number; score: number; total: number }) =>
    api.post('/lessons/submit', data),
  getMaterials: (lessonId?: string | number) => 
    api.get(lessonId ? `/lessons/${lessonId}/materials` : '/materials'),

  // Categorías
  getCategories: () => api.get('/categories'),
  getCategoryVocabulary: (name: string) => api.get(`/categories/${name}`),

  // Flashcards
  getFlashcards: () => api.get('/flashcards'),
  submitFlashcardAnswer: (cardId: number, correct: boolean) =>
    api.post(`/flashcards/${cardId}/answer`, { correcto: correct }),

  // SRS
  getEstadisticasSRS: () => api.get('/srs/estadisticas'),
  getProximasRevisiones: () => api.get('/srs/proximas-revisiones'),
  actualizarRevisionSRS: (palabra: string, correcto: boolean) =>
    api.post('/srs/revisar', { palabra, correcto }),

  // Retos - Formar Palabras
  generateFormarPalabrasReto: (palabra: string) =>
    api.post('/retos/formar-palabras/generar', { palabra }),
  verifyFormarPalabras: (palabra: string, respuesta: string) =>
    api.post('/retos/formar-palabras/verificar', { palabra, respuesta }),

  // Retos - Oraciones
  generateOracionReto: (palabra: string, nivel: string) =>
    api.post('/retos/oraciones/generar', { palabra, nivel }),
  validarOracion: (oracion: string, palabraClave: string) =>
    api.post('/retos/oraciones/validar', { oracion, palabra_clave: palabraClave }),

  // Progreso
  getProgress: () => api.get('/progress'),
  getEstadisticas: () => api.get('/estadisticas'),

  // Usuario
  getUsers: () => api.get('/users/me'),
  updateProfile: (data: any) => api.put('/users/me', data),

  // Análisis de Texto
  analyzeText: (text: string) => api.post('/analyze', { text }),
};

export default api;