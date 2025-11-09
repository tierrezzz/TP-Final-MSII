import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";

// --- Componente de la pagina de Login ---
// Define el formulario y la logica para iniciar sesion
function Login() {
  
  const { login } = useContext(AuthContext);
  
  const navigate = useNavigate();
  
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // --- Manejador del envio del formulario ---
  // Se llama cuando el usuario aprieta "Iniciar sesion"
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const result = await login(username, password);
    
    // Si el login fue exitoso (devuelve un usuario), redirige al dashboard
    if (result.username) {
      navigate("/dashboard");
    } else {
      // Si no, muestra el error que devolvio el contexto
      setError(result.error);
    }
  };

  // Renderiza el formulario
  return (
    <main className="container"> 
      <article>
        <h1 className="text-center">Acceso al sistema</h1>
        <form onSubmit={handleSubmit}>
          
          <label htmlFor="username">Nombre de usuario</label>
          <input
            type="text"
            name="username"
            id="username"
            value={username}
            // Actualiza el estado 'username' cada vez que el usuario escribe
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Tu nombre de usuario"
            required
          />

          <label htmlFor="password">Contraseña</label>
          <input
            type="password"
            name="password"
            id="password"
            value={password}
            // Actualiza el estado 'password' cada vez que el usuario escribe
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Tu contraseña"
            required
          />
          
          <button type="submit">Iniciar sesión</button>
        </form>
        
        {/* Muestra el error solo si existe */}
        {error && <div role="alert">{error}</div>}
        
        <footer className="text-center">
          <Link to="/register">¿No tienes cuenta? Regístrate</Link>
        </footer>
      </article>
    </main>
  );
}

export default Login;