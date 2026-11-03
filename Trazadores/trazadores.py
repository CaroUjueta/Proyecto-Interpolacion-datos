"""
Proyecto Final - Análisis Numérico (Pontificia Universidad Javeriana)
Interpolación por Trazadores Cúbicos Naturales

Este archivo contiene el algoritmo completo para la construcción y evaluación
de trazadores cúbicos (Cubic Splines) con condiciones de frontera naturales.

Algoritmo: Algoritmo 3.4 (Burden & Faires) - Natural Cubic Spline.
Condiciones de frontera naturales: S''(x_0) = 0 y S''(x_n) = 0.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from datos import cargar_datos

# ---------------------------------------------------------------------------
# 1. ALGORITMO DE TRAZADOR CÚBICO
# ---------------------------------------------------------------------------

def construir_trazador_cubico_natural(nodos, valores):
    """
    Construye los coeficientes a_i, b_i, c_i, d_i de cada tramo polinomial S_i(x)
    para un trazador cúbico natural (S''(x_0) = S''(x_n) = 0).

    Parámetros:
        nodos (list/tuple): Lista de valores x_0, x_1, ..., x_n ordenados.
        valores (list/tuple): Lista de valores y_0, y_1, ..., y_n correspondientes.

    Retorna:
        x (list): Nodos ordenados.
        a (list): Coeficientes constantes a_i = y_i para i = 0,...,n-1.
        b (list): Coeficientes lineales b_i para i = 0,...,n-1.
        c (list): Coeficientes cuadráticos c_i para i = 0,...,n-1.
        d (list): Coeficientes cúbicos d_i para i = 0,...,n-1.
    """
    # Ordenar nodos y valores por si no vienen ordenados secuencialmente
    puntos = sorted(zip(nodos, valores))
    x = [float(p[0]) for p in puntos]
    a = [float(p[1]) for p in puntos]
    n = len(x) - 1

    if n < 1:
        raise ValueError("Se requieren al menos 2 puntos para interpolar.")

    # Paso 0: Espaciamiento entre nodos adyacentes h_i
    h = [x[i + 1] - x[i] for i in range(n)]

    # Paso 1: Vector alpha para el sistema de ecuaciones tridiagonal
    alpha = [0.0] * (n + 1)
    for i in range(1, n):
        alpha[i] = (3.0 / h[i]) * (a[i + 1] - a[i]) - (3.0 / h[i - 1]) * (a[i] - a[i - 1])

    # Paso 2 y 3: Factorización Crout / Algoritmo de Thomas para sistema tridiagonal
    l = [1.0] + [0.0] * n
    mu = [0.0] * (n + 1)
    z = [0.0] * (n + 1)

    for i in range(1, n):
        l[i] = 2.0 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

    # Paso 4: Condiciones de frontera naturales (c_0 = 0, c_n = 0)
    l[n] = 1.0
    z[n] = 0.0
    c = [0.0] * (n + 1)

    # Paso 5: Sustitución hacia atrás para obtener los coeficientes b_j, c_j, d_j
    b = [0.0] * n
    d = [0.0] * n

    for j in range(n - 1, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (a[j + 1] - a[j]) / h[j] - h[j] * (c[j + 1] + 2.0 * c[j]) / 3.0
        d[j] = (c[j + 1] - c[j]) / (3.0 * h[j])

    return x, a[:n], b, c[:n], d


def evaluar_trazador(x_eval, x, a, b, c, d):
    """
    Evalúa el trazador cúbico en un punto x_eval usando las piezas polinomiales:
        S_j(x) = a_j + b_j*(x - x_j) + c_j*(x - x_j)^2 + d_j*(x - x_j)^3

    Parámetros:
        x_eval (float): Punto donde se desea aproximar.
        x (list): Nodos ordenados x_0, ..., x_n.
        a, b, c, d (list): Coeficientes obtenidos de construir_trazador_cubico_natural.

    Retorna:
        float: Valor interpolado S(x_eval).
    """
    n = len(b)

    # Selección del tramo polinomial j
    if x_eval <= x[0]:
        j = 0
    elif x_eval >= x[-1]:
        j = n - 1
    else:
        # Búsqueda del subintervalo [x_j, x_{j+1}]
        j = 0
        for i in range(n):
            if x[i] <= x_eval <= x[i + 1]:
                j = i
                break

    dx = x_eval - x[j]
    return a[j] + b[j] * dx + c[j] * (dx ** 2) + d[j] * (dx ** 3)


def trazador_cubico(x_eval, nodos, valores):
    """
    Función envolvente (wrapper) equivalente a la función `lagrange(x, nodos, valores)`.
    Construye y evalúa el trazador cúbico natural en una sola llamada.
    """
    x_nodos, a, b, c, d = construir_trazador_cubico_natural(nodos, valores)
    return evaluar_trazador(x_eval, x_nodos, a, b, c, d)


def error_relativo(exacto, aprox):
    """Calcula el error relativo entre el valor exacto y el valor aproximado."""
    return abs(exacto - aprox) / abs(exacto)


# ---------------------------------------------------------------------------
# 2. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    nodos, valores, resaltados, exactos_res = cargar_datos()

    # Construcción previa del trazador cúbico para reutilizar coeficientes
    x_nodos, a, b, c, d = construir_trazador_cubico_natural(nodos, valores)

    print(f"Trazador Cúbico Natural con {len(nodos)} nodos ({len(b)} tramos polinomiales)\n")
    print(f"{'Año':>6} {'Exacto':>14} {'Trazador Cúbico':>18} {'Error relativo':>20}")
    print("-" * 62)

    for anio_res, exacto in zip(resaltados, exactos_res):
        aprox = evaluar_trazador(anio_res, x_nodos, a, b, c, d)
        err = error_relativo(exacto, aprox)
        print(f"{anio_res:>6} {exacto:>14,.0f} {aprox:>18,.2f} {err:>20.10f}")


if __name__ == "__main__":
    main()
