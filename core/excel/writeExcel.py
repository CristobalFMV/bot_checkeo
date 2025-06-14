from openpyxl import load_workbook
from core.gui import checkeo
from core.config.ruta_excel import archivo_vicarius
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
    def __init__(
        self,
        ip,
        usuario,
        anexo,
        serial,
        mac,
        ubicacion,
        host,
        app_install1,
        firewall,
        app_install2,
        sistema_op,
        tipo_cpu,
        pantalla,
        huellero,
        ytb_premium,
        admin,
        remoto,
        observacion,
        nombre_soporte,
        fecha,
        id=None,
    ):
        self.id = id
        self.ip = ip
        self.users = usuario
        self.anexo = anexo
        self.serial = serial
        self.mac = mac
        self.ubicacion = ubicacion
        self.host = host
        self.app_install1 = app_install1
        self.firewall = firewall
        self.app_install2 = app_install2
        self.sistema_op = sistema_op
        self.tipo_cpu = tipo_cpu
        self.pantalla = pantalla
        self.huellero = huellero
        self.ytb_premium = ytb_premium
        self.admin = admin
        self.remoto = remoto
        self.observacion = observacion
        self.nombre_soporte = nombre_soporte
        self.fecha = fecha

    def escribir_en_excel(self, ws, fila):
        try:
            ws[f"C{fila}"] = self.users
            ws[f"E{fila}"] = self.anexo
            ws[f"F{fila}"] = self.serial
            ws[f"G{fila}"] = self.mac
            ws[f"H{fila}"] = self.ubicacion
            ws[f"I{fila}"] = self.host
            ws[f"J{fila}"] = self.app_install1
            ws[f"K{fila}"] = self.firewall
            ws[f"L{fila}"] = self.app_install2
            ws[f"M{fila}"] = self.sistema_op
            ws[f"N{fila}"] = self.tipo_cpu
            ws[f"O{fila}"] = self.pantalla
            ws[f"P{fila}"] = self.huellero
            ws[f"Q{fila}"] = self.ytb_premium
            ws[f"R{fila}"] = self.admin
            ws[f"S{fila}"] = self.remoto
            ws[f"T{fila}"] = self.observacion
            ws[f"U{fila}"] = self.nombre_soporte
            ws[f"V{fila}"] = self.fecha
        except Exception as e:
            print("❌ Error durante la escritura en Excel:", e)
        else:
            print("✅ Proceso completado con éxito.")

#equipo = Equipo()
#datos = equipo.__dict__