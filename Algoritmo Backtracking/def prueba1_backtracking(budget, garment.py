# def prueba1_backtracking(budget, garments, num_garments):
#     """
#     Backtracking optimizado con poda basada en presupuesto y condiciones.
#     También devuelve la combinación de prendas elegida.
#     """
#     nivel = 0  # Nivel actual en el árbol de decisión
#     s = [0] * num_garments  # Solución parcial (combinación actual)
#     hermanos_recorridos = [0] * num_garments  # Indica el índice del hermano visitado en cada nivel
#     total_gastado = 0  # Total acumulado
#     mejor_solucion = -1  # Mejor solución encontrada (máximo gasto sin exceder el presupuesto)
#     mejor_combinacion = []  # Lista para guardar la combinación que generó la mejor solución

#     while nivel >= 0:
#         # Si hemos llegado a un nivel sin hermanos por visitar
#         if hermanos_recorridos[nivel] >= len(garments[nivel]):
#             nivel -= 1  # Retrocedemos al nivel anterior
#             if nivel >= 0:
#                 total_gastado -= garments[nivel][hermanos_recorridos[nivel] - 1]
#             continue

#         # Exploramos el siguiente hermano en el nivel actual
#         precio_actual = garments[nivel][hermanos_recorridos[nivel]]
#         total_gastado += precio_actual

#         # Si el presupuesto se excede, podar esta rama
#         if total_gastado > budget:
#             total_gastado -= precio_actual
#             hermanos_recorridos[nivel] += 1
#             continue

#         # Avanzar al siguiente nivel
#         s[nivel] = precio_actual
#         hermanos_recorridos[nivel] += 1

#         # Si alcanzamos una solución válida
#         if nivel == num_garments - 1:
#             if total_gastado > mejor_solucion:  # Actualizamos si es una mejor solución
#                 mejor_solucion = total_gastado
#                 mejor_combinacion = s[:]
#             total_gastado -= precio_actual
#         else:
#             # Poda: Si no es posible completar el presupuesto, podar esta rama
#             min_cost_remaining = sum(min(garments[i]) for i in range(nivel + 1, num_garments))
#             if total_gastado + min_cost_remaining > budget:
#                 total_gastado -= precio_actual
#             else:
#                 nivel += 1
#                 hermanos_recorridos[nivel] = 0  # Inicializamos el nuevo nivel

#     return mejor_solucion, mejor_combinacion

# def read_cases_from_file(filename):
#     """
#     Lee el fichero en la ruta indicada en 'filename'.

#     Esta función toma una nombre de fichero 'filname' que contiene la ruta del fichero que se quiere leer.
#     Al abrir el fichero, lee linea por linea para obtener el número de casos, el presupuesto, el numero de prendas,
#     y los precios de los modelos de los modelos en cada caso. 

#     Parámetro:
#     filename (str): Cadena de texto que contiene la ruta del fichero.

#     Devuelve:
#     list of dict: Lista de diccionarios 'cases' con el presupuesto, número de prendas y los precios de cada prenda en cada caso.
#     """
#     cases = []

#     with open(filename, 'r') as file:
#         num_cases = int(file.readline().strip())  # Número de casos

#         for _ in range(num_cases):
#             # Lee el presupuesto y numero de tipos de prendas
#             budget, num_garments = map(int, file.readline().strip().split())

#             garments = []
#             # Lee los precios de las prendas para cada tipo.
#             for _ in range(num_garments):
#                 garment_prices = list(map(int, file.readline().strip().split()[1:]))
#                 garments.append(garment_prices)

#             #Añadir el caso al listado con el presupuesto, número de prendas y la matriz de precios
#             cases.append({'budget': budget, 'num_garments': num_garments, 'garments': garments})

#     return cases




# def main():


#     test_cases = [
#         ('901a (Copy).in', '901a.out')
#         # ('901b.in', '901b.out'),
#         # ('901c.in', '901c.out'),
#     ]

#     # Validación de los casos de prueba
#     for f_in, f_out in test_cases:

#         cases = read_cases_from_file(f_in)

#         solutions = []

#         for case in cases:
#             solution = prueba1_backtracking(case['budget'], case['garments'], case['num_garments'])
#             print(solution)
#         #     solutions.append(solution)
#         # correction, optimization = validation(f_out, solutions)
#         # print(f'Corrección para {f_in}: {correction:.0f}%, Optimización: {optimization:.2f}%')

#     # Fichero con casos grandes creado por la función: 'generar_fichero_entrada_progresivo' => create_files.py
#     time_test_cases = 'casos_grandes.in'
#     # garments = [
#     #     [9, 5, 8],  # Precios para la prenda 1
#     #     [7, 4, 6, 3, 5],  # Precios para la prenda 2
#     #     [1, 8, 3, 6, 8, 10]  # Precios para la prenda 3
#     # ]
#     # budget = 50
#     # num_garments = len(garments)

#     # # Ejecutar el algoritmo optimizado
#     # mejor_gasto, mejor_combinacion = prueba1_backtracking(budget, garments, num_garments)
#     # print(f"Máximo gasto dentro del presupuesto: {mejor_gasto}")
#     # print(f"Combinación elegida: {mejor_combinacion}")


# if __name__ == "__main__":
#     main()





# def prueba1_backtracking(budget, garments, num_garments):
#     """
#     Backtracking optimizado con poda basada en presupuesto y condiciones.
#     También devuelve la combinación de prendas elegida.
#     """
#     nivel = 0  # Nivel actual en el árbol de decisión
#     s = [0] * num_garments  # Solución parcial (combinación actual)
#     hermanos_recorridos = [0] * num_garments  # Indica el índice del hermano visitado en cada nivel
#     total_gastado = 0  # Total acumulado
#     mejor_solucion = -1  # Mejor solución encontrada (máximo gasto sin exceder el presupuesto)
#     mejor_combinacion = []  # Lista para guardar la combinación que generó la mejor solución

#     # Precomputar costos mínimos de cada prenda
#     min_costs = [min(g) for g in garments]
#     max_costs = [max(g) for g in garments]

#     # Función auxiliar para poda rápida
#     def poda_inefectiva(nivel, total_gastado):
#         """
#         Verifica si vale la pena continuar explorando desde el nivel actual.
#         """
#         min_cost_remaining = sum(min_costs[nivel:])  # Suma de mínimos desde este nivel
#         max_potencial = total_gastado + min_cost_remaining
#         return max_potencial <= mejor_solucion

#     while nivel >= 0:
#         # Si hemos llegado a un nivel sin hermanos por visitar
#         if hermanos_recorridos[nivel] >= len(garments[nivel]):
#             nivel -= 1  # Retrocedemos al nivel anterior
#             if nivel >= 0:
#                 total_gastado -= garments[nivel][hermanos_recorridos[nivel] - 1]
#             continue

#         # Exploramos el siguiente hermano en el nivel actual
#         precio_actual = garments[nivel][hermanos_recorridos[nivel]]
#         total_gastado += precio_actual

#         # Si el presupuesto se excede, podar esta rama
#         if total_gastado > budget:
#             total_gastado -= precio_actual
#             hermanos_recorridos[nivel] += 1
#             continue

#         # Avanzar al siguiente nivel
#         s[nivel] = precio_actual
#         hermanos_recorridos[nivel] += 1

#         # Si alcanzamos una solución válida
#         if nivel == num_garments - 1:
#             if total_gastado > mejor_solucion:  # Actualizamos si es una mejor solución
#                 mejor_solucion = total_gastado
#                 mejor_combinacion = s[:]
#             total_gastado -= precio_actual
#         else:
#             # Aplicar poda adicional
#             if poda_inefectiva(nivel + 1, total_gastado):
#                 total_gastado -= precio_actual
#             else:
#                 nivel += 1
#                 hermanos_recorridos[nivel] = 0  # Inicializamos el nuevo nivel

#     return mejor_solucion, mejor_combinacion


# def read_cases_from_file(filename):
#     """
#     Lee el fichero en la ruta indicada en 'filename'.

#     Esta función toma una nombre de fichero 'filname' que contiene la ruta del fichero que se quiere leer.
#     Al abrir el fichero, lee linea por linea para obtener el número de casos, el presupuesto, el numero de prendas,
#     y los precios de los modelos de los modelos en cada caso. 
#     """
#     cases = []

#     with open(filename, 'r') as file:
#         num_cases = int(file.readline().strip())  # Número de casos

#         for _ in range(num_cases):
#             # Lee el presupuesto y numero de tipos de prendas
#             budget, num_garments = map(int, file.readline().strip().split())

#             garments = []
#             # Lee los precios de las prendas para cada tipo.
#             for _ in range(num_garments):
#                 garment_prices = list(map(int, file.readline().strip().split()[1:]))
#                 garments.append(sorted(garment_prices, reverse=True))  # Orden descendente para mejorar poda

#             # Añadir el caso al listado con el presupuesto, número de prendas y la matriz de precios
#             cases.append({'budget': budget, 'num_garments': num_garments, 'garments': garments})

#     return cases


# def main():
#     test_cases = [
#         ('901a.in', '901a.out'),
#         #('901b.in', '901b.out'),
#         #('901c.in', '901c.out'),
#     ]

#     # Validación de los casos de prueba
#     for f_in, f_out in test_cases:
#         cases = read_cases_from_file(f_in)

#         for case in cases:
#             solution = prueba1_backtracking(case['budget'], case['garments'], case['num_garments'])
#             print(solution)


# if __name__ == "__main__":
#     main()











#PROGRAMACION DINAMICA
# def prueba1_dynamic_programming(budget, garments, num_garments):
#     """
#     Programación dinámica para encontrar la mejor combinación de prendas sin exceder el presupuesto.
#     """
#     # Inicializar la tabla DP con -1 (imposible de alcanzar)
#     dp = [[-1] * (budget + 1) for _ in range(num_garments + 1)]
#     dp[0][0] = 0  # Base case: 0 gasto con 0 prendas

#     for i in range(num_garments):
#         for g in garments[i]:
#             for b in range(budget - g, -1, -1):
#                 if dp[i][b] != -1:
#                     dp[i + 1][b + g] = max(dp[i + 1][b + g], dp[i][b] + g)

#     # Encontrar la mejor solución dentro del presupuesto
#     mejor_solucion = max(dp[num_garments])
#     return mejor_solucion if mejor_solucion != -1 else 0


# def read_cases_from_file(filename):
#     """
#     Lee el fichero en la ruta indicada en 'filename'.
#     """
#     cases = []

#     with open(filename, 'r') as file:
#         num_cases = int(file.readline().strip())  # Número de casos

#         for _ in range(num_cases):
#             budget, num_garments = map(int, file.readline().strip().split())

#             garments = []
#             for _ in range(num_garments):
#                 garment_prices = list(map(int, file.readline().strip().split()[1:]))
#                 garments.append(sorted(garment_prices, reverse=True))  # Orden descendente para mejorar poda

#             cases.append({'budget': budget, 'num_garments': num_garments, 'garments': garments})

#     return cases


# def main():
#     test_cases = [
#         ('901a.in', '901a.out'),
#         #('901b.in', '901b.out'),
#         #('901c.in', '901c.out'),
#     ]

#     for f_in, f_out in test_cases:
#         cases = read_cases_from_file(f_in)

#         for case in cases:
#             solution = prueba1_dynamic_programming(case['budget'], case['garments'], case['num_garments'])
#             print(f"Mejor gasto: {solution}")


# if __name__ == "__main__":
#     main()




def prueba1_backtracking(budget, garments, num_garments):
    """
    Backtracking optimizado con poda avanzada y técnicas voraces.
    """
    mejor_solucion = -1  # Mejor solución encontrada (máximo gasto sin exceder el presupuesto)
    mejor_combinacion = []

    # Precomputar costos mínimos y máximos de cada prenda
    min_costs = [min(g) for g in garments]

    # Ordenar los precios de las prendas en orden descendente para aplicar un algoritmo voraz
    for g in garments:
        g.sort(reverse=True)

    # Cache para poda
    cache = {}

    # Función auxiliar recursiva con cache para poda
    def backtrack(nivel, total_gastado):
        nonlocal mejor_solucion

        # Cachear la combinación actual
        estado = (nivel, total_gastado)
        if estado in cache and cache[estado] >= total_gastado:
            return
        cache[estado] = total_gastado

        # Si hemos alcanzado una solución válida
        if nivel == num_garments:
            if total_gastado <= budget:
                mejor_solucion = max(mejor_solucion, total_gastado)
            return

        # Aplicar poda adicional basada en el costo mínimo restante
        if total_gastado + sum(min_costs[nivel:]) > budget:
            return

        # Exploramos todos los modelos disponibles en el nivel actual
        for precio in garments[nivel]:
            nuevo_gasto = total_gastado + precio

            # Poda si el nuevo gasto excede el presupuesto
            if nuevo_gasto <= budget:
                backtrack(nivel + 1, nuevo_gasto)

    # Iniciar el backtracking desde el primer nivel (prenda) y con gasto total 0
    backtrack(0, 0)

    return mejor_solucion


def read_cases_from_file(filename):
    """
    Lee el fichero en la ruta indicada en 'filename'.
    """
    cases = []

    with open(filename, 'r') as file:
        num_cases = int(file.readline().strip())  # Número de casos

        for _ in range(num_cases):
            budget, num_garments = map(int, file.readline().strip().split())

            garments = []
            for _ in range(num_garments):
                garment_prices = list(map(int, file.readline().strip().split()[1:]))
                garments.append(garment_prices)

            cases.append({'budget': budget, 'num_garments': num_garments, 'garments': garments})

    return cases


def main():
    test_cases = [
        ('901a.in', '901a.out'),
        #('901b.in', '901b.out'),
        #('901c.in', '901c.out'),
    ]

    for f_in, f_out in test_cases:
        cases = read_cases_from_file(f_in)

        for case in cases:
            solution = prueba1_backtracking(case['budget'], case['garments'], case['num_garments'])
            print(f"Mejor gasto: {solution}")


if __name__ == "__main__":
    main()







