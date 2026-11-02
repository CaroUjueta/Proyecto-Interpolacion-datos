"""
Proyecto Final - Análisis Numérico (Pontificia Universidad Javeriana)
Interpolación de Lagrange - Población de UCRANIA (1994-2023)
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from datos import cargar_datos

# ---------------------------------------------------------------------------
# 1. ALGORITMO DE LAGRANGE
# ---------------------------------------------------------------------------
def base_lagrange(x, nodos, k):
    """L_k(x) = prod_{j != k} (x - x_j) / (x_k - x_j)"""
    L = 1.0
    for j, xj in enumerate(nodos):
        if j != k:
            L *= (x - xj) / (nodos[k] - xj)
    return L


def lagrange(x, nodos, valores):
    """P(x) = sum_k y_k * L_k(x), con todos los nodos dados."""
    return sum(valores[k] * base_lagrange(x, nodos, k)
               for k in range(len(nodos)))


def error_relativo(exacto, aprox):
    return abs(exacto - aprox) / abs(exacto)


# ---------------------------------------------------------------------------
# 2. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def main():
    # Nodos: filas sin color. Resaltadas: las que se deben aproximar.
    nodos, valores, resaltados, exactos_res = cargar_datos()

    print(f"Polinomio de Lagrange de grado {len(nodos) - 1} "
          f"con {len(nodos)} nodos\n")
    print(f"{'Año':>6} {'Exacto':>14} {'Lagrange':>18} {'Error relativo':>20}")
    print("-" * 62)
    for a, ex in zip(resaltados, exactos_res):
        p = lagrange(a, nodos, valores)
        print(f"{a:>6} {ex:>14,.0f} {p:>18,.2f} {error_relativo(ex, p):>20.10f}")


if __name__ == "__main__":
    main()
