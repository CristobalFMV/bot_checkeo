import pyodbc

con = pyodbc.connect('DSN=SERVER_DEBUG;Trusted_Connection=yes;')

cursor = con.cursor()

# Datos a insertar
datos = (
    '192.168.1.10',       # ip
    'soporte01',          # users
    'pass123',            # password
    '1234',               # anexo
    'SN123456',           # serial
    'AA-BB-CC-DD-EE-FF',  # mac
    'Sala 1',             # ubicacion
    'HOST-PC',            # host
    'Google Chrome',      # app_install1
    'Activo',             # firewall
    'Topia',              # app_install2
    'Windows 10',         # sistema_op
    'Intel i5',           # tipo_cpu
    'Samsung 24"',        # pantalla
    'Sí',                 # huellero
    'No',                 # ytb_premium
    'Sí',                 # admin
    'Sí',                 # remoto
    'Sin observaciones',  # observacion
    'Cristóbal',          # nombre_soporte
    '2025-06-12'          # fecha
)

# Consulta de inserción (id se autogenera)
sql = '''
INSERT INTO equipos (
    ip, users, password, anexo, serial, mac, ubicacion, host,
    app_install1, firewall, app_install2, sistema_op, tipo_cpu,
    pantalla, huellero, ytb_premium, admin, remoto, observacion,
    nombre_soporte, fecha
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

cursor.execute(sql,datos)
con.commit()

print("Inserción correcta")
cursor.close()
con.close()