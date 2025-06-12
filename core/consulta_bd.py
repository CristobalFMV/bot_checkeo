import sqlite3

def ver_equipos_bd():
    conn = sqlite3.connect("equipos_hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipos")
    filas = cursor.fetchall()

    for f in filas:
        print(f)
    conn.close()

if __name__ == '__main__':
    ver_equipos_bd()