from openpyxl import load_workbook

def escribir_datos_en_excel(ruta_excel, datos, ip_local):
    # Abrir el archivo Excel
    wb = load_workbook(ruta_excel)

    for hoja in wb.sheetnames:
        ws = wb[hoja]

        # Buscar la IP en la columna A, desde la fila 5
        for row in ws.iter_rows(min_row=5, min_col=1, max_col=1):
            celda_ip = row[0]
            if celda_ip.value and str(celda_ip.value).strip() == ip_local:
                fila = celda_ip.row

                # Escribir datos en columnas específicas
                if 'usuario' in datos:
                    ws[f'C{fila}'] = datos['usuario']
                if 'serial' in datos:
                    ws[f'F{fila}'] = datos['serial']
                if 'mac' in datos:
                    ws[f'G{fila}'] = datos['mac']
                if 'hostname' in datos:
                    ws[f'I{fila}'] = datos['hostname']
                if 'topia' in datos:
                    ws[f'J{fila}'] = "Sí" if datos['topia'] else "No"
                if 'firewall' in datos:
                    ws[f'K{fila}'] = "Activo" if datos['firewall'] else "Inactivo"
                if 'tipo_equipo' in datos:
                    ws[f'N{fila}'] = datos['tipo_equipo']
                if 'youtube' in datos:
                    ws[f'Q{fila}'] = "Sí" if datos['youtube'] else "No"
                if 'admin' in datos:
                    ws[f'R{fila}'] = "Sí" if datos['admin'] else "No"
                if 'rdp' in datos:
                    ws[f'S{fila}'] = "Sí" if datos['rdp'] else "No"

                break  # Deja de buscar en esta hoja

    # Guardar cambios
    wb.save(ruta_excel)
    wb.close()
