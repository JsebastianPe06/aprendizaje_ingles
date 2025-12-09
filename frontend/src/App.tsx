import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import LessonPage from './pages/LessonPage';
import CategoriesPage from './pages/CategoriesPage';
import FlashcardsPage from './pages/FlashcardsPage';
import SRSPage from './pages/SRSPage';
import RetoFormarPalabrasPage from './pages/RetoFormarPalabrasPage';
import RetoOracionesPage from './pages/RetoOracionesPage';
import ProgressPage from './pages/ProgressPage';
import ProfilePage from './pages/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            {/* Rutas Principales */}
            <Route path="/" element={<HomePage />} />
            <Route path="/home" element={<HomePage />} />

            {/* Lecciones */}
            <Route path="/lessons" element={<LessonPage />} />
            <Route path="/lesson/:id" element={<LessonPage />} />

            {/* Categorías */}
            <Route path="/categories" element={<CategoriesPage />} />
            <Route path="/categoria/:nombre/estudio" element={<CategoriesPage />} />
            <Route path="/categorias/estudio" element={<CategoriesPage />} />

            {/* Flashcards */}
            <Route path="/flashcards" element={<FlashcardsPage />} />
            <Route path="/flashcards/:id" element={<FlashcardsPage />} />

            {/* Sistema de Repetición Espaciada (SRS) */}
            <Route path="/srs" element={<SRSPage />} />
            <Route path="/srs/review" element={<SRSPage />} />

            {/* Retos */}
            <Route path="/reto/formar-palabras" element={<RetoFormarPalabrasPage />} />
            <Route path="/reto/palabras" element={<RetoFormarPalabrasPage />} />
            <Route path="/retos/formar-palabras" element={<RetoFormarPalabrasPage />} />

            <Route path="/reto/oraciones" element={<RetoOracionesPage />} />
            <Route path="/reto/construir-oraciones" element={<RetoOracionesPage />} />
            <Route path="/retos/oraciones" element={<RetoOracionesPage />} />

            {/* Estadísticas y Perfil */}
            <Route path="/progress" element={<ProgressPage />} />
            <Route path="/estadisticas" element={<ProgressPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/perfil" element={<ProfilePage />} />

            {/* Rutas de Error */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;