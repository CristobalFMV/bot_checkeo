from openpyxl import load_workbook
import checkeo

##aquí se escribe en el excel
archivo_vicarius = 'C:\\Users\\cmene\\PycharmProjects\\ML_py_Iris\\data\\vicarius.xlsx'
wb = load_workbook(archivo_vicarius)

hoja = wb['10.1.3.']
fila = 21
columna = 6
hoja.cell(row=fila, column=columna).value = checkeo.checkSerial()
hoja.cell(row=fila, column=columna+1).value = checkeo.checkMac()

wb.save(archivo_vicarius)