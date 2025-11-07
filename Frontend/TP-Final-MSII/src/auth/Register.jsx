import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";

function Register() {
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  
const handleSubmit = async (e) => {
  e.preventDefault();
  setError(""); // Limpia errores viejos

  // 1. Llamamos a la funcion de registro (que ahora tambien loguea)
  const result = await register(username, password);

  if (result.username) {
    // 2. ¡Exito! El 'register' nos devolvio el usuario logueado.
    // Redirigimos directo al dashboard.
    navigate("/dashboard"); // <-- Redireccion directa
  } else {
    // 3. Fallo. Mostramos el error (ej: "Usuario ya en uso")
    setError(result.error);
  }
};

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
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Elige una contraseña"
          required
        />
        <button type="submit">Registrarse</button>
      </form>
      
      {error && <div role="alert">{error}</div>}

      <footer className="text-center">
        <Link to="/login">¿Ya tienes cuenta? Inicia sesion</Link>
      </footer>
    </article>
  </main>
);
}

export default Register;