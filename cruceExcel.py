import pandas as pd
import warnings
import lectura as check
from openpyxl import workbook as wb
from openpyxl import worksheet as ws
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
vicarius_excel = 'excels/vicarius.xlsx'
telefonos_excel ='excels/telefonos.xlsx'
hoja = "10.1.18.1"

#leer excel
df = pd.read_excel(vicarius_excel, engine='openpyxl',sheet_name=hoja,header=4)

df["IP Address"] = df["IP Address"].astype(str).str.strip()
ip_local = check.checkIPExcel()

if ip_local is None:
    print("no se pudo obtener la ip local")
    exit()

fila_indice = df.index[df["IP Address"] == ip_local].tolist()

if not fila_indice:
    print("la ip local no está en el excel")
    exit()

indice = fila_indice[0]

#obtener valores
df.at[indice, "Host Name"] = check.checkHost()
df.at[indice, "Direccion MAC"] = check.checkMac()
df.at[indice, "SERIAL NUMBER"] = check.checkSerial()
df.at[indice, "ADM"] = check.checkAdmin()
df.at[indice, "REMOTO SI/NO"] = check.checkRDP()
df.at[indice, "estado FW 1=ARRIBA 2=ABAJO"] = check.checkProfile()
df.at[indice, "YTB"] = check.checkYTB()
df.at[indice, "TIPO CPU / AIO"] = check.checkTipoEquipo()
df.at[indice, "VICARIUS INST. SI/NO"] = "SI" if check.check_app_instalada("Topia.exe") else "NO"

df.to_excel("A:\\Python\\excels\\vicarius_actualizado.xlsx", index=False)

print("✅ Datos actualizados correctamente en el Excel.")