import sqlite3
import writeExcel as equipoExcel


""" 
Se utiliza .cursor() para crear consultas SQL a través del subcomando .execute()
"""


def crear_bd():
    conn = sqlite3.connect("equipos_hospital.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT UNIQUE,
            users TEXT,
            password TEXT,
            anexo TEXT,
            serial TEXT,
            mac TEXT,
            ubicacion TEXT,
            host TEXT,
            app_install1 TEXT,
            firewall TEXT,
            app_install2 TEXT,
            sistema_op TEXT,
            tipo_cpu TEXT,
            pantalla TEXT,
            huellero TEXT,
            ytb_premium TEXT,
            admin TEXT,
            remoto TEXT,
            observacion TEXT,
            nombre_soporte TEXT,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_en_bd(equipo):
    conn = sqlite3.connect("equipos_hospital.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT OR REPLACE INTO equipos (
                ip, users, password, anexo, serial, mac, ubicacion, host,
                app_install1, firewall, app_install2, sistema_op, tipo_cpu,
                pantalla, huellero, ytb_premium, admin, remoto,
                observacion, nombre_soporte, fecha
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        equipo.ip,
        equipo.users,
        equipo.password,
        equipo.anexo,
        equipo.serial,
        equipo.mac,
        equipo.ubicacion,
        equipo.host,
        equipo.app_install1,
        equipo.firewall,
        equipo.app_install2,
        equipo.sistema_op,
        equipo.tipo_cpu,
        equipo.pantalla,
        equipo.huellero,
        equipo.ytb_premium,
        equipo.admin,
        equipo.remoto,
        equipo.observacion,
        equipo.nombre_soporte,
        equipo.fecha
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_bd()
    equipo = equipoExcel.Equipo()
    guardar_en_bd(equipo)
    print("GUARDADO CORRECTAMENTE EN BD!")

