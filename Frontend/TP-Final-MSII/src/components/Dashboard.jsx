import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar.jsx";

// --- Componente Dashboard (Pagina Principal) ---
// Muestra las habitaciones disponibles y permite crear reservas
function Dashboard() {
  
  const { authFetch, createReserva } = useContext(AuthContext);
  const navigate = useNavigate();

  const [habitaciones, setHabitaciones] = useState([]); 
  const [error, setError] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");

  // --- Carga las habitaciones al iniciar ---
  useEffect(() => {
    // Funcion interna para poder usar async/await
    const fetchHabitaciones = async () => {
      try {
        //llamar al backend con el token
        const res = await authFetch("/habitaciones/");
        if (!res.ok) {
          throw new Error("Error al cargar habitaciones o token expirado");
        }
        const data = await res.json();
        // Guarda la lista de habitaciones en el estado
        setHabitaciones(data);
      } catch (err) {
        setError(err.message);
      }
    };


    fetchHabitaciones();
  }, [authFetch]);

  // --- Manejador para crear una reserva ---
  const handleReservar = async (habitacionId) => {
    // no permite fechas vacias
    if (!fechaInicio || !fechaFin) {
      alert("Por favor, selecciona una fecha de inicio y fin.");
      return;
    }

    // Arma el objeto para enviar al backend
    const reservaData = {
      habitacion_id: habitacionId,
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
    };

    const result = await createReserva(reservaData);
    
    // Si el backend devuelve un error
    if (result.error) {
      alert(`Error: ${result.error}`);
    } else {
      // Si todo sale bien, avisa y redirige
      alert(`¡Reserva creada!`);
      navigate("/mis-reservas");
    }
  };

  // --- Manejo de renderizado con errores ---
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
    <>
      <Navbar />
      <main className="container">
        {/* Envolvemos el titulo y seleccion de fecha en una card */}
        <article>
          <h1 style={{ marginTop: "20px" }}>Habitaciones Disponibles</h1>
          <p>Bienvenido. Selecciona tus fechas y reserva una habitación.</p>
          
          {/* Grilla para los inputs de fecha */}
          <div className="grid">
            <label>
              Desde:
              <input
                type="date"
                value={fechaInicio}
                onChange={(e) => setFechaInicio(e.target.value)}
              />
            </label>
            <label>
              Hasta:
              <input
                type="date"
                value={fechaFin}
                onChange={(e) => setFechaFin(e.target.value)}
              />
            </label>
          </div>
        </article>
        
        <hr />

        {/* Grilla para las cards de habitaciones */}
        <div className="grid">
          {habitaciones.length === 0 ? (
            <p>Cargando habitaciones...</p>
          ) : (
            // Mapea la lista de habitaciones y crea una card por cada una
            habitaciones.map((hab) => (
              <article key={hab.id}>
                {/* Muestra el nombre del tipo de habitacion (del JOIN) */}
                <h4>{hab.tipo_nombre}</h4>

                <p>
                  <strong>Capacidad:</strong> {hab.capacidad} persona(s)
                  <br />
                  <strong>Precio:</strong> ${hab.precio} / noche
                </p>

                <footer>
                  <button onClick={() => handleReservar(hab.id)}>
                    Reservar
                  </button>
                </footer>
              </article>
            ))
          )}
        </div>
      </main>
    </>
  );
}

export default Dashboard;