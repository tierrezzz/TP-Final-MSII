from pydantic import BaseModel

# --- Schema para la respuesta del Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Schema para los datos DENTRO del Token ---
class TokenData(BaseModel):
    username: str | None = None

# --- Schema para el Usuario (Publico) ---
class Usuario(BaseModel):
    id: int
    username: str
    
    # Configuracion para que Pydantic pueda leer datos
    # desde objetos de base de datos y no solo dicts
    class Config:
        from_attributes = True 

# --- Schema para el Usuario (en Base de Datos) ---
class UsuarioInDB(Usuario):
    hashed_password: str
    # Tambien necesita leer desde atributos de BD
    class Config:
        from_attributes = True

# --- Schema para Crear un Usuario ---
class UsuarioCreate(BaseModel):
    username: str
    password: str