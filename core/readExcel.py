import pandas as pd
import warnings
import checkeo
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
#planilla_vicarius = 'A:\\Python\\data\\vicarius.xlsx'
#planilla_telefonos = 'A:\\Python\\data\\telefonos.xlsx'

planilla_vicarius = 'A:\\Python\\data\\vicarius.xlsx'
hojas_vicarius = ['10.1.2.', 'HALLAZGOS ', '10.1.3.', ' 10.1.4.', '10.1.5.', '10.1.7.',
                  '10.1.10.', '10.1.11.', ' 10.1.12.', ' 10.1.13.', '10.1.15.', '10.1.16',
                  '10.1.20.1', '10.1.18.1', '10.1.21.1', '192.1.1.0', ' 168.88.162.', '168.88.164.1'
                    , '168.88.165.1']
planilla_telefonos = 'A:\\Python\\data\\telefonos.xlsx'
columnas_excel = ['IP Address', 'Estado', 'Perfil ', 'Clave', 'ANEXO', 'SERIAL NUMBER ',
       'Direccion MAC', 'UBICACIÓN ', 'Host Name', '   VICARIUS  INST. SI/NO ',
       'estado FW 1=ARRIBA 2=ABAJO ', 'SOPHOS', 'TIPO W XP-7-10-11',
       '    TIPO     CPU / AIO', 'TIPO MONITOR', 'HUELLERO SI/NO', 'YTB',
       'ADM', 'REMOTO SI/NO ']
columnas_telefonos = ['Unnamed: 0', 'Número', 'Nombre', 'IP', 'Tipo conexión', 'Unnamed: 5',
       'Unnamed: 6']
df = pd.read_excel(planilla_vicarius, engine='openpyxl',sheet_name=hojas_vicarius, header=4) ##vicarius
df_telefonos= pd.read_excel(planilla_telefonos, engine='openpyxl',header=1) ##telefonos
df_excel = pd.ExcelFile(planilla_vicarius)

###funciones sin uso aún, se espera utilizarlas para regularizar telefonos###
def recorrerHojasIP():
    for ws in hojas_vicarius:
        findIP()
def buscarIPtelefonos():
    #filasTelefonos = df_telefonos.iloc[0:357]
    #datosTelefonos = filasTelefonos.values.tolist()
    ip_list_tel = []
    for index, row in df_telefonos.iterrows():
        ipTel= row.iloc[3]
        if pd.notna(ipTel):
            ip_list_tel.append(str(ipTel).strip())
    return "telefono con ip: "+ str(ip_list_tel)
def buscarDispositivo():
    #filas = df.iloc[0:253]
    #datos = filas.values.tolist()
    ip_list_disp = []
    for name_hoja, df_hoja in df.items():
        for index, row in df_hoja.iterrows():
            ip = row.iloc[0]
            if pd.notna(ip):
                ip_list_disp.append(str(ip).strip())
        print("ip encontrada "+ip)
    return "dispositivo con ip: "+ str(ip_list_disp)

def findIP():
        ip_telefono = buscarIPtelefonos()
        ip_dispositivo = buscarDispositivo()
        ip_comunes = set(ip_telefono).intersection(ip_dispositivo)
        print("IP's en Ambos archivos Excel: ")
        for ip in ip_comunes:
            print(ip)
        ip_unicas = set(ip_telefono) - set(ip_dispositivo)
        print("IP's  no identificadas y presentes en solo 1 archivo Excel.")
        for ip in ip_unicas:
            print(ip)

recorrerHojasIP()