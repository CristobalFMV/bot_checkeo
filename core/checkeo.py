import subprocess
import os
import getpass
import requests
import tkinter as tk
from tkinter import simpledialog

####ARCHIVO PARA SCRAPEAR DATOS DEL PC####

hostname = subprocess.check_output("hostname", shell=True, text=True).strip()
ruta_archivo = os.path.join(os.getcwd(), f"{hostname}_resultado_checkeo.txt")

with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write("Información de registro del equipo: " + hostname + "\n")
def pedirAnexo():
    root = tk.Tk()
    root.withdraw()
    anexo = simpledialog.askstring("ANEXO DEL EQUIPO","Ingrese el Anexo que corresponde a este equipo")
    print("Ingresado el anexo: "+anexo)
    return anexo
checkAnexo = pedirAnexo()
with open(ruta_archivo, "a", encoding="utf-8") as f:
    f.write("\n ==== ANEXO ==== \n\n" + checkAnexo +"\n")

def pedirPassword():
    root = tk.Tk()
    root.withdraw()
    contrasena = simpledialog.askstring("CONTRASEÑA DEL EQUIPO", "Ingrese la contraseña de este equipo")
    print("Contraseña guardada")
    return contrasena
checkPassword = pedirPassword()
with open(ruta_archivo,"a",encoding="utf-8") as f:
    f.write("\n === CONTRASEÑA DEL EQUIPO === \n\n"+checkPassword+"\n")

def checkIP():
    value = None
    try:
        check_ip = subprocess.check_output("ipconfig", shell=True, text=True)
        salida = check_ip.splitlines()
        for linea in salida:
            if "IPv4" in linea:
                print("linea encontrada " + linea)
                value = linea.strip().split()[-1]
                print("Dirección IPv4: " + value)
                with open(ruta_archivo, "a", encoding="utf-8") as f:
                    f.write("\n===== DIRECCION IP =====\n\n" + value + "\n")
                break
        if not value:
            with open(ruta_archivo, "a", encoding="utf-8") as f:
                f.write("\n===== DIRECCION IP NO ENCONTRADA =====")
    except subprocess.CalledProcessError as e:
        print("Error en la ejecución del comando CMD")
        print(e)
    return value
def checkProfile():
    check_user = getpass.getuser()
    with open(ruta_archivo,"a",encoding="utf-8") as f:
        f.write("\n==== Perfil en el equipo ====\n\n"+check_user+"\n")
def checkAdmin():


    try:
        check_admin = subprocess.check_output("powershell -Command \"[bool]([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)\"",text=True)
        if check_admin.strip() == "True":
            print("Es administrador")
            with open(ruta_archivo, "a", encoding="utf-8") as f:
                f.write("\n==== ¿ES ADMINISTRADOR? ====\n")
                f.write("\nSI es administrador\n")
        else:
            print("No está habilitado como administrador")
            with open(ruta_archivo, "a", encoding="utf-8") as f:
                f.write("\n==== ¿ES ADMINISTRADOR? ====\n")
                f.write("\nNO es administrador\n")
    except subprocess.CalledProcessError as e:
        print("Ha ocurrido un error")
def checkRDP():
    try:
        check_remote = subprocess.check_output('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections'
, shell=True,text=True)
        salida = check_remote.splitlines()
        for e in salida:
            if "fDenyTSConnections" in e:
                print("linea encontrada: "+ e)
                value = e.strip().split()[-1]
                if value == "0x0":
                    print("TIENE ACCESO REMOTO")
                    with open(ruta_archivo, "a", encoding="utf-8") as f:
                        f.write("\n==== ¿ESTÁ ACTIVADO EL ACCESO REMOTO? ====\n")
                        f.write("\nTIENE ACCESO REMOTO\n")
                else:
                    print("NO TIENE ACCESO REMOTO")
                    with open(ruta_archivo, "a", encoding="utf-8") as f:
                        f.write("\n==== ¿ESTÁ ACTIVADO EL ACCESO REMOTO? ====\n")
                        f.write("\nNO TIENE ACCESO REMOTO\n")
    except subprocess.CalledProcessError as e:
        print("Error checkeando.")
        print(e)
def checkFirewall():
    try:
        fwCmd = subprocess.check_output("powershell -Command (Get-NetFirewallProfile).Enabled", shell=True, text=True)
        salida = fwCmd.splitlines()
        firewall_activo = False
        for e in salida:
            if e.strip() == "True":
                firewall_activo = True
                break
        if firewall_activo:
            with open(ruta_archivo, "a", encoding="utf-8") as f:
                f.write("\n==== ¿ESTÁ ACTIVADO EL FIREWALL? ====\n")
                f.write("\nTIENE FIREWALL ACTIVO\n")
            print("firewall ACTIVADO en el equipo")

        else:
            with open(ruta_archivo, "a", encoding="utf-8") as f:
                f.write("\n==== ¿ESTÁ ACTIVADO EL FIREWALL? ====\n")
                f.write("\nNO, NO TIENE FIREWALL ACTIVO\n")
            print("firewall DESACTIVADO en el equipo")

    except subprocess.CalledProcessError as e:
        print("Error checkeando firewall")
        print(e)
