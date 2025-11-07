import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";

function Login() {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await login(username, password);
    if (result.username) navigate("/dashboard");
    else setError(result.error);
  };

  return (
    <main className="container"> 
      <article>
        <h1 className="text-center">Acceso al sistema</h1>
        <form onSubmit={handleSubmit}>
          {/* Pico es "classless". Solo pones el label y el input.
            El 'placeholder' es necesario para que el label "flote"
          */}
          <label htmlFor="username">Nombre de usuario</label>
          <input
            type="text"
            name="username"
            id="username"
            value={username}
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
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Tu contraseña"
            required
          />
          
          <button type="submit">Iniciar sesión</button>
        </form>
        {error && <div role="alert">{error}</div>}
        
        <footer className="text-center">
          <Link to="/register">¿No tienes cuenta? Regístrate</Link>
        </footer>
      </article>
    </main>
  );
}

export default Login;
