import subprocess
import os
import getpass
import requests
import tkinter as tk
from tkinter import simpledialog

####ARCHIVO PARA SCRAPEAR DATOS DEL PC####


def pedirAnexo():
    root = tk.Tk()
    root.withdraw()
    anexo = simpledialog.askstring("ANEXO DEL EQUIPO","Ingrese el Anexo que corresponde a este equipo")
    return anexo
def pedirPassword():
    root = tk.Tk()
    root.withdraw()
    contrasena = simpledialog.askstring("CONTRASEÑA DEL EQUIPO", "Ingrese la contraseña de este equipo")
    return contrasena
def checkCurrentUser():
    usuario = getpass.getuser()
    return usuario
def checkIP():
    global value
    try:
        check_ip = subprocess.check_output("ipconfig", shell=True, text=True)
        value =""
        salida = check_ip.splitlines()
        for linea in salida:
            if "IPv4" in linea:
                value = linea.strip().split()[-1]
                print("Dirección IPv4: " + value)
                return value
        if not value:
            msg = "No se encontró dirección ip"
            return msg
    except subprocess.CalledProcessError as e:
        print("Error en la ejecución del comando CMD")
        print(e)
    return value
def checkProfile():
    check_user = getpass.getuser()
    return check_user
def checkAdmin():
    try:
        check_admin = subprocess.check_output("powershell -Command \"[bool]([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)\"",text=True)
        if check_admin.strip() == "True":
            msg = "Es administrador"
            return msg
        else:
            msg = "No está habilitado como administrador"
            return msg
    except subprocess.CalledProcessError as e:
        msg_error = (f"Ha ocurrido un error" + {e})
        return msg_error
def checkRDP():
    try:
        check_remote = subprocess.check_output('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections'
, shell=True,text=True)
        salida = check_remote.splitlines()
        for e in salida:
            if "fDenyTSConnections" in e:
                value = e.strip().split()[-1]
                if value == "0x0":
                    msg = "TIENE ACCESO REMOTO"
                    return msg
                else:
                    msg = "NO TIENE ACCESO REMOTO"
                    return msg
    except subprocess.CalledProcessError as e:
        msg_error_check = "Error checkeando"
        return msg_error_check
def checkFirewall():
    try:
        fwCmd = subprocess.check_output("netsh advfirewall show allprofiles", shell=True, text=True)
        salida = fwCmd.splitlines()
        firewall_activo = False
        for e in salida:
            if e.strip() == "True":
                firewall_activo = True
                break
        if firewall_activo:
            msg_firewall_activo = "1"
            return msg_firewall_activo
        else:
            msg_firewall_desactivado = "2"
            return msg_firewall_desactivado

    except subprocess.CalledProcessError as e:
        msg_error ="Ha ocurrido un error leyendo el Firewall "+ e
        return msg_error
def checkMac():
    try:
        check_mac = subprocess.check_output("getmac -v", shell=True, text=True)
        salida = check_mac.splitlines()
        for linea in salida:
            if "Ethernet" in linea:
                partes = linea.strip().split()
                for parte in partes:
                    if "-" in parte and len(parte) >= 17:
                        return parte
        return "No se ha encontrado dirección MAC"

    except subprocess.CalledProcessError as e:
        return f"Error checkeando dirección MAC: {e}"
def checkHost():
    try:
        check_hostname = subprocess.check_output("hostname",shell=True,text=True)
        return check_hostname
    except subprocess.CalledProcessError as e:
        msg_error = "error checkeando Hostname del equipo\n" + e
        return msg_error
def checkSerial():
    try:
        check_serialnumber = subprocess.check_output("wmic bios get serialnumber",text=True,shell=True)
        return check_serialnumber
    except subprocess.CalledProcessError as e:
        msg = (f"(Error leyendo el serialnumber del equipo\n + {e}")
        return  msg
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
                return "Sí"
        except subprocess.CalledProcessError:
            continue
    return "No"

def checkYTB():
    try:
        check_ytb = requests.get("https://www.youtube.com", timeout=5)
        if check_ytb.status_code == 200:
            msg = 'Sí'
            return msg
        if check_ytb.status_code == 500:
            msg = 'No'
            return msg
    except requests.RequestException as e:
        msg_error = 'Ha ocurrido un error '+e
        return msg_error
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
        return tipo_detectado
    except Exception as e:
        msg_error = "Error detectando el tipo de equipo: "+ e
        return msg_error

#for que ejecuta cada funcion previa y evita que el script se detenga si falla una
#def runScript():
#    for func in [checkIP, checkHost, checkMac, checkSerial, checkAdmin, checkRDP, checkProfile,
#                 checkYTB, checkTipoEquipo, lambda: check_app_instalada("Topia.exe")]:
#        try:
#            func()
#        except Exception as e:
#            nombre = getattr(func, '__name__', 'función anónima o lambda')
#            print(f"Error ejecutando {nombre}: {e}")






