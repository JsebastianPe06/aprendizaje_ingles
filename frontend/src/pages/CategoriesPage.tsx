import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { learningAPI } from '../services/api';
import './CategoriesPage.css';

interface Categoria {
  nombre: string;
  palabras: string[];
  cantidad: number;
}

const CategoriesPage: React.FC = () => {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [categoriasSeleccionadas, setCategoriasSeleccionadas] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await learningAPI.getCategories();
        setCategorias(response.data.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  const toggleCategoria = (nombre: string) => {
    const nuevas = new Set(categoriasSeleccionadas);
    if (nuevas.has(nombre)) {
      nuevas.delete(nombre);
    } else {
      nuevas.add(nombre);
    }
    setCategoriasSeleccionadas(nuevas);
  };

  const handleEstudiarCategoria = (nombre: string) => {
    navigate(`/categoria/${nombre}/estudio`);
  };

  const handleEstudiarSeleccionadas = () => {
    if (categoriasSeleccionadas.size > 0) {
      const categoriasStr = Array.from(categoriasSeleccionadas).join(',');
      navigate(`/categorias/estudio?categorias=${categoriasStr}`);
    }
  };

  if (loading) return <div className="loading">Cargando categorías...</div>;

  const totalPalabras = categorias.reduce((sum, cat) => sum + cat.cantidad, 0);

  return (
    <div className="categories-page">
      <header className="categorias-header">
        <h1>📚 Categorías de Vocabulario</h1>
        <p>Aprende vocabulario organizado por categorías</p>
      </header>

      <div className="stats-summary">
        <div className="stat">
          <span className="stat-label">Total de Categorías</span>
          <span className="stat-value">{categorias.length}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Total de Palabras</span>
          <span className="stat-value">{totalPalabras}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Seleccionadas</span>
          <span className="stat-value">{categoriasSeleccionadas.size}</span>
        </div>
      </div>

      <div className="categorias-grid-container">
        <h2>Selecciona categorías para estudiar</h2>
        <div className="categorias-grid">
          {categorias.map((categoria) => (
            <div 
              key={categoria.nombre}
              className={`categoria-card ${categoriasSeleccionadas.has(categoria.nombre) ? 'selected' : ''}`}
              onClick={() => toggleCategoria(categoria.nombre)}
            >
              <div className="categoria-header">
                <h3>{categoria.nombre}</h3>
                {categoriasSeleccionadas.has(categoria.nombre) && (
                  <span className="check-mark">✓</span>
                )}
              </div>
              <p className="palabra-count">{categoria.cantidad} palabras</p>
              <div className="palabras-preview">
                {categoria.palabras.slice(0, 3).map((palabra, idx) => (
                  <span key={idx} className="palabra-tag">{palabra}</span>
                ))}
                {categoria.palabras.length > 3 && (
                  <span className="palabra-tag">+{categoria.palabras.length - 3}</span>
                )}
              </div>
              <button 
                className="btn btn-study"
                onClick={(e) => {
                  e.stopPropagation();
                  handleEstudiarCategoria(categoria.nombre);
                }}
              >
                Estudiar Ahora
              </button>
            </div>
          ))}
        </div>
      </div>

      {categoriasSeleccionadas.size > 0 && (
        <div className="action-panel">
          <div className="seleccionadas-list">
            <h4>Categorías seleccionadas:</h4>
            <div className="tags">
              {Array.from(categoriasSeleccionadas).map((cat) => (
                <span key={cat} className="tag">
                  {cat}
                  <button onClick={() => toggleCategoria(cat)}>×</button>
                </span>
              ))}
            </div>
          </div>
          <button 
            className="btn btn-primary btn-large"
            onClick={handleEstudiarSeleccionadas}
          >
            Estudiar {categoriasSeleccionadas.size} Categoría{categoriasSeleccionadas.size !== 1 ? 's' : ''}
          </button>
        </div>
      )}
    </div>
  );
};

export default CategoriesPage;