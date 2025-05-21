import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

planilla_vicarius = 'excels\\vicarius.xlsx'
planilla_telefonos = 'excels\\telefonos.xlsx'
columnas_excel = ['IP Address', 'Estado', 'Perfil ', 'Clave', 'ANEXO', 'SERIAL NUMBER ',
       'Direccion MAC', 'UBICACIÓN ', 'Host Name', '   VICARIUS  INST. SI/NO ',
       'estado FW 1=ARRIBA 2=ABAJO ', 'SOPHOS', 'TIPO W XP-7-10-11',
       '    TIPO     CPU / AIO', 'TIPO MONITOR', 'HUELLERO SI/NO', 'YTB',
       'ADM', 'REMOTO SI/NO ']
columnas_telefonos = ['Unnamed: 0', 'Número', 'Nombre', 'IP', 'Tipo conexión', 'Unnamed: 5',
       'Unnamed: 6']
df = pd.read_excel(planilla_vicarius, engine='openpyxl', header=4) ##vicarius
df_telefonos= pd.read_excel(planilla_telefonos, engine='openpyxl',header=1) ##telefonos
#print(df_telefonos.columns)
#print(df_telefonos.loc[1,columnas_telefonos])
#print(df.columns)
#print(df.loc[1,columnas_excel])
#print(df.loc[0:253])
#print(df.iloc[0:253])
def buscarIPtelefonos():
    filasTelefonos = df_telefonos.iloc[0:357]
    datosTelefonos = filasTelefonos.values.tolist()
    ip_list_tel = []
    for i in datosTelefonos:
        ipTel= i[3]
        if pd.notna(ipTel):
            ip_list_tel.append(str(ipTel).strip())
    return ip_list_tel
def buscarDispositivo():
    filas = df.iloc[0:253]
    datos = filas.values.tolist()
    ip_list_disp = []
    for x in datos:
        ip = x[0]
        if pd.notna(ip):
            ip_list_disp.append(str(ip).strip())
    return ip_list_disp

def compareIP():
        ip_telefono = buscarIPtelefonos()
        ip_dispositivo = buscarDispositivo()
        ip_comunes = set(ip_telefono).intersection(ip_dispositivo)
        print("IP's en Ambos archivos Excel: ")
        for ip in ip_comunes:
            print(ip)
        ip_unicas = set(ip_telefono) - set(ip_dispositivo)
        print("IP's que no identificadas y presentes en solo 1 archivo Excel")
        for ip in ip_unicas:
            print(ip)

compareIP()
