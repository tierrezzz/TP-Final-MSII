from pydantic import BaseModel

# --- Schema para los datos del Reporte ---
class VentaAgrupada(BaseModel):
    anio: int
    mes: int
    total_ventas: float
