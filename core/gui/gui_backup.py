import socket
import sys
import customtkinter as ctk
from tkinter import messagebox
from openpyxl import load_workbook
from core.modules import checkeo as check
from core.excel.writeExcel import Equipo
from core.config.ruta_excel import archivo_vicarius
from core.excel.utils import buscar_fila_por_ip

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

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
    ip_entry.delete(0, "end")
    ip_entry.insert(0, ip)

def kill():
    root.destroy()
    sys.exit()

root = ctk.CTk()
root.resizable(False,False)
root.geometry("400x420")
root.title("Formulario de Auditoría - Robot Inspector")

frame = ctk.CTkFrame(master=root, corner_radius=10)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Widgets con customtkinter
ctk.CTkLabel(frame, text="IP del equipo:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
ip_entry = ctk.CTkEntry(frame, width=200)
ip_entry.grid(row=0, column=1, pady=5)
ip_entry.insert(0, obtener_ip_local())

ctk.CTkLabel(frame, text="Anexo:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
anexo_entry = ctk.CTkEntry(frame, width=200)
anexo_entry.grid(row=1, column=1, pady=5)

ctk.CTkLabel(frame, text="Ubicación:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
ubicacion_entry = ctk.CTkEntry(frame, width=200)
ubicacion_entry.grid(row=2, column=1, pady=5)

ctk.CTkLabel(frame, text="¿Tiene huellero?").grid(row=3, column=0, sticky="w", pady=5, padx=5)
huellero_combo = ctk.CTkComboBox(frame, values=["Sí", "No"], width=200)
huellero_combo.grid(row=3, column=1, pady=5)
huellero_combo.set("Sí")

ctk.CTkLabel(frame, text="Soporte técnico:").grid(row=4, column=0, sticky="w", pady=5, padx=5)
soporte_entry = ctk.CTkEntry(frame, width=200)
soporte_entry.grid(row=4, column=1, pady=5)

ctk.CTkLabel(frame, text="Observaciones:").grid(row=5, column=0, sticky="w", pady=5, padx=5)
observacion_entry = ctk.CTkEntry(frame, width=200)
observacion_entry.grid(row=5, column=1, pady=5)

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
        serial=check.checkSerial(),
        mac=check.checkMac(),
        ubicacion=ubicacion,
        host=check.checkHost(),
        app_install1=check.check_ruta_topia(),
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
ctk.CTkButton(frame, text="Actualizar IP", command=actualizar_ip).grid(row=6, column=0, pady=10, padx=9)
ctk.CTkButton(frame, text="Procesar", command=procesar_datos).grid(row=6, column=1, pady=10, padx=9)
ctk.CTkButton(frame, text="Salir", command=kill).grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
