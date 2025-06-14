from core.excel.writeExcel import Equipo
from core.DB.model import get_equipo_local
from core.DB.connection_server import guardar_en_bd
# Obtener datos del sistema
datos = get_equipo_local()

# Crear objeto
datos["id"] = None
equipo = Equipo(**datos)

# Guardar en base de datos
guardar_en_bd(equipo)
print("✅ Equipo guardado en base de datos correctamente.")
