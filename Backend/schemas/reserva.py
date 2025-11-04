from pydantic import BaseModel
from datetime import date

class ReservaCreate(BaseModel):
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date

class ReservaIn(BaseModel):
    usuario_id: int
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date

class Reserva(BaseModel):
    id: int
    usuario_id: int
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date
    
    # --- ARREGLO AQUÍ ---
    # Habilitamos la creación del modelo desde atributos de objeto
    class Config:
        from_attributes = True

