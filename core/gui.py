from openpyxl import load_workbook
import checkeo
import writeExcel

archivo_vicarius = 'A:\\Python\\data\\vicarius.xlsx'
hojas_vicarius = ['10.1.2.', 'HALLAZGOS ', '10.1.3.', ' 10.1.4.', '10.1.5.', '10.1.7.',
                  '10.1.10.', '10.1.11.', ' 10.1.12.', ' 10.1.13.', '10.1.15.', '10.1.16',
                  '10.1.20.1', '10.1.18.1', '10.1.21.1', '192.1.1.0', ' 168.88.162.',
                  '168.88.164.1', '168.88.165.1']

wb = load_workbook(archivo_vicarius)
ip_local = checkeo.checkIP()
encontrada = False

for hoja in hojas_vicarius:
    if encontrada:
        break
    ws = wb[hoja]

    for fila in range(5, ws.max_row + 1):
        celda = ws[f"A{fila}"]
        if celda.value and str(celda.value).strip() == ip_local:
            writeExcel.escribirExcel(ws, fila)
            encontrada = True
            break

if encontrada:
    wb.save(archivo_vicarius)
else:
    print("IP no encontrada en ninguna hoja.")

