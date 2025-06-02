from openpyxl import Workbook, load_workbook
import checkeo

##aquí se escribe en el excel
archivo_vicarius = 'A:\\Python\\data\\vicarius.xlsx'
wb = load_workbook(archivo_vicarius)
hojas_vicarius = ['10.1.2.', 'HALLAZGOS ', '10.1.3.', ' 10.1.4.', '10.1.5.', '10.1.7.',
                  '10.1.10.', '10.1.11.', ' 10.1.12.', ' 10.1.13.', '10.1.15.', '10.1.16',
                  '10.1.20.1', '10.1.18.1', '10.1.21.1', '192.1.1.0', ' 168.88.162.',
                  '168.88.164.1', '168.88.165.1']
ws = wb.active
current_ws = wb['10.1.3.']
ip_local = checkeo.checkIP()

for ws in wb.worksheets:
    for fila in range(5,ws.max_row + 1):
        if ws[f"A{fila}"].value == ip_local:
            ws[f"C{fila}"] = checkeo.checkCurrentUser()
            ws[f"D{fila}"] = checkeo.pedirPassword()
            ws[f"E{fila}"] = checkeo.pedirAnexo()
            ws[f"F{fila}"] = checkeo.checkSerial()
            ws[f"G{fila}"] = checkeo.checkMac()
            ws[f"I{fila}"] = checkeo.checkHost()
            ws[f"J{fila}"] = checkeo.check_app_instalada("Topia.exe")
            ws[f"K{fila}"] = checkeo.checkFirewall()
            ws[f"L{fila}"] = checkeo.check_app_instalada("Topia.exe")
            ws[f"M{fila}"] = checkeo.check_app_instalada("Sophos.exe")
            break
wb.save(archivo_vicarius)