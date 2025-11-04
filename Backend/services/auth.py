import os
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# --- CAMBIOS AQUÍ ---
# 1. Reemplazamos passlib por pwdlib
from pwdlib import PasswordHash
from config.database import db
# Importamos 'Usuario' para la validación de 'get_current_user'
from schemas.auth import UsuarioInDB, TokenData, UsuarioCreate, Usuario
from utils.jwt_handler import create_access_token, decode_token
from dotenv import load_dotenv


load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))

# --- CAMBIOS AQUÍ ---
# 2. Configuramos pwdlib (igual que en tu proyecto funcional)
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- CAMBIOS AQUÍ ---
# 3. Creamos la función 'get_password_hash' (igual que en tu proyecto funcional)
def get_password_hash(password: str) -> str:
    # pwdlib maneja el límite de 72 bytes automáticamente
    return password_hash.hash(password)

# --- CAMBIOS AQUÍ ---
# 4. Actualizamos 'verify_password' para usar pwdlib
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # pwdlib maneja el límite de 72 bytes automáticamente
    return password_hash.verify(plain_password, hashed_password)

async def get_user(username: str) -> UsuarioInDB | None:
    # (Sin cambios, esta consulta es correcta)
    query = "SELECT id, username, hashed_password FROM usuarios WHERE username = :username"
    row = await db.fetch_one(query, values={"username": username})
    
    return UsuarioInDB(**row) if row else None

async def authenticate_user(username: str, password: str):
    usuario = await get_user(username)
    # (Sin cambios, ahora usa la nueva 'verify_password')
    if not usuario or not verify_password(password, usuario.hashed_password):
        return None  
    return usuario

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    usuario = await get_user(username)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    
    # Ahora devolvemos un objeto Usuario que incluye el 'id'
    return Usuario.from_attributes(usuario)

async def create_user(usuario: UsuarioCreate):
    
    # 1. (Sin cambios) Verificar si el usuario ya existe
    existing_user = await get_user(usuario.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El nombre de usuario ya está en uso"
        )

    # --- CAMBIOS AQUÍ ---
    # 2. Hashear la contraseña usando la nueva función
    hashed_password_value = get_password_hash(usuario.password)
    
    # 3. (Sin cambios) Usamos la columna 'hashed_password'
    query = "INSERT INTO usuarios (username, hashed_password) VALUES (:username, :hashed_password)"
    values = {"username": usuario.username, "hashed_password": hashed_password_value}
    
    try:
        await db.execute(query, values)
        # 4. (Sin cambios) Devolver un diccionario seguro
        return {"username": usuario.username}
    except Exception as e:
        # 5. (Sin cambios) Captura genérica
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario en la base de datos: {e}"
        )