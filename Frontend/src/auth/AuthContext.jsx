import { createContext, useState, useEffect } from "react";

// Creamos el Contexto
export const AuthContext = createContext();

// Creamos el Proveedor del Contexto
// Este 'AuthProvider' envolvera a toda nuestra aplicacion
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const API_URL = "http://localhost:8000"; 

  // Revisa si ya existe un token al cargar la app
  
    const checkAuth = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          // Hacemos una peticion a /auth/me para validar el token
          const res = await fetch(`${API_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (!res.ok) {
            // Si el token es malo (expirado, invalido), lo borramos
            throw new Error("Token invalido o expirado");
          }

          const data = await res.json();
          setUser(data); // Logueado

        } catch {
          localStorage.removeItem("token");
          setUser(null); // No logueado
        }
      }
      setLoading(false); // Terminamos de cargar
    };

useEffect(() => {
    checkAuth();
  }, []); // El [] significa que solo se ejecuta 1 vez al cargar

 // Register: crea un nuevo usuario Y HACE LOGIN
 const register = async (username, password) => {
  // Registrar el usuario 
  const registerData = {
    username: username,
    password: password,
  };

  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(registerData),
  });

  if (!res.ok) {
    // Si fallo el registro
    const errorData = await res.json();
    return { error: errorData.detail };
  }

  // Reusamos la funcion 'login' que ya sabe guardar tokens y setear usuarios.
  const loginResult = await login(username, password);
  
  // Devolvemos el resultado del login
  return loginResult;
};

// crear una reserva
const createReserva = async (reservaData) => {
  // 'reservaData' debe ser un objeto. Ej:
  // { habitacion_id: 5, fecha_inicio: "2025-11-10", fecha_fin: "2025-11-12" }

  try {
    // Usamos authFetch que ya envia el token 
    const res = await authFetch('/reservas/', {
      method: 'POST',
      body: JSON.stringify(reservaData),
    });

    // Si el backend da un error
    if (!res.ok) {
      
      const errorData = await res.json();
      let errorMessage = "Ocurrió un error desconocido.";

      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          const firstError = errorData.detail[0];
          errorMessage = `${firstError.msg} (campo: ${firstError.loc[1]})`;
        } else {
          errorMessage = errorData.detail;
        }
      }
      
      return { error: errorMessage };
    }

    // Devuelve la reserva que acabamos de crear
    const nuevaReserva = await res.json();
    return nuevaReserva;

  } catch (err) {
    console.error("Error en createReserva:", err);
    return { error: "Fallo la conexion con el servidor" };
  }
};
// Elimina una reserva
const deleteReserva = async (reservaId) => {
  try {
    // Usamos authFetch que ya envia el token
    const res = await authFetch(`/reservas/${reservaId}`, {
      method: 'DELETE',
    });

    if (!res.ok) {
      // Si el backend da un error
      const errorData = await res.json();
      return { error: errorData.detail || "Error al cancelar la reserva" };
    }

    // El backend devuelve un mensaje de exito.
    const successData = await res.json();
    return successData;

  } catch (err) {
    console.error("Error en deleteReserva:", err);
    return { error: "Fallo la conexion con el servidor" };
  }
};

// Obtenemos el reporte.
const getReportePDF = async () => {
  try {
    // Llama al endpoint
    const res = await authFetch('/reportes/ventas/mensual');
  
    // Si el backend da un error
    if (!res.ok) {
      
      throw new Error("El servidor no pudo generar el reporte");
    }

    // No usamos .json() Usamos .blob()
    const pdfBlob = await res.blob();

    // Crea una URL temporal en el navegador para ese archivo ".blob()""
    const url = URL.createObjectURL(pdfBlob);
    
    // Abre esa URL en una pestaña nueva
    window.open(url, '_blank');

    // Limpia la URL de la memoria del navegador
    setTimeout(() => URL.revokeObjectURL(url), 10000); // 10 segundos

  } catch (err) {
    console.error("Error en getReportePDF:", err);
    alert(err.message);
  }
};

  // Login: obtiene el token y guarda usuario
  const login = async (username, password) => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      body: formData, 
    });
    
    // Si fallo el login 
    if (!res.ok) {
     
      const errorData = await res.json();
      return { error: errorData.detail };
    }

    //Guarda el token
    const data = await res.json();
    localStorage.setItem("token", data.access_token);

    // Obtener los datos del usuario autenticado
    const meRes = await fetch(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${data.access_token}` },
    });

    if (!meRes.ok) {
        const errorData = await res.json();
        return { error: errorData.detail };
      }

    const me = await meRes.json();
    setUser(me); // Guarda el usuario en el estado
    return me; // Devuelve el usuario al componente Login
  };

  // Logout
  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

// Peticion autenticada con fetch
  const authFetch = async (url, options = {}) => {
    const token = localStorage.getItem("token");
    const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      };

      if (options.body) {
        headers['Content-Type'] = 'application/json';
      }
  
      const res = await fetch(`${API_URL}${url}`, { ...options, headers });
      
      if (res.status === 401) {
        logout();
        return res;
      }
      
      return res;
    };

  // Expone el 'valor' del contexto al resto de la app
  return (
    <AuthContext.Provider value={{ user, createReserva, deleteReserva, register, login, logout, authFetch, getReportePDF }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};