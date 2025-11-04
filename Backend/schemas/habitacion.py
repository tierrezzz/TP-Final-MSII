from pydantic import BaseModel

class HabitacionIn(BaseModel):
    tipo_id: int
    capacidad: int
    precio: float

class Habitacion(BaseModel):
    id: int
    tipo_id: int
    capacidad: int
    precio: float