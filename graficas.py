"""
Gráficas del proyecto - Población de UCRANIA (1994-2023)

Uso:  python graficas.py
Guarda los PNG en la carpeta graficas/ y los muestra en pantalla.
Dependencias: openpyxl y matplotlib.

Secciones:
  - Lagrange   (listo)
  - Trazadores (pendiente: agregar sus funciones y llamarlas en main())
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SALIDA = RAIZ / "graficas"
sys.path.append(str(RAIZ))
sys.path.append(str(RAIZ / "Lagrange"))

import matplotlib.pyplot as plt

from datos import cargar_datos
from lagrange import error_relativo, lagrange

# ---------------------------------------------------------------------------
# Datos compartidos
# ---------------------------------------------------------------------------
nodos, valores, resaltados, exactos_res = cargar_datos()
todos = sorted(zip(nodos + resaltados, valores + exactos_res))
años = [a for a, _ in todos]
poblacion = [p for _, p in todos]


def dibujar_puntos(ax, aprox_res):
    """Datos, nodos y años resaltados (aproximado vs exacto)."""
    ax.plot(años, poblacion, "k.", ms=4, label="Datos exactos")
    ax.plot(nodos, valores, "go", ms=5, label=f"Nodos usados ({len(nodos)})")
    ax.plot(resaltados, aprox_res, "r^", ms=8, label="Aproximación (años resaltados)")
    ax.plot(resaltados, exactos_res, "rx", ms=9, label="Valor exacto (años resaltados)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Población")
    ax.grid(alpha=0.3)


def grafica_errores(errores, titulo, archivo):
    """Barras del error relativo por año resaltado."""
    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar([str(a) for a in resaltados], errores, color="tab:red")
    ax.set_xlabel("Año resaltado")
    ax.set_ylabel("Error relativo")
    ax.set_title(titulo)
    ax.grid(alpha=0.3, axis="y")
    for b, e in zip(barras, errores):
        ax.annotate(f"{e:,.6f}", (b.get_x() + b.get_width() / 2, e),
                    ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(SALIDA / archivo, dpi=150)


# ---------------------------------------------------------------------------
# LAGRANGE
# ---------------------------------------------------------------------------
def graficas_lagrange():
    grado = len(nodos) - 1
    aprox = [lagrange(a, nodos, valores) for a in resaltados]
    errores = [error_relativo(e, p) for e, p in zip(exactos_res, aprox)]

    def curva(a, b, pasos=600):
        xs = [a + (b - a) * i / pasos for i in range(pasos + 1)]
        return xs, [lagrange(x, nodos, valores) for x in xs]

    # 1. Curva completa: muestra cómo se dispara en 1994 y 2023
    fig, ax = plt.subplots(figsize=(8, 5))
    xs, ys = curva(min(años), max(años))
    ax.plot(xs, ys, label=f"Polinomio de Lagrange (grado {grado})")
    dibujar_puntos(ax, aprox)
    ax.set_title("Lagrange - curva completa (se dispara en 1994 y 2023)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(SALIDA / "lagrange_curva_completa.png", dpi=150)

    # 2. Zoom al rango de los nodos y a los valores de los datos
    fig, ax = plt.subplots(figsize=(8, 5))
    xs, ys = curva(min(nodos), max(nodos))
    ax.plot(xs, ys, label=f"Polinomio de Lagrange (grado {grado})")
    dibujar_puntos(ax, aprox)
    ax.set_xlim(min(nodos) - 1, max(nodos) + 1)
    ax.set_ylim(min(poblacion) * 0.97, max(poblacion) * 1.02)
    ax.set_title("Lagrange - zoom al rango de los nodos (1995-2022)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(SALIDA / "lagrange_zoom.png", dpi=150)

    # 3. Error relativo por año
    grafica_errores(errores, "Lagrange - error relativo por año",
                    "lagrange_errores.png")


# ---------------------------------------------------------------------------
# TRAZADORES  (pendiente)
# ---------------------------------------------------------------------------
# def graficas_trazadores():
#     ...  usar dibujar_puntos() y grafica_errores() igual que en Lagrange


if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    graficas_lagrange()
    # graficas_trazadores()
    print("Gráficas guardadas en", SALIDA)
    plt.show()
