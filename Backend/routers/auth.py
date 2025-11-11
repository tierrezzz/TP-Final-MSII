from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from schemas.auth import Token, Usuario, UsuarioCreate
from services.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_user

# Creamos un router. /auth
router = APIRouter(prefix="/auth", tags=["Auth"])

# --- Endpoint de Login ---
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    
    usuario = await authenticate_user(form_data.username, form_data.password)
    
    # Si el servicio devuelve None (fallo)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Crea el token JWT
    token = create_access_token(data={"sub": usuario.username}, expires_delta=access_token_expires)

    return Token(access_token=token, token_type="bearer")

'''
 La ruta GET /auth/me 
 esta funcion depende de "get_current_user"
 "get_current_user" se encarga de validar el token (Bearer)
 Si el token es valido, devuelve los datos del usuario.
 Si es invalido, "get_current_user" ya lanzo el error HTTP
'''
@router.get("/me", response_model=Usuario)
async def read_users_me(current_user: Annotated[Usuario, Depends(get_current_user)]):
   
    return current_user

# --- Endpoint de Registro ---
@router.post("/register", response_model=Usuario)
async def register(usuario: UsuarioCreate):

    return await create_user(usuario)