import { useContext } from 'react';
import { AuthContext } from '../auth/AuthContext';
import { Link } from 'react-router-dom'; // Para los links de navegacion

// Un estilo basico para el Navbar (CSS puro y simple)
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
  gap: '20px'
};

const userInfo = {
  display: 'flex',
  alignItems: 'center',
  gap: '15px'
};

function Navbar() {
  // 1. Trae el 'user' y 'logout' del cerebro
  const { user, logout, getReportePDF} = useContext(AuthContext);

const handleReportClick = (e) => {
  e.preventDefault(); // Evita que el link intente navegar
  getReportePDF();    // Llama a la funcion del authprovider
};


  return (
    <nav style={navStyle}>
      <div style={navLinks}>
        <Link to="/dashboard">Habitaciones</Link>
        <Link to="/mis-reservas">Mis Reservas</Link>
        <a 
          href="#" 
          onClick={handleReportClick}
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