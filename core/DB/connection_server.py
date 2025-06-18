import pyodbc
from core.gui.users import obtener_usuarios, insertar_usuarios_sql
from core.DB.consulta_bd import equipo
# Cambia estos valores según tu entorno
driver = 'ODBC Driver 17 for SQL Server'
server = '168.88.162.66'
database = 'DB_INFORMATICA'
username = 'soporte_ext'
password = 'Soporte1234567'

# Cadena de conexión completa
conn_str = f'''
DRIVER={{{driver}}};
SERVER={server};
DATABASE={database};
UID={username};
PWD={password};
'''
def convertir_a_bit(valor):
    if isinstance(valor, str):
        return 1 if valor.strip().lower() in ['sí', 'si', 'yes', 'true', '1'] else 0
    return int(bool(valor))

def guardar_en_bd(equipo):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO T_REG_SOPORTE_EXTERNO (
            IP_EQUIPO, N_SERIE, MAC, HOSTNAME, SISTEMA_OPERATIVO, TIPO_CPU,
            PULGADAS_PANTALLA, ANEXO_USUARIO, UBICACION, CTA_ADMINISTRADOR,
            PING_YOUTUBE, APP_SOFOS, APP_VICARIUS, HUELLERO, FIREWALL_WINDOWS,
            ESCRITORIO_REMOT, OBSERVACIONES, USER_REGISTRA
        ) OUTPUT INSERTED.ID_REG
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        equipo.ip,
        equipo.serial,
        equipo.mac,
        equipo.host,
        equipo.sistema_op,
        equipo.tipo_cpu,
        equipo.pantalla,
        equipo.anexo,
        equipo.ubicacion,
        convertir_a_bit(equipo.admin),
        convertir_a_bit(equipo.ytb_premium),
        convertir_a_bit(equipo.app_install1),
        convertir_a_bit(equipo.app_install2),
        convertir_a_bit(equipo.huellero),
        convertir_a_bit(equipo.firewall),
        convertir_a_bit(equipo.remoto),
        equipo.observacion,
        equipo.users,
    ))
    id_reg = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_reg

# --- USO ---
id_reg = guardar_en_bd(equipo)
usuarios = obtener_usuarios()
insertar_usuarios_sql(usuarios, id_reg)
print(f"Equipo registrado con ID_REG {id_reg} y {len(usuarios)} usuarios insertados.")
