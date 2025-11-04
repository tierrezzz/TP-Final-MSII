from config.database import db
from schemas.reserva import ReservaCreate, Reserva
from typing import List

# --- FUNCIÓN MODIFICADA/RENOMBRADA ---
# Ahora filtra por el ID del usuario
async def get_reservas_by_usuario(usuario_id: int) -> List[Reserva]:
    query = "SELECT * FROM reservas WHERE usuario_id = :usuario_id"
    reservas_db = await db.fetch_all(query, values={"usuario_id": usuario_id})
    
    # --- ARREGLO AQUÍ ---
    # Usamos from_attributes para convertir la data de la DB al schema
    return [Reserva.from_attributes(res) for res in reservas_db]

# --- FUNCIÓN MODIFICADA ---
# Ahora usa 'ReservaCreate' y recibe el 'usuario_id' del token
async def create_reserva(reserva: ReservaCreate, usuario_id: int) -> Reserva:
    query = """
        INSERT INTO reservas (usuario_id, habitacion_id, fecha_inicio, fecha_fin)
        VALUES (:usuario_id, :habitacion_id, :fecha_inicio, :fecha_fin)
    """
    # Combinamos los datos del schema y el usuario_id del token
    values = {**reserva.dict(), "usuario_id": usuario_id}
    
    last_id = await db.execute(query, values)
    
    # Devolvemos la reserva completa
    query_select = "SELECT * FROM reservas WHERE id = :id"
    created_reserva = await db.fetch_one(query_select, values={"id": last_id})
    
    # --- ARREGLO AQUÍ ---
    return Reserva.from_attributes(created_reserva)