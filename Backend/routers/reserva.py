from fastapi import APIRouter, Depends
from schemas.reserva import ReservaCreate, Reserva # Importamos los schemas correctos
from schemas.auth import Usuario # Importamos el schema de Usuario
from services.reserva import create_reserva, get_reservas_by_usuario # Importamos las funciones renombradas
from services.auth import get_current_user
from typing import List # Para el response_model

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# --- ENDPOINT MODIFICADO ---
@router.get("/", response_model=List[Reserva]) # Añadido response_model
async def listar_reservas_del_usuario(user: Usuario = Depends(get_current_user)):
    # Pasamos el ID del usuario (del token) al servicio
    return await get_reservas_by_usuario(user.id)

# --- ENDPOINT MODIFICADO ---
@router.post("/", response_model=Reserva) # Añadido response_model
async def agregar_reserva(
    reserva: ReservaCreate, # Usamos el schema seguro (sin usuario_id)
    user: Usuario = Depends(get_current_user)
):
    # Pasamos el ID del usuario (del token) al servicio
    return await create_reserva(reserva, user.id)