def checkMac():
    try:
        check_mac = subprocess.check_output("getmac -v",shell=True, text=True)
        salida = check_mac.splitlines()
        for linea in salida:
            if "Wi-Fi" in linea:
                print("Linea encontrada: "+linea)
                value = linea.strip().split()[-2]
                if value:
                    print("Tiene direccion mac: "+value)
                    return value
                else:
                    print("No se ha encontrado dirección MAC")

    except subprocess.CalledProcessError as e:
        print("Error checkeando direccion MAC\n"+e)
def checkHost():
    try:
        check_hostname = subprocess.check_output("hostname",shell=True,text=True)
        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write("\n===== HOSTNAME =====\n\n" + check_hostname)
    except subprocess.CalledProcessError as e:
        print("error checkeando Hostname del equipo\n" + e)
def checkSerial():
    try:
        check_serialnumber = subprocess.check_output("wmic bios get serialnumber",text=True,shell=True)
        return check_serialnumber
    except subprocess.CalledProcessError as e:
        print("Error leyendo el serialnumber del equipo\n"+e)
def check_app_instalada(nombre_app):
    rutas = [
        r'HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall',
        r'HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
        r'HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall'
    ]

    for ruta in rutas:
        try:
            comando = f'reg query "{ruta}" /s /f "{nombre_app}" /d'
            resultado = subprocess.check_output(comando, shell=True, text=True, stderr=subprocess.DEVNULL)

            if nombre_app.lower() in resultado.lower():
                print(f"{nombre_app} está instalada (en: {ruta})")
                with open(ruta_archivo, "a",encoding="utf-8") as f:
                    f.write(f"\n==== ¿La aplicación {nombre_app} está instalada? ====\n")
                    f.write(f"\n¡La aplicación {nombre_app} SÍ está instalada en el equipo!\n")
                return True
            else:
                with open(ruta_archivo, "a",encoding="utf-8") as f:
                    f.write(f"\n==== ¿La aplicación {nombre_app} está instalada? ====\n")
                    f.write("\nAplicación NO instalada en el equipo\n")
        except subprocess.CalledProcessError:
            continue

    print(f"{nombre_app} NO está instalada.")
    return False
def checkYTB():
    try:
        check_ytb = requests.get("https://www.youtube.com", timeout=5)
        if check_ytb.status_code == 200:
            print("El equipo tiene acceso a Youtube")
            with open(ruta_archivo,"a",encoding="utf-8") as f:
                f.write("\n==== Acceso a YTB ====\n \nSI tiene acceso a Youtube!!\n")
            return True
        if check_ytb.status_code == 500:
            with open(ruta_archivo, "a", encoding="utf-8") as f:
                f.write("\n==== Acceso a YTB ====\n \nNO tiene acceso a Youtube\n")
    except requests.RequestException as e:
        print("No se tiene acceso a Youtube: ",e)
        return False
def checkTipoEquipo():
    try:
        tipo = subprocess.check_output(
            'powershell -Command "Get-WmiObject -Class Win32_SystemEnclosure | Select-Object -ExpandProperty ChassisTypes"',
            shell=True,
            text=True
        )

        tipo = tipo.strip().replace("{", "").replace("}", "")
        lineas = tipo.splitlines()

        chasis = []
        for linea in lineas:
            linea = linea.strip()
            if linea.isdigit():
                chasis.append(int(linea))

        descripcion = {
            3: "Desktop/CPU",
            4: "Low Profile Desktop",
            6: "Mini Tower",
            7: "Tower",
            13: "All-in-One/AIO",
            9: "Laptop",
            10: "Notebook"
        }

        tipo_detectado = [descripcion.get(c, f"Desconocido ({c})") for c in chasis]

        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write("\n==== TIPO DE EQUIPO ====\n\n")
            f.write("\n\n".join(tipo_detectado) + "\n")

        print("Tipo de equipo detectado:", ", ".join(tipo_detectado))

    except Exception as e:
        print("Error detectando el tipo de equipo:", e)

#for que ejecuta cada funcion previa y evita que el script se detenga si falla una
#def runScript():
#    for func in [checkIP, checkHost, checkMac, checkSerial, checkAdmin, checkRDP, checkProfile,
#                 checkYTB, checkTipoEquipo, lambda: check_app_instalada("Topia.exe")]:
#        try:
#            func()
#        except Exception as e:
#            nombre = getattr(func, '__name__', 'función anónima o lambda')
#            print(f"Error ejecutando {nombre}: {e}")

def checkIPExcel():
    try:
        check_ip = subprocess.check_output("ipconfig", shell=True, text=True)
        salida = check_ip.splitlines()
        for linea in salida:
            if "IPv4" in linea:
                value = linea.strip().split()[-1]
                return value.strip()
    except subprocess.CalledProcessError as e:
        print("Error en ipconfig:", e)
        return None






