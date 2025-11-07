from pydantic import BaseModel

# --- Schema para CREAR una Habitacion ---
class HabitacionIn(BaseModel):
    tipo_id: int
    capacidad: int
    precio: float

# --- Schema para MOSTRAR una Habitacion ---
class Habitacion(BaseModel):
    id: int
    tipo_id: int
    capacidad: int
    precio: float