import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import Navbar from "./Navbar";

// --- Componente de la pagina "Mis Reservas" ---
// Muestra las reservas del usuario y permite cancelarlas
function MisReservas() {
  const [reservas, setReservas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  const { authFetch, deleteReserva } = useContext(AuthContext); 

  // --- Carga las reservas del usuario al iniciar ---
  useEffect(() => {
    const fetchReservas = async () => {
      try {
        // Llama al backend con el token para traer SOLO las reservas de este usuario
        const res = await authFetch("/reservas/");
        
        // Si el backend falla 
        if (!res.ok) {
          throw new Error(
            "Error al cargar tus reservas o no tiene reservas realizadas"
          );
        }
        
        // Guarda las reservas en el estado
        const data = await res.json();
        setReservas(data); 

      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false); 
      }
    };

    fetchReservas();
  }, [authFetch]);

  // --- Manejador para CANCELAR una reserva ---
  const handleCancel = async (reservaId) => {

    // Pide confirmacion al usuario
    if (!window.confirm("¿Estas seguro de que quieres cancelar esta reserva?")) {
      return;
    }

    const result = await deleteReserva(reservaId);
    
    
    // Si el backend da un error, lo muestra
    if (result.error) {
      alert(`Error al cancelar: ${result.error}`);
    } else {
      alert(result.mensaje); 
      
      // --- Actualizacion instantanea ---
      // Filtra la lista de reservas en el estado para quitar la que
      // acabamos de borrar. Esto actualiza la UI sin recargar la pagina.
      setReservas(prevReservas => 
        prevReservas.filter(reserva => reserva.id !== reservaId)
      );
    }
  };

  // --- Renderizado: Muestra "Cargando..." ---
  if (loading) {
    return (
      <>
        <Navbar />
        <main className="container">
          <p>Cargando tus reservas...</p>
        </main>
      </>
    );
  }

  // --- Renderizado: Muestra un error ---
  if (error) {
    return (
      <>
        <Navbar />
        <main className="container">
          <p style={{ color: "red" }}>{error}</p>
        </main>
      </>
    );
  }

  // --- Renderizado principal ---
  return (
    <div>
      <Navbar />
      <main className="container">
        <h1 style={{ marginTop: "20px" }}>Mis Reservas</h1>

        {/* Revisa si hay reservas, si no, muestra un mensaje */}
        {reservas.length === 0 ? (
          <p>Todavía no has hecho ninguna reserva.</p>
        ) : (
          // Si hay reservas, las mapea en una grilla
          <div className="grid">
            {reservas.map((reserva) => (
              // Cada reserva es una "card" (<article>)
              <article key={reserva.id}>
                {/* Muestra el nombre del tipo (del JOIN del backend) */}
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
                    // Conecta el boton al manejador
                    onClick={() => handleCancel(reserva.id)} 
                  >
                    Cancelar
                  </button>
                </footer>
              </article>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default MisReservas;