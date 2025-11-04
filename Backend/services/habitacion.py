from config.database import db
from schemas.habitacion import HabitacionIn

async def get_all_habitaciones():
    query = "SELECT * FROM habitaciones"
    return await db.fetch_all(query)

async def create_habitacion(habitacion: HabitacionIn):
    query = """
        INSERT INTO habitaciones (tipo_id, capacidad, precio)
        VALUES (:tipo_id, :capacidad, :precio)
    """
    values = habitacion.dict()
    last_id = await db.execute(query, values)
    return {**values, "id": last_id}