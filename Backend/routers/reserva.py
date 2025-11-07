from fastapi import APIRouter, Depends
from schemas.reserva import ReservaCreate, Reserva 
from schemas.auth import Usuario 
from services.reserva import create_reserva, get_reservas_by_usuario, delete_reserva
from services.auth import get_current_user
from typing import List

# Creamos el router. /reservas
router = APIRouter(prefix="/reservas", tags=["Reservas"])

# --- Endpoint para OBTENER las reservas del usuario ---
@router.get("/", response_model=List[Reserva]) # Define que la respuesta es una lista
async def listar_reservas_del_usuario(user: Usuario = Depends(get_current_user)): # Esta protegida por Depends(get_current_user)
    # Llama al servicio y le pasa el ID del usuario (obtenido del token)
    # Asi solo trae las reservas de ESE usuario
    return await get_reservas_by_usuario(user.id)

# --- Endpoint para ver detalle de una reserva ---
@router.get("/{reserva_id}", response_model=Reserva)
async def ver_reserva_por_id(
    reserva_id: int,
    user: Usuario = Depends(get_current_user)
):
    # Llama al servicio que busca UNA reserva y verifica al dueño
    return await get_reserva_by_id(reserva_id=reserva_id, usuario_id=user.id)

# --- Endpoint para CREAR una reserva ---
@router.post("/", response_model=Reserva) # Define que la respuesta es una sola reserva
async def agregar_reserva(
    # Recibe los datos de la reserva (fechas, habitacion) desde el body
    reserva: ReservaCreate, 
    # Protege la ruta. Obtiene el usuario del token.
    user: Usuario = Depends(get_current_user)
):
    # Llama al servicio para crear la reserva
    # Le pasa los datos de la reserva (reserva)
    # Y le pasa el ID del usuario (user.id) del token
    # Esto asegura que el 'dueño' de la reserva sea el usuario logueado
    return await create_reserva(reserva, user.id)

# --- Endpoint para modificar una reserva ---
@router.put("/{reserva_id}", response_model=Reserva)
async def modificar_reserva(
    reserva_id: int,
    reserva_data: ReservaCreate, # Los nuevos datos vienen en el body
    user: Usuario = Depends(get_current_user)
):
    # Llama al servicio que modifica Y verifica al dueño
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
    # Llama al servicio pasandole el ID de la reserva y el ID del usuario
    return await delete_reserva(reserva_id=reserva_id, usuario_id=user.id)