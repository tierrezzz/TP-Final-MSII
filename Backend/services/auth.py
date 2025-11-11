import os
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from config.database import db
from schemas.auth import UsuarioInDB, TokenData, UsuarioCreate, Usuario
from utils.jwt_handler import create_access_token, decode_token
from dotenv import load_dotenv


load_dotenv()

# Lee el tiempo de expiracion del token desde .env
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))

# --- OBJETOS ---
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- Funcion para HASHEAR un password ---
def get_password_hash(password: str) -> str:
    
    return password_hash.hash(password)


# --- Funcion para VERIFICAR un password ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# --- Funcion para OBTENER un usuario de la DB ---
async def get_user(username: str) -> UsuarioInDB | None:
    query = "SELECT id, username, hashed_password FROM usuarios WHERE username = :username"
   
    row = await db.fetch_one(query, values={"username": username})
    
    # Convierte el resultado de la DB a un objeto Pydantic
    return UsuarioInDB(**dict(row)) if row else None


# --- Funcion para AUTENTICAR un usuario ---
async def authenticate_user(username: str, password: str):
    usuario = await get_user(username)
    # Si no existe O el password es incorrecto, devuelve None
    if not usuario or not verify_password(password, usuario.hashed_password):
        return None  

    return usuario


# --- Funcion de DEPENDENCIA para proteger rutas ---
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
 
    payload = decode_token(token)
 
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")

    usuario = await get_user(username)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    return usuario


# --- Funcion para CREAR un nuevo usuario ---
async def create_user(usuario: UsuarioCreate):
    
    # Verifica si el usuario ya existe
    existing_user = await get_user(usuario.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El nombre de usuario ya esta en uso"
        )

    hashed_password_value = get_password_hash(usuario.password)
    
    # Consulta que agrega al nuevo usuario
    query = "INSERT INTO usuarios (username, hashed_password) VALUES (:username, :hashed_password)"
    values = {"username": usuario.username, "hashed_password": hashed_password_value}
    
    # Ejecuta
    try:
        # Captura el ID del usuario recien creado
        last_id = await db.execute(query, values)

        # Devuelve el ID y el username, cumpliendo con el schema 'Usuario'
        return {"id": last_id, "username": usuario.username}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario en la base de datos: {e}"
        )