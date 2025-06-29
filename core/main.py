from openpyxl import load_workbook
from core.modules.checkeo import checkIP
from core.excel.utils import buscar_fila_por_ip
from core.excel.writeExcel import Equipo
from core.config.ruta_excel import archivo_vicarius

def main():
    try:
        wb = load_workbook(archivo_vicarius)
        hojas = ['10.1.2.', 'HALLAZGOS ', '10.1.3.', ' 10.1.4.', '10.1.5.', '10.1.7.',
                 '10.1.10.', '10.1.11.', ' 10.1.12.', ' 10.1.13.', '10.1.15.', '10.1.16',
                 '10.1.20.1', '10.1.18.1', '10.1.21.1', '192.1.1.0', ' 168.88.162.',
                 '168.88.164.1', '168.88.165.1']

        ip_local = checkIP()
        ws, fila = buscar_fila_por_ip(wb, hojas, ip_local)

        if ws and fila:
            equipo = Equipo()
            equipo.escribir_en_excel(ws, fila)
            wb.save(archivo_vicarius)
            print("✔ Datos escritos correctamente.")
        else:
            print("❌ IP no encontrada.")

    except Exception as e:
        print(f"⚠ Error: {e}")

if __name__ == '__main__':
    main()
