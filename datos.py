from pathlib import Path

import openpyxl

EXCEL = Path(__file__).parent / "ANUM - Proyecto Final.xlsx"


def cargar_datos(ruta=EXCEL):
    """Lee Año (col B) y Población (col C) de la hoja activa.

    Devuelve (x, y, x_resaltados, y_resaltados):
      - x, y: filas SIN color de relleno (las que se usan para interpolar)
      - x_resaltados, y_resaltados: filas con color (las que se ignoran)
    """
    ws = openpyxl.load_workbook(ruta).active
    x, y, xr, yr = [], [], [], []
    for fila in range(2, ws.max_row + 1):
        anio, pob = ws.cell(fila, 2), ws.cell(fila, 3)
        if anio.value is None or pob.value is None:
            continue
        if anio.fill.fill_type == "solid":  # celda con color -> ignorar
            xr.append(anio.value)
            yr.append(pob.value)
        else:
            x.append(anio.value)
            y.append(pob.value)
    return x, y, xr, yr


if __name__ == "__main__":
    x, y, xr, yr = cargar_datos()
    print(len(x), "puntos para interpolar; ignorados:", xr)
