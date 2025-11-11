from fastapi import APIRouter, Depends, Response
from schemas.auth import Usuario
from services.auth import get_current_user
from services.reporte import get_ventas_mensuales
from fpdf import FPDF
from typing import List

# Creamos router. /reportes
router = APIRouter(prefix="/reportes", tags=["Reportes"])

# Esta funcion solo existe para ser llamada por el endpoint
def generar_pdf(datos: List, titulo: str):
    """
    Funcion auxiliar para crear el PDF con FPDF.
    """
    # Inicia FPDF
    pdf = FPDF()
    pdf.add_page()
    
    # --- Estilos del PDF ---
    # el titulo
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, titulo, 0, 1, "C")
    pdf.ln(10)
    
    # los encabezados de la tabla
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "Año", 1) 
    pdf.cell(50, 10, "Mes", 1)
    pdf.cell(50, 10, "Total Ventas", 1)
    pdf.ln()
    
    # tabla con los datos
    pdf.set_font("Arial", "", 12)
    for fila in datos:
        pdf.cell(50, 10, str(fila.anio), 1)
        pdf.cell(50, 10, str(fila.mes), 1)
        pdf.cell(50, 10, f"${fila.total_ventas:,.2f}", 1)
        pdf.ln()
        
    # Genera el PDF y lo devuelve como 'bytes'
    return bytes(pdf.output(dest='S'))


# Endpoint de Reporte de Ventas
# Ruta GET /reportes/ventas/mensual
@router.get("/ventas/mensual")
async def reporte_ventas_mensuales(user: Usuario = Depends(get_current_user)):
    """
    Genera un reporte en PDF de las ventas mensuales.
    """
    # Esta ruta esta protegida. Primero valida el token.
    
    # Obtiene los datos de la base de datos
    datos = await get_ventas_mensuales()
    
    # Llama a la funcion auxiliar para crear el PDF en memoria
    pdf_bytes = generar_pdf(datos, "Reporte de Ventas Mensuales")
    
    # Devuelve una respuesta HTTP especial (no un JSON)
    return Response(
        content=pdf_bytes, # El contenido es el PDF en bytes
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_ventas_mensuales.pdf"}
    )