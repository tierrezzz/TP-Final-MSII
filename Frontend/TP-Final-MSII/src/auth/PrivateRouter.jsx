import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";

// --- Componente Guardia de Ruta (Ruta Privada) ---
// Revisa si el usuario esta logueado.
// Si no lo esta, lo lleva a la pagina de login.
export default function PrivateRoute({ children }) {

  const { user, loading } = useContext(AuthContext);

  // Si 'loading' es true, AuthContext esta revisando el token.
  if (loading) return <p>Cargando...</p>;

  // Si no esta cargando Y no hay usuario (user es null),
  // redirige a /login.
  if (!user) return <Navigate to="/login" replace />;

  return children;
}