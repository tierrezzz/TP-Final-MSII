from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Usuario(BaseModel):
    id: int
    username: str
    
    # --- ARREGLO AQUÍ ---
    # Habilitamos la creación del modelo desde atributos de objeto
    class Config:
        from_attributes = True

class UsuarioInDB(Usuario):
    hashed_password: str
    # No necesita Config porque hereda el de Usuario

class UsuarioCreate(BaseModel):
    username: str
    password: str

