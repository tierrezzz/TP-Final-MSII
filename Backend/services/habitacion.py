from config.database import db
from schemas.habitacion import HabitacionIn

# --- Funcion para OBTENER TODAS las habitaciones ---
async def get_all_habitaciones():

    query = """
        SELECT 
            h.id, 
            h.capacidad, 
            h.precio, 
            h.tipo_id,
            t.nombre AS tipo_nombre
        FROM 
            habitaciones h
        JOIN 
            tipos_habitacion t ON h.tipo_id = t.id
    """
    

    return await db.fetch_all(query)

# --- Funcion para OBTENER una habitacion por ID ---
async def get_habitacion_by_id(habitacion_id: int):
    query = "SELECT * FROM habitaciones WHERE id = :id"
    habitacion = await db.fetch_one(query, values={"id": habitacion_id})
    if not habitacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habitacion no encontrada")
    return habitacion # Devuelve el 'Record' de la DB

# --- Funcion para CREAR una habitacion ---
# No esta en uso pero sirve para futuras funcionalidades
async def create_habitacion(habitacion: HabitacionIn):
    query = """
        INSERT INTO habitaciones (tipo_id, capacidad, precio)
        VALUES (:tipo_id, :capacidad, :precio)
    """
    # Convierte el objeto Pydantic (habitacion) a un diccionario
    values = habitacion.dict()
    
    # Ejecuta la consulta y obtiene el ID nuevo
    last_id = await db.execute(query, values)
    
    # Devuelve el objeto creado + el nuevo ID
    return {**values, "id": last_id}
    


# --- Funcion para MODIFICAR una habitacion ---
async def update_habitacion(habitacion_id: int, habitacion_data: HabitacionIn):
    # Verifica si existe primero
    await get_habitacion_by_id(habitacion_id) # Si no existe, esto da 404

    query = """
        UPDATE habitaciones
        SET tipo_id = :tipo_id, 
            capacidad = :capacidad, 
            precio = :precio
        WHERE id = :id
    """
    values = {**habitacion_data.model_dump(), "id": habitacion_id}
    await db.execute(query, values)
    
    # Devuelve el objeto actualizado
    return {**habitacion_data.model_dump(), "id": habitacion_id}

# --- Funcion para ELIMINAR una habitacion ---
async def delete_habitacion(habitacion_id: int):
    # Verifica si existe primero
    await get_habitacion_by_id(habitacion_id) # Si no existe, esto da 404

    query = "DELETE FROM habitaciones WHERE id = :id"
    await db.execute(query, values={"id": habitacion_id})
    
    return {"mensaje": "Habitacion eliminada exitosamente"}
