import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar: React.FC = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-logo" onClick={closeMenu}>
          🌍 English Learning
        </Link>

        {/* Hamburger Menu */}
        <div className={`hamburger ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
          <span></span>
          <span></span>
          <span></span>
        </div>

        {/* Menu */}
        <ul className={`nav-menu ${menuOpen ? 'active' : ''}`}>
          <li className="nav-item">
            <Link
              to="/"
              className={`nav-link ${isActive('/') && location.pathname === '/' ? 'active' : ''}`}
              onClick={closeMenu}
            >
              🏠 Home
            </Link>
          </li>

          {/* Aprendizaje */}
          <li className="nav-item dropdown">
            <button className="nav-link dropdown-toggle">
              📚 Aprendizaje
            </button>
            <div className="dropdown-menu">
              <Link to="/lessons" className="dropdown-item" onClick={closeMenu}>
                📖 Lecciones
              </Link>
              <Link to="/categories" className="dropdown-item" onClick={closeMenu}>
                📂 Categorías
              </Link>
              <Link to="/flashcards" className="dropdown-item" onClick={closeMenu}>
                📇 Flashcards
              </Link>
              <Link to="/srs" className="dropdown-item" onClick={closeMenu}>
                🔄 Repetición Espaciada
              </Link>
            </div>
          </li>

          {/* Retos */}
          <li className="nav-item dropdown">
            <button className="nav-link dropdown-toggle">
              🎮 Retos
            </button>
            <div className="dropdown-menu">
              <Link to="/reto/formar-palabras" className="dropdown-item" onClick={closeMenu}>
                🔤 Formar Palabras
              </Link>
              <Link to="/reto/oraciones" className="dropdown-item" onClick={closeMenu}>
                📝 Construir Oraciones
              </Link>
            </div>
          </li>

          {/* Estadísticas y Perfil */}
          <li className="nav-item dropdown">
            <button className="nav-link dropdown-toggle">
              👤 Mi Cuenta
            </button>
            <div className="dropdown-menu">
              <Link to="/progress" className="dropdown-item" onClick={closeMenu}>
                📈 Mi Progreso
              </Link>
              <Link to="/profile" className="dropdown-item" onClick={closeMenu}>
                ⚙️ Mi Perfil
              </Link>
              <a href="#logout" className="dropdown-item" onClick={closeMenu}>
                🚪 Cerrar Sesión
              </a>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;