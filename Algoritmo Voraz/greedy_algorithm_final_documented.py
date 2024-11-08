import time

def read_cases_from_file(filename):
    """
    Lee el fichero en la ruta indicada en 'filename'.

    Esta función toma una nombre de fichero 'filname' que contiene la ruta del fichero que se quiere leer.
    Al abrir el fichero, lee linea por linea para obtener el número de casos, el presupuesto, el numero de prendas,
    y los precios de los modelos de los modelos en cada caso. 

    Parámetro:
    filename (str): Cadena de texto que contiene la ruta del fichero.

    Devuelve:
    list of dict: Lista de diccionarios 'cases' con el presupuesto, número de prendas y los precios de cada prenda en cada caso.
    """
    cases = []

    with open(filename, 'r') as file:
        num_cases = int(file.readline().strip())  # Número de casos

        for _ in range(num_cases):
            # Lee el presupuesto y numero de tipos de prendas
            budget, num_garments = map(int, file.readline().strip().split())

            garments = []
            # Lee los precios de las prendas para cada tipo.
            for _ in range(num_garments):
                garment_prices = list(map(int, file.readline().strip().split()[1:]))
                garments.append(garment_prices)

            #Añadir el caso al listado con el presupuesto, número de prendas y la matriz de precios
            cases.append({'budget': budget, 'num_garments': num_garments, 'garments': garments})

    return cases


def greedy_selection(budget, garments, num_garments):
    """
    Algoritmo voraz que selecciona modelos de cada prenda para maximizar el gasto sin sobrepasar el presupuesto.

    Esta función toma el presupuesto 'budget', una lista de prendas con precios de modelos 'garments', 
    y el número total de prendas 'num_garments'. Selecciona el modelo óptimo para cada prenda considerando
    la restricción del presupuesto.

    Parámetros:
    budget (int): Presupuesto disponible.
    garments (list of list of int): Lista de cada prenda. Cada sublista contiene precios de modelos.
    num_garments (int): Número de prendas que se deben seleccionar.

    Devuelve:
    int: Dinero total gastado si se seleccionaron las prendas sin superar el presupuesto.
    None: Si no se pudo seleccionar una combinación sin exceder el presupuesto.
    """
    selected_prices = []  # Lista para almacenar los precios de los modelos seleccionados
    current_total = 0  # Total actual de los precios seleccionados
    weighted_garments = calculate_weights(garments)

    for _ in range(len(weighted_garments)):
        # Seleccionar la prenda con el mejor peso
        garment_with_best_weight = select_best_weighted_garment(weighted_garments)
        weighted_garments.remove(garment_with_best_weight)
        garment_prices = garment_with_best_weight[0]
    
        # Calcular el precio máximo por prenda que se puede seleccionar
        max_price_per_garment = (budget - current_total) / (num_garments - len(selected_prices))
        # Selecciona el precio más adecuado para la prenda actual
        max_feasible_price = selection(garment_prices, max_price_per_garment, current_total, budget)

        if max_feasible_price is not None:
            current_total += max_feasible_price
            selected_prices.append(max_feasible_price)
        else:
            break

    if not len(selected_prices) == num_garments: # Verifica si se seleccionaron todos los modelos necesarios
        return None

    return sum(selected_prices)

def selection(garment_prices, max_price_per_garment, current_total, budget):
    """
    Selecciona el modelo más factible de una prenda.

    La función toma los precios de una lista de modelos y selecciona el precio máximo que no supera 
    el límite 'max_price_per_garment'. Si no hay ningún precio factible, elige el modelo más barato que 
    permita mantenerse dentro del presupuesto 'budget' al sumarlo al dinero gastado hasta el momento 
    'current_total'.

    Parámetros:
    garment_prices (list of int): Lista de precios de cada modelo de una prenda.
    max_price_per_garment (int): Precio máximo permitido por prenda.
    current_total (int): Total gastado hasta el momento.
    budget (int): Presupuesto disponible.

    Devuelve:
    int: Precio factible de un modelo.
    None: Si no hay opciones dentro del presupuesto. 
    """
    max_feasible_price = None
    for price in garment_prices:
        if price <= max_price_per_garment:
            if max_feasible_price is None or max_feasible_price < price:
                max_feasible_price = price

    if max_feasible_price is None:
        min_price = min(garment_prices)
        if current_total + min_price <= budget:
            max_feasible_price = min_price

    return max_feasible_price

