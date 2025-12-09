import React, { useState, useEffect } from 'react';
import { learningAPI } from '../services/api';
import './ProfilePage.css';

interface Usuario {
  id: number;
  name: string;
  email: string;
  level: string;
  joinDate: string;
  totalXP: number;
  badges: string[];
  estadisticas: {
    palabras_aprendidas: number;
    retos_completados: number;
    racha: number;
  };
}

const ProfilePage: React.FC = () => {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await learningAPI.getUsers();
        setUsuario(response.data.data);
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) return <div className="loading">Cargando perfil...</div>;

  if (!usuario) return <div className="error">Error al cargar el perfil</div>;

  const daysLearning = Math.floor(
    (new Date().getTime() - new Date(usuario.joinDate).getTime()) / (1000 * 60 * 60 * 24)
  );

  const getLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'principiante':
        return '#28a745';
      case 'intermedio':
        return '#ffc107';
      case 'avanzado':
        return '#dc3545';
      default:
        return '#667eea';
    }
  };

  const getLevelEmoji = (level: string) => {
    switch (level.toLowerCase()) {
      case 'principiante':
        return '🌱';
      case 'intermedio':
        return '🌿';
      case 'avanzado':
        return '🌳';
      default:
        return '📚';
    }
  };

  return (
    <div className="profile-page">
      <div className="profile-container">
        {/* Encabezado del Perfil */}
        <div className="profile-header">
          <div className="avatar">
            <span className="avatar-letter">{usuario.name.charAt(0).toUpperCase()}</span>
          </div>
          <div className="header-info">
            <h1>{usuario.name}</h1>
            <p className="email">{usuario.email}</p>
            <div className="level-badge" style={{ borderColor: getLevelColor(usuario.level) }}>
              <span>{getLevelEmoji(usuario.level)} {usuario.level}</span>
            </div>
          </div>
          {!editMode && (
            <button 
              className="btn btn-edit"
              onClick={() => setEditMode(true)}
            >
              ✏️ Editar Perfil
            </button>
          )}
        </div>

        {/* Tarjeta Principal */}
        <div className="profile-card">
          <div className="card-section">
            <h2>Información General</h2>
            <div className="info-grid">
              <div className="info-item">
                <span className="label">Miembro desde</span>
                <span className="value">{new Date(usuario.joinDate).toLocaleDateString('es-ES')}</span>
              </div>
              <div className="info-item">
                <span className="label">Días aprendiendo</span>
                <span className="value">{daysLearning} días</span>
              </div>
              <div className="info-item">
                <span className="label">XP Total</span>
                <span className="value xp">{usuario.totalXP.toLocaleString()}</span>
              </div>
              <div className="info-item">
                <span className="label">Racha Actual</span>
                <span className="value streak">🔥 {usuario.estadisticas.racha} días</span>
              </div>
            </div>
          </div>

          {/* Estadísticas */}
          <div className="card-section">
            <h2>Mis Estadísticas</h2>
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-icon">📖</div>
                <span className="stat-label">Palabras Aprendidas</span>
                <span className="stat-value">{usuario.estadisticas.palabras_aprendidas}</span>
              </div>
              <div className="stat-item">
                <div className="stat-icon">🎯</div>
                <span className="stat-label">Retos Completados</span>
                <span className="stat-value">{usuario.estadisticas.retos_completados}</span>
              </div>
              <div className="stat-item">
                <div className="stat-icon">⭐</div>
                <span className="stat-label">Racha</span>
                <span className="stat-value">{usuario.estadisticas.racha} días</span>
              </div>
            </div>
          </div>

          {/* Insignias */}
          <div className="card-section">
            <h2>Mis Insignias</h2>
            <div className="badges-grid">
              {usuario.badges.map((badge, idx) => (
                <div key={idx} className="badge-item">
                  <div className="badge-icon">🏆</div>
                  <span>{badge}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sección de Metas */}
        <div className="goals-section">
          <h2>Mis Objetivos</h2>
          <div className="goals-grid">
            <div className="goal">
              <div className="goal-header">
                <h3>📚 Aprender 500 Palabras</h3>
                <span className="progress-text">
                  {usuario.estadisticas.palabras_aprendidas}/500
                </span>
              </div>
              <div className="goal-progress">
                <div 
                  className="goal-progress-fill"
                  style={{
                    width: `${(usuario.estadisticas.palabras_aprendidas / 500) * 100}%`
                  }}
                ></div>
              </div>
            </div>

            <div className="goal">
              <div className="goal-header">
                <h3>🎯 Completar 100 Retos</h3>
                <span className="progress-text">
                  {usuario.estadisticas.retos_completados}/100
                </span>
              </div>
              <div className="goal-progress">
                <div 
                  className="goal-progress-fill"
                  style={{
                    width: `${(usuario.estadisticas.retos_completados / 100) * 100}%`
                  }}
                ></div>
              </div>
            </div>

            <div className="goal">
              <div className="goal-header">
                <h3>🔥 Racha de 30 Días</h3>
                <span className="progress-text">
                  {usuario.estadisticas.racha}/30
                </span>
              </div>
              <div className="goal-progress">
                <div 
                  className="goal-progress-fill"
                  style={{
                    width: `${(usuario.estadisticas.racha / 30) * 100}%`
                  }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Consejos Personalizados */}
        <div className="tips-section">
          <h2>💡 Recomendaciones Personalizadas</h2>
          <div className="tips">
            {usuario.estadisticas.palabras_aprendidas < 100 && (
              <div className="tip">
                <p>¡Sigue aprendiendo palabras! Todavía tienes mucho camino por recorrer. 📚</p>
              </div>
            )}
            {usuario.estadisticas.racha >= 7 && usuario.estadisticas.racha < 30 && (
              <div className="tip">
                <p>¡Vas muy bien con tu racha! Sigue estudiando para llegar a 30 días. 🔥</p>
              </div>
            )}
            {usuario.estadisticas.racha >= 30 && (
              <div className="tip">
                <p>¡Increíble! ¡Has alcanzado una racha de 30 días! Mantén el momentum. 🌟</p>
              </div>
            )}
            {usuario.estadisticas.retos_completados < 20 && (
              <div className="tip">
                <p>Intenta completar más retos para mejorar tus habilidades. 🎯</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;