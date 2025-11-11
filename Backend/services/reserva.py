from config.database import db
from schemas.reserva import ReservaCreate, Reserva
from typing import List
from fastapi import HTTPException, status
from datetime import date

# --- Funcion para OBTENER las reservas de un usuario ---
async def get_reservas_by_usuario(usuario_id: int) -> List[Reserva]:
    query = """
        SELECT 
            r.id, r.usuario_id, r.habitacion_id, r.fecha_inicio, r.fecha_fin,
            h.precio, t.nombre AS tipo_nombre
        FROM 
            reservas r
        JOIN habitaciones h ON r.habitacion_id = h.id
        JOIN tipos_habitacion t ON h.tipo_id = t.id
        WHERE r.usuario_id = :usuario_id
        ORDER BY r.fecha_inicio DESC
    """
    reservas_db = await db.fetch_all(query, values={"usuario_id": usuario_id})
    
    # Mapea los resultados de la DB al schema 'Reserva'
    # Usa **dict() para convertir el 'Record' de la DB
    return [Reserva(**dict(res)) for res in reservas_db]

# --- Funcion para OBTENER una reserva por ID ---
async def get_reserva_by_id(reserva_id: int):
    query = "SELECT * FROM reservas WHERE id = :id"
    reserva = await db.fetch_one(query, values={"id": reserva_id})
    if not reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    return reserva


# --- Funcion para CREAR una reserva ---
async def create_reserva(reserva: ReservaCreate, usuario_id: int) -> Reserva:
    
    # Comprueba si la fecha de fin es ANTES o IGUAL
    if reserva.fecha_fin <= reserva.fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )
    
    # Comprueba si la reserva es para hoy o el futuro
    if reserva.fecha_inicio < date.today():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="La fecha de inicio no puede ser en el pasado"
        )

    query = """
        INSERT INTO reservas (usuario_id, habitacion_id, fecha_inicio, fecha_fin)
        VALUES (:usuario_id, :habitacion_id, :fecha_inicio, :fecha_fin)
    """

    values = {**reserva.model_dump(), "usuario_id": usuario_id}
    
    # Ejecuta la insercion y obtiene el ID nuevo
    last_id = await db.execute(query, values)
    
    # Busca la reserva recien creada para devolverla completa
    query_select = "SELECT * FROM reservas WHERE id = :id"
    created_reserva = await db.fetch_one(query_select, values={"id": last_id})
    
    #Convierte el resultado de la DB a un schema 'Reserva' y lo devuelve
    return Reserva(**dict(created_reserva))

# --- Funcion para MODIFICAR una reserva ---
# Sin uso, para futura funciones
async def update_reserva(reserva_id: int, usuario_id: int, reserva_data: ReservaCreate) -> Reserva:
  
    query_check = "SELECT * FROM reservas WHERE id = :reserva_id"
    reserva_db = await db.fetch_one(query_check, values={"reserva_id": reserva_id})

    if not reserva_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

    if reserva_db["usuario_id"] != usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para modificar esta reserva")

    query_update = """
        UPDATE reservas
        SET habitacion_id = :habitacion_id, 
            fecha_inicio = :fecha_inicio, 
            fecha_fin = :fecha_fin
        WHERE id = :reserva_id
    """
    values = {**reserva_data.model_dump(), "reserva_id": reserva_id}
    await db.execute(query_update, values)


    updated_data = {
        **reserva_data.model_dump(),
        "id": reserva_id,
        "usuario_id": usuario_id
    }
    return Reserva(**updated_data)

# Funcion para ELIMINAR una reserva (Cancelar)
async def delete_reserva(reserva_id: int, usuario_id: int):
    
    reserva = await get_reserva_by_id(reserva_id) 
    
    # Compara el dueño de la reserva con el que la quiere borrar (del token)
    if reserva["usuario_id"] != usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para borrar esta reserva")

    query = "DELETE FROM reservas WHERE id = :id"
    await db.execute(query, values={"id": reserva_id})
   
    return {"mensaje": "Reserva cancelada exitosamente"}