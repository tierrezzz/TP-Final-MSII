import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";

// --- Componente de la pagina de Registro ---
// Define el formulario y la logica para crear una cuenta nueva
function Register() {
  
  const { register } = useContext(AuthContext);

  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  
  // --- Manejador del envio del formulario ---
  // Se llama cuando el usuario aprieta "Registrarse"
  const handleSubmit = async (e) => {
    e.preventDefault(); // Evita que la pagina recargue
    setError(""); // Limpia errores viejos

    // Llama a la funcion 'register' del contexto.
    // Esta funcion tambien hace el auto-login.
    const result = await register(username, password);

    if (result.username) {
      // Si el registro/login fue exitoso, redirige al dashboard
      navigate("/dashboard");
    } else {
      // Si no, muestra el error (ej: "Usuario ya en uso")
      setError(result.error);
    }
  };

  // Renderiza el formulario
  return (
    <main className="container">
    <article>
      <h1 className="text-center">Registro de Usuario</h1>
      <form onSubmit={handleSubmit}>
        
        <label htmlFor="username">Nombre de usuario</label>
        <input
          type="text"
          name="username"
          id="username"
          value={username}
          // Actualiza el estado 'username' cada vez que el usuario escribe
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Elige un nombre de usuario"
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
          placeholder="Elige una contraseña"
          required
        />
        <button type="submit">Registrarse</button>
      </form>
      
      {/* Muestra el error solo si existe */}
      {error && <div role="alert">{error}</div>}

      <footer className="text-center">
        <Link to="/login">¿Ya tienes cuenta? Inicia sesion</Link>
      </footer>
    </article>
  </main>
);
}

export default Register;