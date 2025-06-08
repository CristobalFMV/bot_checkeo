import sys
import os

if getattr(sys, 'frozen', False):
    # Carpeta donde está el EXE que se usa en otros equipos!!
    ruta_base = os.path.dirname(sys.executable)
else:
    # Carpeta donde está el .py archivo principal para ejecución
    ruta_base = os.path.dirname(os.path.abspath(__file__))

archivo_vicarius = os.path.join(ruta_base, 'vicarius.xlsx')
