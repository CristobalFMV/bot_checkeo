import os.path
from datetime import date
from tkinter import simpledialog
from screeninfo import get_monitors
import subprocess
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

root = tk.Tk()
root.withdraw()

ruta_sofos = 'C:\\Program Files\\Sophos'

'''
def tieneHuellero():
    huellero = simpledialog.askstring("HUELLERO", "¿El equipo tiene huellero?")
    return huellero
def pedirAnexo():
    anexo = simpledialog.askstring("ANEXO DEL EQUIPO","Ingrese el Anexo que corresponde a este equipo")
    return anexo
def pedirPassword():

    contrasena = simpledialog.askstring("CONTRASEÑA DEL EQUIPO", "Ingrese la contraseña de este equipo")
    return contrasena
def pedirUbicacion():
    ubicacion = simpledialog.askstring("UBICACIÓN", "Ingrese el servicio donde está ubicado el equipo")
    return ubicacion'''
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
def obtener_estado_firewall():
    try:
        comando = [
            "powershell",
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

            if "True" in linea:
                estados[perfil_actual] = True
            elif "False" in linea:
                estados[perfil_actual] = False

        # Evaluamos los estados
        valores = list(estados.values())
        if all(valores):
            return "1"  # Todos activos
        elif not any(valores):
            return "2"  # Todos desactivados
        else:
            return "Algunos perfiles activos"
    except subprocess.CalledProcessError as e:
        print("Error al obtener el estado del firewall:", e)
        return None
def checkMac():
    mac = uuid.getnode()
    return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

def checkHost():
    return socket.gethostname()


def check_serial():
    try:
        c = wmi.WMI()

        # Intenta con Win32_BIOS
        bios_list = c.Win32_BIOS()
        if bios_list:
            serial = bios_list[0].SerialNumber.strip()
            if serial and "O.E.M" not in serial and serial.lower() != "none":
                print(serial)
                return serial

        # Fallback con Win32_SystemEnclosure
        enclosure_list = c.Win32_SystemEnclosure()
        if enclosure_list:
            serial = enclosure_list[0].SerialNumber.strip()
            if serial and "O.E.M" not in serial and serial.lower() != "none":
                print(serial)
                return serial

        return "Serial no disponible o inválido"

    except Exception as e:
        return f"Error leyendo el serial: {e}"


def check_app_instalada(nombre_app):
    claves = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    for root, path in claves:
        try:
            with winreg.OpenKey(root, path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if nombre_app.lower() in name.lower():
                                return "Sí"
                        except FileNotFoundError:
                            continue
        except FileNotFoundError:
            continue
    return "No"

def check_ruta_sofos():
    if os.path.exists(ruta_sofos):
        msg = "Sí"
        return msg
    else:
        msg = "No"
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




