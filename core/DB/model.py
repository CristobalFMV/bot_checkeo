import socket
import uuid
import getpass
import platform
import datetime
import subprocess
import os

def get_equipo_local():
    ip = socket.gethostbyname(socket.gethostname())
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                    for ele in range(0, 8 * 6, 8)][::-1])
    usuario = getpass.getuser()
    host = socket.gethostname()
    sistema_op = platform.system() + " " + platform.release()
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Datos de ejemplo o falsos si no se pueden obtener
    return {
        "ip": ip,
        "usuario": usuario,
        "anexo": "",
        "serial": obtener_serial(),
        "mac": mac,
        "ubicacion": "",  # Puedes dejarlo vacío o configurarlo según lógica local
        "host": host,
        "app_install1": "Topia" if app_instalada("Topia") else "No",
        "firewall": obtener_estado_firewall(),
        "app_install2": "Sofos" if app_instalada("Sofos") else "No",
        "sistema_op": sistema_op,
        "tipo_cpu": platform.processor(),
        "pantalla": "",
        "huellero": "No",
        "ytb_premium": "No",
        "admin": es_admin(),
        "remoto": acceso_remoto_habilitado(),
        "observacion": "",
        "nombre_soporte": usuario,
        "fecha": fecha
    }


def obtener_serial():
    try:
        result = subprocess.check_output("wmic bios get serialnumber", shell=True)
        return result.decode().split("\n")[1].strip()
    except:
        return "Desconocido"


def es_admin():
    try:
        return "Sí" if os.getuid() == 0 else "No"
    except AttributeError:
        import ctypes
        return "Sí" if ctypes.windll.shell32.IsUserAnAdmin() != 0 else "No"


def acceso_remoto_habilitado():
    try:
        result = subprocess.check_output(
            'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections', shell=True)
        return "Sí" if b'0x0' in result else "No"
    except:
        return "Desconocido"


def obtener_estado_firewall():
    try:
        result = subprocess.check_output("netsh advfirewall show allprofiles", shell=True)
        return "Activo" if b"Estado                                 ON" in result else "Inactivo"
    except:
        return "Desconocido"


def app_instalada(nombre_app):
    try:
        result = subprocess.check_output(f'wmic product get name', shell=True)
        return nombre_app.lower() in result.decode().lower()
    except:
        return False
