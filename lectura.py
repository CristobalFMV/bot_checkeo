import subprocess
import os
hostname = subprocess.check_output("hostname", shell=True, text=True).strip()
ruta_archivo = os.path.join(os.getcwd(), f"{hostname}_resultado_checkeo.txt")
with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write("Información de registro del equipo: " + hostname + "\n\n")
def checkIP():
    try:
        check_ip = subprocess.check_output("ipconfig",shell=True,text=True)
        salida = check_ip.splitlines()
        for linea in salida:
            if "IPv4" in linea:
                print("linea encontrada "+linea)
                value = linea.strip().split()[-1]
                if value:
                    print("Dirección IPv4: "+value)
                    with open(ruta_archivo, "a", encoding="utf-8") as f:
                        f.write("\n===== DIRECCION IP =====\n"+value)
                else:
                    with open(ruta_archivo, "a", encoding="utf-8") as f:
                        f.write("\n===== DIRECCION IP NO ENCONTRADA =====")
    except subprocess.CalledProcessError as e:
        print("error en la ejecucion del comando CMD")
        print(e)
def checkAdmin():


    try:
        check_admin = subprocess.check_output("powershell -Command \"[bool]([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)\"",text=True)
        if check_admin.strip() == True:
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
        check_remote = subprocess.check_output('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections', shell=True,text=True)
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
                    with open(ruta_archivo, "a", encoding="utf-8") as f:
                        f.write("\n===== DIRECCION MAC =====\n "+value)
                else:
                    print("No se ha encontrado dirección MAC")
                    with open(ruta_archivo, "a", encoding="utf-8") as f:
                        f.write("\nDireccion mac no encontrada en el equipo")
    except subprocess.CalledProcessError as e:
        print("Error checkeando direccion MAC\n"+e)
def checkHost():
    try:
        check_hostname = subprocess.check_output("hostname",shell=True,text=True)
        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write("\n===== HOSTNAME =====\n" + check_hostname)
    except subprocess.CalledProcessError as e:
        print("error checkeando Hostname del equipo\n" + e)
def checkSerial():
    try:
        check_serialnumber = subprocess.check_output("wmic bios get serialnumber",text=True,shell=True)
        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write("\n===== SERIAL NUMBER =====\n"+check_serialnumber)
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



###CHECK CMD###
checkIP()
checkHost()
checkMac()
checkSerial()
###CHECK OPCIONES DE WINDOWS###
checkAdmin()
checkRDP()
checkFirewall()
# APLICACION INSTALADA
check_app_instalada("Google Chrome")




