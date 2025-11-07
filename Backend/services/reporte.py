from config.database import db
from schemas.reporte import VentaAgrupada
from typing import List

# --- Funcion para OBTENER el reporte de ventas ---
async def get_ventas_mensuales() -> List[VentaAgrupada]:
    """
    Llama al procedimiento almacenado 'sp_reporte_ventas_mensual'
    para obtener las ventas agrupadas por mes.
    """
    
    # Consulta SQL para llamar al Stored Procedure
    query = "CALL sp_reporte_ventas_mensual();"
    
    # Ejecuta la consulta
    ventas_db = await db.fetch_all(query)
    
    """
    Mapea los resultados de la DB
    Convierte cada 'Record' de la DB en un 'dict'
    y luego usa el 'dict' para crear un objeto 'VentaAgrupada'
    Esto limpia y valida los datos que vienen del SP
    """
    return [VentaAgrupada(**dict(venta)) for venta in ventas_db]