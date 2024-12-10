import numpy as np
from typing import Tuple, List, Any


def max_shelves_pd(wall_length: int, shelves: List[Tuple[int, int]]) -> tuple[list[int], int]:

    """
    Resuelve el problema de llenar la pared con estanterías utilizando programación dinámica.

    Args:
        wall_length: la longitud de la pared en metros
        shelves: una lista de tuplas, donde cada tupla contiene el ancho y el alto de una estantería

    Devuelve:
        Una tupla que contiene:
        - una lista indicando la orientación de cada estantería (0 = no usada, 1 = horizontal, 2 = vertical)
        - el número máximo de estanterías que caben en la pared
    """
    n_shelves = len(shelves)

    if wall_length <= 0 or n_shelves <= 0:
        return [], 0  # No hay estanterías válidas o la pared no tiene longitud

    # Inicializar la tabla de programación dinámica
    dp = np.zeros((n_shelves + 1, wall_length + 1), dtype=int)
    # en casos base (0,0), (0,j) y (i,0) es 0

    # Rellenar la tabla
    for i in range(1, n_shelves + 1):  # Iterar por cada estantería
        wi, hi = shelves[i - 1] # Dimensiones de la estantería (ancho y alto)
        for j in range(1, wall_length + 1):  # Iterar por cada ancho de la pared

            # Caso 1: No usar la estantería i
            dp[i][j] = dp[i - 1][j]

            # Caso 2: Usar la estantería en orientación horizontal
            if j >= wi:
                dp[i][j] = max(dp[i][j], 1 + dp[i - 1][j - wi])

            # Caso 3: Usar la estantería en orientación vertical
            if j >= hi:
                dp[i][j] = max(dp[i][j], 1 + dp[i - 1][j - hi])

    # Extraer la solución óptima desde la tabla
    placement = [None] * n_shelves # Lista para almacenar la orientación de cada estantería
    j = wall_length
    for i in range(n_shelves, 0, -1):
        wi, hi = shelves[i - 1]
        if dp[i][j] == dp[i - 1][j]:
            placement[i-1] = 0 # La estantería no se usa
        elif j >= wi and dp[i][j] == (dp[i-1][j - wi] + 1):
            placement[i-1] = 1 # La estantería se usa en orientación horizontal
            j -= wi
        elif j >= hi and dp[i][j] == (dp[i-1][j - hi] + 1):
            placement[i-1] = 2 # La estantería se usa en orientación vertical
            j -= hi


    return placement, dp[n_shelves][wall_length]


def show_results(placement, max_shelves, shelves, wall_length):
    """
            Función para mostrar los resultados del problema.
    """

    print(f"\n\tLongitud de la pared: {wall_length}")
    print(f"\t Total estanterías: {len(placement)}")
    print(f"Uso max de las estanterías: {max_shelves}")
    for i, p in enumerate(placement, start=1):
        orientation = "No usada" if p == 0 else f"Horizontal - {shelves[i - 1][0]}" \
            if p == 1 else f"Vertical - {shelves[i - 1][1]}"
        print(f"Estantería {i}: {orientation}")

def main():
    """
        Función principal para probar el problema de Ikrea.
    """
    shelves_1 = [(2, 3), (4, 1), (3, 2), (1, 5)]  # [(ancho, alto)]
    wall_length_1 = 5  # Longitud de la pared
    placement1, max_shelves1 = max_shelves_pd(wall_length_1, shelves_1)
    show_results(placement1, max_shelves1, shelves_1, wall_length_1)

    shelves_2 = [(4,5), (3,7), (8,2), (7,1), (2,2)]
    wall_length_2 = 8
    placement2, max_shelves2= max_shelves_pd(wall_length_2, shelves_2)
    show_results(placement2, max_shelves2, shelves_2, wall_length_2)

if __name__ == "__main__":
    main()