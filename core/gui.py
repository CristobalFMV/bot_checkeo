import tkinter as tk
import socket
from tkinter import messagebox
import checkeo as check
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

# Función para actualizar el campo de IP manualmente
def actualizar_ip():
    ip = obtener_ip_local()
    ip_entry.delete(0, tk.END)
    ip_entry.insert(0, ip)

# Crear ventana principal
root = tk.Tk()
root.geometry("400x300")
root.title("Formulario de Auditoría - Robot Inspector")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Campos de entrada
tk.Label(frame, text="IP del equipo:").grid(row=0, column=0, sticky="e")
ip_entry = tk.Entry(frame, width=30)
ip_entry.grid(row=0, column=1)
ip_entry.insert(0, obtener_ip_local())

tk.Label(frame, text="Contraseña del equipo:").grid(row=1, column=0, sticky="e")
contrasena_entry = tk.Entry(frame, width=30, show="*")
contrasena_entry.grid(row=1, column=1)

tk.Label(frame, text="Anexo:").grid(row=2, column=0, sticky="e")
anexo_entry = tk.Entry(frame, width=30)
anexo_entry.grid(row=2, column=1)

tk.Label(frame, text="Ubicación:").grid(row=3, column=0, sticky="e")
ubicacion_entry = tk.Entry(frame, width=30)
ubicacion_entry.grid(row=3, column=1)

tk.Label(frame, text="¿Tiene huellero?:").grid(row=4, column=0, sticky="e")
huellero_entry = tk.Entry(frame, width=30)
huellero_entry.grid(row=4, column=1)

# Función para procesar los datos
def procesar_datos():
    ip = ip_entry.get().strip()
    contrasena = contrasena_entry.get().strip()
    anexo = anexo_entry.get().strip()
    ubicacion = ubicacion_entry.get().strip()
    huellero = huellero_entry.get().strip()

    if not ip or not contrasena or not anexo or not ubicacion or not huellero:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos antes de continuar.")
        return

# Botones
tk.Button(frame, text="Procesar", command=procesar_datos).grid(row=6, column=0, pady=10)
tk.Button(frame, text="Salir", command=root.destroy).grid(row=6, column=1, pady=10)
tk.Button(frame, text="Actualizar IP", command=actualizar_ip).grid(row=5, column=1, sticky="e")

root.mainloop()
