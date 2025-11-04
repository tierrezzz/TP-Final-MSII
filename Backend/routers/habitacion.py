from fastapi import APIRouter
from schemas.habitacion import HabitacionIn
from services.habitacion import get_all_habitaciones, create_habitacion

router = APIRouter(prefix="/habitaciones", tags=["Habitaciones"])

@router.get("/")
async def listar_habitaciones():
    return await get_all_habitaciones()

@router.post("/")
async def agregar_habitacion(habitacion: HabitacionIn):
    return await create_habitacion(habitacion)