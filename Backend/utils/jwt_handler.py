import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

# --- Configuracion de JWT ---
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))

# --- Funcion para CREAR un token ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):

    # Copia los datos que van dentro del token
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Agrega la fecha de expiracion al token
    to_encode.update({"exp": expire})
    
    # Firma el token con la clave secreta y lo devuelve
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- Funcion para DECODIFICAR un token ---
def decode_token(token: str):

    try:
        # Intenta validar la firma y la expiracion
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Si esta OK, devuelve los datos (ej: username)
        return payload
    except ExpiredSignatureError:
        # El token se vencio
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except InvalidTokenError:
        # El token es falso o esta corrupto
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")