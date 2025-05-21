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
df = pd.read_excel(planilla_vicarius, engine='openpyxl', header=4)
df_telefonos= pd.read_excel(planilla_telefonos, engine='openpyxl',header=1)
#print(df_telefonos.columns)
#print(df_telefonos.loc[1,columnas_telefonos])
#print(df.columns)
#print(df.loc[1,columnas_excel])
#print(df.loc[0:253])
#print(df.iloc[0:253])
def buscarIPtelefonos():
    filasTelefonos = df_telefonos.iloc[0:357]
    datosTelefonos = filasTelefonos.values.tolist()
    cont2=0
    for i in datosTelefonos:
        cont2 +=1
        ipTel= i[3]
    return ipTel
def buscarDispositivo():
    cont = 0
    filas = df.iloc[0:253]
    datos = filas.values.tolist()
    for x in datos:
        cont += 1
        ip = x[0]
    return ip

def compareIP():
        ip_telefono = buscarIPtelefonos()
        ip_dispositivo = buscarDispositivo()
        print(ip_dispositivo)
        print(ip_telefono)

compareIP()
