import subprocess
import pyodbc
# NO debes importar id_reg directamente
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
# Función para obtener usuarios del sistema
def obtener_usuarios():
    resultado = subprocess.run(["net", "user"], capture_output=True, text=True, shell=True)
    salida = resultado.stdout

    lineas = salida.splitlines()
    usuarios = []
    capturando = False

    for linea in lineas:
        if "----------" in linea:
            capturando = not capturando
            continue
        if capturando and not linea.strip().startswith("Se ha completado"):
            usuarios += linea.split()

    return usuarios

# Función reutilizable para insertar usuarios
def insertar_usuarios_sql(usuarios, id_reg):
    conexion = pyodbc.connect(conn_str)
    cursor = conexion.cursor()

    for usuario in usuarios:
        cursor.execute("""
            INSERT INTO T_REG_SOPORTE_EXTERNO_USUARIO (ID_REG, USUARIO)
            VALUES (?, ?)
        """, (id_reg, usuario))

    conexion.commit()
    cursor.close()
    conexion.close()
