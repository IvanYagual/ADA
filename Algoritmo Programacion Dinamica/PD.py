import numpy as np

# Datos
ancho = [4, 3, 8, 7, 2]
alto = [5, 7, 2, 1, 2]
n_estanterias = len(ancho)
pared = 8

# Crear la tabla de DP
# +1 en dimensiones para manejar el caso base donde no hay espacio o no hay estanterías
dp = np.zeros((n_estanterias + 1, pared + 1), dtype=int)

# Rellenar la tabla
for i in range(1, n_estanterias + 1):  # Iterar por cada estantería
    for m in range(1, pared + 1):      # Iterar por cada ancho de la pared
        # Caso 1: No usar la estantería i
        dp[i][m] = dp[i-1][m]
        
        # Caso 2: Usar la estantería en orientación horizontal
        if m >= ancho[i-1]:
            dp[i][m] = max(dp[i][m], 1 + dp[i-1][m - ancho[i-1]])
        
        # Caso 3: Usar la estantería en orientación vertical
        if m >= alto[i-1]:
            dp[i][m] = max(dp[i][m], 1 + dp[i-1][m - alto[i-1]])

# Resultado óptimo: número máximo de estanterías que caben en la pared
print("Máximo número de estanterías:", dp[n_estanterias][pared])
dp