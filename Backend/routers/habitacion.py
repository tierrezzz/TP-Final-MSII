from fastapi import APIRouter, Depends
from schemas.habitacion import HabitacionIn, Habitacion
from services.habitacion import get_all_habitaciones, create_habitacion, get_habitacion_by_id,  update_habitacion, delete_habitacion
from services.auth import get_current_user
from schemas.auth import Usuario

# Creamos el router. /habitaciones
router = APIRouter(prefix="/habitaciones", tags=["Habitaciones"])

# --- Endpoint para obtener habitaciones ---
@router.get("/")
async def listar_habitaciones():
    return await get_all_habitaciones()

# --- Endpoint para obtener habitaciones por ID 
@router.get("/{habitacion_id}", response_model=Habitacion)
async def ver_habitacion_por_id(habitacion_id: int):

    return await get_habitacion_by_id(habitacion_id=habitacion_id)

# --- Endpoint para Crear habitaciones ---
@router.post("/")
async def agregar_habitacion(habitacion: HabitacionIn):
    return await create_habitacion(habitacion)

# --- Endpoint para Modificar habitaciones ---
@router.put("/{habitacion_id}")
async def modificar_habitacion(
    habitacion_id: int,
    habitacion_data: HabitacionIn,
    user: Usuario = Depends(get_current_user) # Protegido
):
    # Llama al servicio que modifica
    return await update_habitacion(
        habitacion_id=habitacion_id, 
        habitacion_data=habitacion_data
    )

# --- Endpoint para Eliminar habitaciones ---
@router.delete("/{habitacion_id}")
async def eliminar_habitacion(
    habitacion_id: int,
    user: Usuario = Depends(get_current_user) # Protegido
):
    # Llama al servicio que elimina
    return await delete_habitacion(habitacion_id=habitacion_id)