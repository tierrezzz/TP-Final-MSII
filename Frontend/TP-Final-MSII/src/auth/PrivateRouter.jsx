import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../auth/AuthContext";

export default function PrivateRoute({ children }) {
  const { user, loading } = useContext(AuthContext);
  if (loading) return <p>Cargando...</p>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}
