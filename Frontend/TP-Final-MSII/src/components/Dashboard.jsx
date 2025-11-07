import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar.jsx";

function Dashboard() {
  const { authFetch, createReserva } = useContext(AuthContext);
  const navigate = useNavigate();
  const [habitaciones, setHabitaciones] = useState([]);
  const [error, setError] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");

  // (Este useEffect sigue igual, trayendo las habitaciones)
  useEffect(() => {
    const fetchHabitaciones = async () => {
      try {
        const res = await authFetch("/habitaciones");
        if (!res.ok) {
          throw new Error("Error al cargar habitaciones o token expirado");
        }
        const data = await res.json();
        setHabitaciones(data);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchHabitaciones();
  }, [authFetch]);

  const handleReservar = async (habitacionId) => {
    // Validacion simple
    if (!fechaInicio || !fechaFin) {
      alert("Por favor, selecciona una fecha de inicio y fin.");
      return;
    }

    const reservaData = {
      habitacion_id: habitacionId,
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
    };

    // Llamamos a la funcion del Context
    const result = await createReserva(reservaData);

    if (result.error) {
      // Si el backend da error (ej: "Fechas no disponibles")
      alert(`Error: ${result.error}`);
    } else {
      // ¡Exito!
      alert(`¡Reserva #${result.id} creada exitosamente!`);
      // 5. Redirigimos al usuario a "Mis Reservas"
      navigate("/mis-reservas");
    }
  };

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

  return (
    <>
      <Navbar />
      <main className="container">
        <article>
          <h1 style={{ marginTop: "20px" }}>Habitaciones Disponibles</h1>
          <p>Bienvenido. Selecciona tus fechas y reserva una habitación.</p>
        </article>
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

        <hr />

        <div className="grid">
          {habitaciones.length === 0 ? (
            <p>Cargando habitaciones...</p>
          ) : (
            habitaciones.map((hab) => (
              <article key={hab.id}>
                <h4>Habitación 
                  <br />{hab.tipo_nombre}</h4>

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
