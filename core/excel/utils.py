def buscar_fila_por_ip(wb, hojas, ip_objetivo):
    """
    Busca la IP en todas las hojas y retorna la hoja y la fila donde se encontró.
    """
    for hoja in hojas:
        if hoja not in hojas:
            continue
        ws = wb[hoja]
        for fila in range(5, ws.max_row + 1):
            celda = ws[f"A{fila}"]
            if celda.value and str(celda.value).strip() == ip_objetivo:
                return ws, fila
    return None, None