def calculate_weights(garment_list):
    """
    Asigna un peso a cada prenda.

    Esta funcion toma una lista de listas, donde cada sublista representa una prenda con
    el precio de los modelos, y Asigna un peso a cada prenda.

    Parámetros:
    garment_list (list of list of int): Lista de listas; cada sublista contiene precios de modelos.  
    
    Devuelve:
    list of tuples: Lista de tuplas; cada tupla contiene los modelos de una prenda con el peso asignado
    """
    weighted_list = []
    for prices in garment_list:
        price_range = max(prices) - min(prices)
        model_count = len(prices)
        # Cálculo del peso: priorizar un rango de precios pequeño y menos modelos
        weight = (1 / (model_count + 1)) + (1 / (price_range + 1))
        weighted_list.append((prices, weight))
    return weighted_list


def select_best_weighted_garment(weighted_garments):
    """
    Selecciona la prenda con mayor peso.

    Esta función toma una lista de tuplas 'weighted_garments', cada tupla representa una prenda con 
    la lista de los precios de cada modelo y el peso asignado y obtiene la prenda con mayor 
    peso.

    Prámetros:
    weighted_garments (list of tuples): Lista de tuplas con el precio de los modelos y sus pesos.

    Devuelve:
    tuple: Tupla con la lista de precios de una prenda y su respectivo peso. 
    """
    best_weight = None
    best_garment = None
    for garment, weight in weighted_garments:
        if best_weight is None or best_weight < weight:
            best_weight = weight
            best_garment = (garment, weight)
    return best_garment



def validation(out_file, greedy_solution):
    """
    Compara las salidas de 'out_file' con 'greedy_solution' para calcular la precisión.

    Esta función toma el archivo 'out_file' con las soluciones esperadas y compara con las soluciones
    de 'greedy_solution' para calcular la precisión en porcentaje.

    Parámetros:
    out_file (str): Ruta del fichero con las soluciones esperadas.
    greedy_solution (list): Lista de modelos seleccionados por el algoritmo.

    Devuelve:
    int: Precisión del algoritmo en porcentaje.
    list of float: Lista con las precisiones de cada caso.
    """
    greedy_solution = [greed_sol or 0 for greed_sol in greedy_solution]

    # Leer soluciones esperadas desde el archivo
    with open(out_file, 'r') as out_file:
        actual_solutions = [
            0 if line.strip() == 'no solution' else int(line.strip())
            for line in out_file
        ]

    percentages = []
    for i in range(len(actual_solutions)):

        if actual_solutions[i] == 0:
            if greedy_solution[i] == 0:
                percentages.append(100.0)  # Ambas son cero, coincidencia perfecta
            else:
                percentages.append(0.0)  # La esperada es cero, pero la actual no lo es
        else:
            percentage = (greedy_solution[i] * 100) / actual_solutions[i]# Calcula el porcentaje
            percentages.append(round(percentage, 2))


    accuracy = round(sum(percentages) / len(percentages), 2)
    return accuracy, percentages

# Lista de casos de prueba, tanto los datos de entrada como las salidas esperadas.
test_cases = [
    ('901a.in', '901a.out'),
    ('901b.in', '901b.out'),
    ('901c.in', '901c.out'),
]

for f_in, f_out in test_cases:

    cases = read_cases_from_file(f_in)

    solutions = []
    times = []

    for case in cases:
        time_start = time.time()
        solution = greedy_selection(case['budget'], case['garments'], case['num_garments'])
        time_end = time.time()
        times.append(time_end - time_start)
        solutions.append(solution)
        print(f'Number of garments: {case['num_garments']}, time of execution: {time_end - time_start:.7f} s')
    accuracy, pr = validation(f_out, solutions)
    print(f'Accuracy for {f_in}: {accuracy}, Times: {(sum(times) / len(times)):.7f} s')