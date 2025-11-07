import os
from dotenv import load_dotenv
from databases import Database

# Carga las variables de entorno
load_dotenv()

# --- Configuracion de Base de Datos ---

# Lee las variables de entorno para la DB
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# URL de conexion para MySQL (compatible con async)
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crea la instancia de base de datos asincrona
db = Database(DATABASE_URL)