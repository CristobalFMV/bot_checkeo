import tkinter as tk
import socket
import sys
from tkinter import messagebox, ttk
from openpyxl import load_workbook
from core.modules import checkeo as check
from core.excel.writeExcel import Equipo
from core.config.ruta_excel import archivo_vicarius
from core.excel.utils import buscar_fila_por_ip

# Función para obtener la IP local
def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "No se pudo obtener la IP"

def actualizar_ip():
    ip = obtener_ip_local()
    ip_entry.delete(0, tk.END)
    ip_entry.insert(0, ip)

# Ventana principal
root = tk.Tk()
root.geometry("400x350")
root.title("Formulario de Auditoría - Robot Inspector")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Campos de entrada
tk.Label(frame, text="IP del equipo:").grid(row=0, column=0, sticky="e")
ip_entry = tk.Entry(frame, width=30)
ip_entry.grid(row=0, column=1)
ip_entry.insert(0, obtener_ip_local())

tk.Label(frame, text="Anexo:").grid(row=2, column=0, sticky="e")
anexo_entry = tk.Entry(frame, width=30)
anexo_entry.grid(row=2, column=1)

tk.Label(frame, text="Ubicación:").grid(row=3, column=0, sticky="e")
ubicacion_entry = tk.Entry(frame, width=30)
ubicacion_entry.grid(row=3, column=1)

tk.Label(frame, text="¿Tiene huellero?").grid(row=4, column=0, sticky="e")
huellero_var = tk.StringVar()
huellero_combo = ttk.Combobox(frame, width=27, textvariable=huellero_var, state="readonly")
huellero_combo['values'] = ("Sí", "No")
huellero_combo.grid(row=4, column=1)
huellero_combo.current(0)

tk.Label(frame, text="Soporte técnico:").grid(row=5, column=0, sticky="e")
soporte_entry = tk.Entry(frame, width=30)
soporte_entry.grid(row=5, column=1)

tk.Label(frame, text="Observaciones:").grid(row=6, column=0, sticky="e")
observacion_entry = tk.Entry(frame, width=30)
observacion_entry.grid(row=6, column=1)


# Función para procesar y guardar
def procesar_datos():
    ip = ip_entry.get().strip()
    anexo = anexo_entry.get().strip()
    ubicacion = ubicacion_entry.get().strip()
    huellero = huellero_combo.get()
    soporte = soporte_entry.get().strip()
    observacion = observacion_entry.get().strip()

    if not ip or not anexo or not ubicacion or not soporte:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos requeridos.")
        return
    root.update_idletasks()
    equipo = Equipo(
        ip=ip,
        usuario=check.checkCurrentUser(),
        anexo=anexo,
        serial=check.check_serial(),
        mac=check.checkMac(),
        ubicacion=ubicacion,
        host=check.checkHost(),
        app_install1=check.check_app_instalada("Topia.exe"),
        firewall=check.obtener_estado_firewall(),
        app_install2=check.check_ruta_sofos(),
        sistema_op=check.checkOS(),
        tipo_cpu=check.checkTipoEquipo(),
        pantalla=check.checkScreen(),
        huellero=huellero,
        ytb_premium=check.checkYTB(),
        admin=check.checkAdmin(),
        remoto=check.checkRDP(),
        observacion=observacion,
        nombre_soporte=soporte,
        fecha=check.checkFecha()
    )

    try:
        wb = load_workbook(archivo_vicarius)
        hojas = ['10.1.2.', 'HALLAZGOS ', '10.1.3.', ' 10.1.4.', '10.1.5.', '10.1.7.',
                 '10.1.10.', '10.1.11.', ' 10.1.12.', ' 10.1.13.', '10.1.15.', '10.1.16',
                 '10.1.20.1', '10.1.18.1', '10.1.21.1', '192.1.1.0', ' 168.88.162.',
                 '168.88.164.1', '168.88.165.1']

        ws, fila = buscar_fila_por_ip(wb, hojas, equipo.ip)

        if ws and fila:
            equipo.escribir_en_excel(ws, fila)
            wb.save(archivo_vicarius)
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        else:
            messagebox.showerror("No encontrado", "No se encontró la IP en ninguna hoja.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
    finally:
        root.update_idletasks()

# Botones
tk.Button(frame, text="Actualizar IP", command=actualizar_ip).grid(row=7, column=0, pady=10)
tk.Button(frame, text="Procesar", command=procesar_datos).grid(row=7, column=1, pady=10)
tk.Button(frame, text="Salir", command=lambda: (root.destroy(), sys.exit())).grid(row=9, column=0, columnspan=2, pady=5)
root.mainloop()
