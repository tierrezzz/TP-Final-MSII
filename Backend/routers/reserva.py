from fastapi import APIRouter, Depends
from schemas.reserva import ReservaCreate, Reserva 
from schemas.auth import Usuario 
from services.reserva import create_reserva, get_reservas_by_usuario, delete_reserva
from services.auth import get_current_user
from typing import List

# Creamos el router. /reservas
router = APIRouter(prefix="/reservas", tags=["Reservas"])

# --- Endpoint para OBTENER las reservas del usuario ---
@router.get("/", response_model=List[Reserva]) 
async def listar_reservas_del_usuario(user: Usuario = Depends(get_current_user)):

    return await get_reservas_by_usuario(user.id)

# --- Endpoint para ver detalle de una reserva ---
@router.get("/{reserva_id}", response_model=Reserva)
async def ver_reserva_por_id(
    reserva_id: int,
    user: Usuario = Depends(get_current_user)
):
    return await get_reserva_by_id(reserva_id=reserva_id, usuario_id=user.id)

# --- Endpoint para CREAR una reserva ---
@router.post("/", response_model=Reserva) 
async def agregar_reserva(
    reserva: ReservaCreate, 
    user: Usuario = Depends(get_current_user)
):
    return await create_reserva(reserva, user.id)

# --- Endpoint para modificar una reserva ---
@router.put("/{reserva_id}", response_model=Reserva)
async def modificar_reserva(
    reserva_id: int,
    reserva_data: ReservaCreate, 
    user: Usuario = Depends(get_current_user)
):

    return await update_reserva(
        reserva_id=reserva_id, 
        usuario_id=user.id, 
        reserva_data=reserva_data
    )

# --- Endpoint para eliminar una reserva ---
@router.delete("/{reserva_id}")
async def cancelar_reserva(
    reserva_id: int, 
    user: Usuario = Depends(get_current_user) 
):
    return await delete_reserva(reserva_id=reserva_id, usuario_id=user.id)