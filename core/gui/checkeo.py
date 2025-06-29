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
"""
Funciones que extraen informacion del equipo de acuerdo a requisitos de planilla VICARIUS RANGO IP
"""
root = tk.Tk()
root.withdraw()

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

def checkFirewall():
    try:
        w = wmi.WMI(namespace="root\\StandardCimv2")
        perfiles = {
            1: "Dominio",
            2: "Privado",
            3: "Público"
        }
        resultados = []

        for perfil in w.MSFT_NetFirewallProfile():
            nombre = perfiles.get(perfil.Name, f"Desconocido ({perfil.Name})")
            estado = "Activo" if perfil.Enabled else "Inactivo"
            resultados.append(f"{nombre}: {estado}")

        return resultados
    except Exception as e:
        return [f"Error al verificar firewall: {e}"]


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




