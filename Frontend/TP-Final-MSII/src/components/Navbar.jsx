import { useContext } from 'react';
import { AuthContext } from '../auth/AuthContext';
import { Link } from 'react-router-dom'; 

// --- Estilos el Navbar ---
const navStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  padding: '10px 20px',
  backgroundColor: '#f0f0f0',
  borderBottom: '1px solid #ccc'
};

const navLinks = {
  display: 'flex',
  gap: '20px' // Espacio entre links
};

const userInfo = {
  display: 'flex',
  alignItems: 'center',
  gap: '15px' // Espacio entre "Hola" y el boton
};

// --- Componente de la Barra de Navegacion ---
function Navbar() {

  const { user, logout, getReportePDF} = useContext(AuthContext);

  // --- Manejador para el boton de Reportes ---
  const handleReportClick = (e) => {
    e.preventDefault(); 
    getReportePDF();
  };

  // Renderiza el Navbar
  return (
    <nav style={navStyle}>
      <div style={navLinks}>
        <Link to="/dashboard">Habitaciones</Link>
        <Link to="/mis-reservas">Mis Reservas</Link>
        <a 
          href="#" 
          onClick={handleReportClick}
          role="button" 
          style={{ padding: 0, margin: 0, background: 'none', border: 'none', color: 'var(--pico-primary)' }}
        >
          Reportes
        </a>

      </div>

      <div style={userInfo}>
        <span>Hola, {user.username}</span>
        <button onClick={logout}>Cerrar Sesion</button>
      </div>
    </nav>
  );
}

export default Navbar;