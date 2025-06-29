from datetime import date
from tkinter import simpledialog
from screeninfo import get_monitors
import getpass
import requests
import tkinter as tk
import math
import ctypes
import wmi
import socket
import winreg
import win32com.client
import uuid
import platform
import os
import subprocess
root = tk.Tk()
root.withdraw()
ruta_sofos = 'C:\\Program Files\\Sophos'
"""
Funciones que extraen informacion del equipo
"""
def checkCurrentUser():
    return getpass.getuser()
def checkIP():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        return f"Error obteniendo IP: {e}"
def checkProfile():
    check_user = getpass.getuser()
    return check_user
def checkAdmin():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return "SÍ" if is_admin else "NO"
    except:
        return "❌ No se pudo verificar privilegios de administrador."
def checkRDP():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Terminal Server")
        value, _ = winreg.QueryValueEx(key, "fDenyTSConnections")
        return "SÍ" if value == 0 else "NO"
    except Exception as e:
        return f"Error leyendo RDP: {e}"
import subprocess

def obtener_estado_firewall():
    try:
        comando = [
            "powershell.exe",
            "-Command",
            "Get-NetFirewallProfile | Select-Object Name, Enabled"
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        salida = resultado.stdout.strip().splitlines()
        estados = {}
        perfil_actual = None

        for linea in salida:
            if "Domain" in linea:
                perfil_actual = "Dominio"
            elif "Private" in linea:
                perfil_actual = "Privado"
            elif "Public" in linea:
                perfil_actual = "Público"

            if "True" in linea and perfil_actual:
                estados[perfil_actual] = True
            elif "False" in linea and perfil_actual:
                estados[perfil_actual] = False

        valores = list(estados.values())
        if all(valores):
            return "1"
        elif not any(valores):
            return "2"
        else:
            return "Algunos perfiles activos"
    except subprocess.CalledProcessError as e:
        print("Error al obtener el estado del firewall:")
        print(e.stderr)
        return None
def checkMac():
    mac = uuid.getnode()
    return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

def checkHost():
    return socket.gethostname()
def checkSerial():
    try:
        c = wmi.WMI()
        for bios in c.Win32_BIOS():
            return bios.SerialNumber
    except Exception as e:
        return f"Error leyendo el serial: {e}"
def check_ruta_topia():
    user = getpass.getuser()
    ruta_topia = f'C:\\Users\\{user}\\Topia.exe'
    if os.path.exists(ruta_topia):
        msg = "Sí está instalado"
        return msg
    else:
        msg = "No está instalado"
        return msg

def check_ruta_sofos():
    if os.path.exists(ruta_sofos):
        msg = "Sí"
        return msg
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
        c = wmi.WMI()
        chasis_list = []
        for enclosure in c.Win32_SystemEnclosure():
            if enclosure.ChassisTypes:
                chasis_list.extend(enclosure.ChassisTypes)

        descripcion = {
            3: "Desktop/CPU",
            4: "Low Profile Desktop",
            6: "Mini Tower",
            7: "Tower",
            13: "All-in-One/AIO",
            9: "Laptop",
            10: "Notebook"
        }

        tipo_detectado = [descripcion.get(c, f"Desconocido ({c})") for c in chasis_list]
        return str(tipo_detectado) if tipo_detectado else "No se pudo detectar el tipo de equipo"
    except Exception as e:
        return f"⚠️ Error detectando el tipo de equipo: {e}"
def checkOS():
    return platform.release()  # "10", "11", etc.
def checkScreen():
    global monitores;
    try:
        for monitores in get_monitors():
            alto = (monitores.height_mm / 25.4)**2
            ancho = (monitores.width_mm / 25.4)**2
            pitagoras = math.sqrt(alto+ancho)
            str_pitagoras = str(pitagoras)
            pulgadas = str_pitagoras.split(".")[0]
            return pulgadas + " pulgadas"
    except Exception as e:
        return e
def checkObservaciones():

    observacion = simpledialog.askstring("OBSERVACION","Escriba la observación si hay una")
    return observacion
def checkNombreSoporte():
    nombre = simpledialog.askstring("NOMBRE DE QUIEN REVISA", "Escriba su nombre")
    return nombre
def checkFecha():
    fecha = date.today().strftime("%Y-%m-%d")
    return fecha




