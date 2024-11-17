import time
import numpy as np
import matplotlib.pyplot as plt

def validation(out_file, backtracking_solution):
    """
    Compara las salidas de 'out_file' con 'greedy_solution' para calcular la precisión.

    Esta función toma el archivo 'out_file' con las soluciones esperadas y compara con las soluciones
    de 'greedy_solution' para calcular la precisión en porcentaje.

    Parámetros:
    out_file (str): Ruta del fichero con las soluciones esperadas.
    greedy_solution (list): Lista de modelos seleccionados por el algoritmo.

    Devuelve:
    float: Corrección - porcentaje de casos calculados correctamente según la solución proporcionada.
    float: Optimización - porcentaje de coincidencia de las soluciones con la calidad esperada.
    """
    backtracking_solution = [0 if backsol == -1 else backsol for backsol in backtracking_solution]

    # Leer soluciones esperadas desde el archivo
    with open(out_file, 'r') as out_file:
        actual_solutions = [
            0 if line.strip() == 'no solution' else int(line.strip())
            for line in out_file
        ]

    # Comprueba si el número de soluciones recibidas es igual al de las soluciones esperadas
    if len(actual_solutions) != len(backtracking_solution):
        raise ValueError("The number of provided solutions does not equal the number of actual solutions.")

    correct_count = 0
    optimization_count = 0
    optimization_number = 0
    for i in range(len(actual_solutions)):

        if actual_solutions[i] == 0:
            if backtracking_solution[i] == 0:
                correct_count += 1
        else:
            if backtracking_solution[i] != 0:
                correct_count += 1
                optimization_count+=1
                optimization_number += backtracking_solution[i] / actual_solutions[i]

    optimization_pr = optimization_number / optimization_count * 100

    correction_pr = correct_count / len(backtracking_solution) * 100

    return correction_pr, optimization_pr


def time_test(test_file):
    """
    Realiza pruebas de tiempo sobre los casos de prueba en el archivo 'test_file'.

    Parámetros:
    test_file (str): Ruta del archivo con los casos de prueba.

    Devuelve:
    tuple: Lista con los tiempos de ejecución y los tamaños de los casos.
    """

    # Lee los casos de prueba desde el archivo
    cases = read_cases_from_file(test_file)

    times = []  # Lista para almacenar los tiempos de ejecución
    sizes = []  # Lista para almacenar los tamaños de los casos

    # Ejecuta la selección backtracking para cada caso y mide el tiempo de ejecución
    for case in cases:
        budget, garments, n_garments = case['budget'], case['garments'], case['num_garments']

        # Calcula el tamaño como presupuesto * número de prendas
        size = budget * n_garments

        start_time = time.time()
        prueba1_backtracking(budget, garments, n_garments)
        end_time = time.time()

        # Almacena el tiempo de ejecución y el tamaño del caso
        times.append(end_time - start_time)
        sizes.append(size)  # Se usa el tamaño calculado

    # Devuelve una tupla con los tiempos y tamaños de los casos
    return times, sizes


def plot_results(times, sizes):
    """
    Genera un gráfico que muestra la relación entre los tiempos de ejecución y los tamaños de los casos.

    Parámetros:
    times (list): Lista de los tiempos de ejecución de los casos de prueba.
    sizes (list): Lista de los tamaños de los casos de prueba.
    """

    # Configura el tamaño de la figura del gráfico
    plt.figure(figsize=(10, 6))

    # Crea un gráfico de dispersión con los tiempos y tamaños
    plt.scatter(sizes, times, color='blue', label='Resultados')

    # Regresión polinómica (o ajuste lineal, dependiendo del objetivo)
    degree = 2  # Usamos un ajuste cuadrático en lugar de lineal
    coeffs = np.polyfit(sizes, times, degree)  # Calcula los coeficientes del polinomio cuadrático
    poly_fit = np.poly1d(coeffs)  # Crea la función del polinomio

    # Ordena los tamaños para un gráfico más suave de la línea de ajuste
    sorted_sizes = np.sort(sizes)
    fitted_times = poly_fit(sorted_sizes)  # Obtiene los tiempos ajustado

    # Dibuja la línea de ajuste
    plt.plot(sorted_sizes, fitted_times, color='red', label='Ajuste cuadrático')

    # Etiquetas y título del gráfico
    plt.xlabel('Tamaños ~ n * b')
    plt.ylabel('Tiempos')
    plt.title('Relación entre tamaño y tiempo de ejecución')
    plt.legend()

    # Muestra el gráfico
    plt.show()


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
        ('901b.in', '901b.out'),
        ('901c.in', '901c.out'),
    ]

    for f_in, f_out in test_cases:
        cases = read_cases_from_file(f_in)

        solutions = []

        for case in cases:
            solution = prueba1_backtracking(case['budget'], case['garments'], case['num_garments'])
            solutions.append(solution)
        correction, optimization = validation(f_out, solutions)
        print(f'Corrección para {f_in}: {correction:.0f}%, Optimización: {optimization:.0f}%')

    # Fichero con casos grandes creado por la función: 'generar_fichero_entrada_progresivo' => create_files.py
    time_test_cases = 'casos_grandes.in'

    # Ejecuta las pruebas de tiempo y construye los resultados
    times, sizes = time_test(time_test_cases)
    plot_results(times, sizes)



if __name__ == "__main__":
    main()







