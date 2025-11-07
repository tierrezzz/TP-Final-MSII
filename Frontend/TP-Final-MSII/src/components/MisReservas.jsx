// src/components/MisReservas.jsx

import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import Navbar from "./Navbar";

function MisReservas() {
  const [reservas, setReservas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { authFetch, deleteReserva} = useContext(AuthContext); // Traemos el fetcher

  useEffect(() => {
    const fetchReservas = async () => {
      try {
        // Este endpoint (GET /reservas) ya esta protegido y
        // solo devuelve las reservas del usuario (gracias al token)
        const res = await authFetch("/reservas");

        if (!res.ok) {
          throw new Error(
            "Error al cargar tus reservas o no tiene reservas realizadas"
          );
        }

        const data = await res.json();
        setReservas(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false); // Pase lo que pase, dejamos de cargar
      }
    };

    fetchReservas();
  }, [authFetch]); // La dependencia es authFetch


  // Funcion para cancelar una reserva
  const handleCancel = async (reservaId) => {
    if (!window.confirm("¿Estas seguro de que quieres cancelar esta reserva?")) {
      return; // Si dice "No", no hacemos nada
    }

    const result = await deleteReserva(reservaId);

    if (result.error) {
      alert(`Error al cancelar: ${result.error}`);
    } else {
      alert(result.mensaje); // Muestra "Reserva cancelada exitosamente"
      
      // Actualizamos la lista de reservas en pantalla SIN recargar.
      // Creamos una nueva lista filtrando la reserva que acabamos de borrar.
      setReservas(prevReservas => 
        prevReservas.filter(reserva => reserva.id !== reservaId)
      );
    }
  };

  // --- Renderizado ---

  if (loading) {
    return (
      <>
        <Navbar />
        <div style={{ padding: "20px" }}>
          <p>Cargando tus reservas...</p>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbar />
        <div style={{ padding: "20px" }}>
          <p style={{ color: "red" }}>{error}</p>
        </div>
      </>
    );
  }

  return (
    <div>
      <Navbar />
      <main className="container">
        <h1 style={{ marginTop: "20px" }}>Mis Reservas</h1>

        {loading && <p>Cargando tus reservas...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {!loading && !error && (
          <>
            {reservas.length === 0 ? (
              <p>Todavía no has hecho ninguna reserva.</p>
            ) : (
              // Usamos la misma grilla que en el Dashboard
              <div className="grid">
                {reservas.map((reserva) => (
                  // Cada reserva es una "card"
                  <article key={reserva.id}>
                    {/* ¡Usamos los nuevos datos del JOIN! */}
                    <h4>{reserva.tipo_nombre}</h4>

                    <p>
                      <strong>Desde:</strong> {reserva.fecha_inicio}
                      <br />
                      <strong>Hasta:</strong> {reserva.fecha_fin}
                      <br />
                      <strong>Precio:</strong> ${reserva.precio} / noche
                    </p>

                    <footer>
                      <button
                        className="secondary outline"
                        style={{
                          color: "var(--pico-color-red-500)",
                          borderColor: "var(--pico-color-red-500)",
                        }}
                        onClick={() => handleCancel(reserva.id)}
                      >
                        Cancelar
                      </button>
                    </footer>
                  </article>
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default MisReservas;
