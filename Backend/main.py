from fastapi import FastAPI
from config.database import db
from routers import auth, habitacion, reserva
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/")
async def root():
    return {"message": "Bienvenidos a mi API REST"}
    
app.include_router(auth.router)
app.include_router(habitacion.router)
app.include_router(reserva.router)