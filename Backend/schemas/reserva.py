from pydantic import BaseModel
from datetime import date
from pydantic import model_validator

# --- Schema para CREAR una Reserva (Cliente) ---
class ReservaCreate(BaseModel):
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date

# --- Schema para CREAR una Reserva (Interno) ---
class ReservaIn(BaseModel):
    usuario_id: int
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date

# --- Schema para MOSTRAR una Reserva ---
class Reserva(BaseModel):
    id: int
    usuario_id: int
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date
    
    # Vienen del JOIN, pero no estan en la tabla 'reservas'
    precio: float | None = None
    tipo_nombre: str | None = None
    # Habilita que el modelo se cree desde un objeto de BD
    class Config:
        from_attributes = True