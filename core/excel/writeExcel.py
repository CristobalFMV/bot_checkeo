import time

from openpyxl import load_workbook
import checkeo
from ruta_excel import archivo_vicarius

archivo_vicarius = archivo_vicarius
wb = load_workbook(archivo_vicarius)
ws = wb.active
ip_local = checkeo.checkIP()
'''Parametros para el SQL'''
'''users,password,anexo,
                serial,mac,ubicacion,host,
                app_install1,firewall,app_install2,
                sistema_op, tipo_cpu,pantalla,huellero,
                ytb_premium, admin,remoto,
                observacion,nombre_soporte,fecha'''
#============================================
"""Objeto equipo que almacenara la información por equipo tomado"""
class Equipo:
    def __init__(self):
        self.ip = checkeo.checkIP()
        self.users = checkeo.checkCurrentUser()
        self.password = checkeo.pedirPassword()
        self.anexo = checkeo.pedirAnexo()
        self.serial = checkeo.checkSerial()
        self.mac = checkeo.checkMac()
        self.ubicacion = checkeo.pedirUbicacion()
        self.host = checkeo.checkHost()
        self.app_install1 = checkeo.check_app_instalada("Topia.exe")
        self.firewall = checkeo.checkFirewall()
        self.app_install2 = checkeo.check_app_instalada("Sophos UI.exe")
        self.sistema_op = (checkeo.checkOS())
        self.tipo_cpu = checkeo.checkTipoEquipo()
        self.pantalla = checkeo.checkScreen()
        self.huellero = checkeo.tieneHuellero()
        self.ytb_premium = checkeo.checkYTB()
        self.admin = checkeo.checkAdmin()
        self.remoto = checkeo.checkRDP()
        self.observacion = checkeo.checkObservaciones()
        self.nombre_soporte = checkeo.checkNombreSoporte()
        self.fecha = checkeo.checkFecha()

    def escribirExcel(ws, fila):
        try:
            ws[f"C{fila}"] = checkeo.checkCurrentUser()
            ws[f"D{fila}"] = checkeo.pedirPassword()
            time.sleep(1)
            ws[f"E{fila}"] = checkeo.pedirAnexo()
            time.sleep(1)
            ws[f"F{fila}"] = checkeo.checkSerial()
            ws[f"G{fila}"] = checkeo.checkMac()
            ws[f"H{fila}"] = checkeo.pedirUbicacion()
            time.sleep(1)
            ws[f"I{fila}"] = checkeo.checkHost()
            ws[f"J{fila}"] = checkeo.check_app_instalada("Topia.exe")
            ws[f"K{fila}"] = checkeo.checkFirewall()
            ws[f"L{fila}"] = checkeo.check_app_instalada("Sophos UI.exe")
            ws[f"M{fila}"] = checkeo.checkOS()
            ws[f"N{fila}"] = checkeo.checkTipoEquipo()
            ws[f"O{fila}"] = checkeo.checkScreen()
            ws[f"P{fila}"] = checkeo.tieneHuellero()
            ws[f"Q{fila}"] = checkeo.checkYTB()
            ws[f"R{fila}"] = checkeo.checkAdmin()
            ws[f"S{fila}"] = checkeo.checkRDP()
            ws[f"T{fila}"] = checkeo.checkObservaciones()
            ws[f"U{fila}"] = checkeo.checkNombreSoporte()
            ws[f"V{fila}"] = checkeo.checkFecha()

        except:
            msg = "Ha ocurrido un error durante la ejecución."
            print(msg)
        else:
            msg = "Proceso completado con éxito."
            print(msg)

#equipo = Equipo()
#datos = equipo.__dict__