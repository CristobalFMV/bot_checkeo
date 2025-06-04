import os
import sys

if getattr(sys, 'frozen', False):
    ruta_base = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))

archivo_vicarius = os.path.join(ruta_base, 'vicarius.xlsx')
