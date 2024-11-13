

import math

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

"""
def generar(nivel, s, num_garments, garments):
    s[nivel] += 1
    if s[nivel] == num_garments: #maximo de modelos 
        total_actual += garments[nivel][s[nivel]]
    return s

def solucion (nivel, s, total_actual, budget, n_garments):
    return (nivel == n_garments) and (total_actual <= budget)

def criterio(nivel, s, total_actual, budget, n_garments):
    return (nivel < n_garments) and  (total_actual <= budget)


def mas_hermanos(nivel, s):
    return s[nivel] < num_modelos



def backtracking(budget, garments, num_garments):
    nivel = 0
    s = 0
    voa = - math.inf
    soa = None
    total_actual = 0
    weighted_garments = calculate_weight(nivel, s, num_garments, garments)

    while nivel != 0:
        garment_with_best_weight = select_best_weighted_garment(weighted_garments)
        s = generar (nivel, s, garment_with_best_weight)
        if solucion(nivel, s) and total_actual > voa:
            voa = total_actual
            soa = s
        if criterio(nivel, s):
            nivel = nivel + 1
        else:
            while not masHermanos(nivel, s) and nivel > 0:
                s = retroceder(nivel, s)
    return s
"""




def solucion (nivel,total_actual, budget, n_garments):
    return (nivel == n_garments) and (total_actual <= budget)

def criterio(nivel, total_actual, budget, n_garments):
    return (nivel < n_garments) and  (total_actual <= budget)

def prueba_retroceder(nivel, hermanos_recorridos, s):
    s[nivel] = -1
    hermanos_recorridos += 1
    return hermanos_recorridos
#-----------------------------------------------------


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

def prubea_mas_hermanos(nivel, hermnanos_recorridos, garments):
    return hermnanos_recorridos < len(garments[nivel])

def prube_generar(nivel, s, hermanos_recorridos, garments, total_gastado, budget):
    total_gastado += garments[nivel][hermanos_recorridos]
    if total_gastado <= budget:
        s[nivel] = garments[nivel][hermanos_recorridos]
    return s, total_gastado


def prueba1_backtracking(budget, garments, num_garments):
    nivel = 0 #Inicializa en la raiz
    s = [0] * num_garments #Inicialización
    all_combinations = [] #Guarda todas las posibles combinaciones
    hermanos_recorridos = [0] * num_garments #Lista cada posición representa el nivel y cada valor el indice del hermano
    total_gastado = 0
    #soa = None
    #total_actual = 0#Dinero acumulado
    #weighted_garments = calculate_weight(garments)
    #garment_with_best_weight = select_best_weighted_garment(weighted_garments)
    while nivel>=0:
        #garment_with_best_weight = select_best_weighted_garment(weighted_garments)
        #garment in weighted_garments: # Recorre las prendas
        #s, total_actual = prube_generar (total_actual, nivel, s, garment_with_best_weight[nivel])# se añade el modelo más caro de la prenda
        print(s)
        if nivel == num_garments or total_gastado > budget: # Significa que ya ha obtenido un modelo de cada prenda
            if total_gastado <= budget:
                all_combinations.append(s[:]) #Añade esa combinacion de modelos
            nivel -= 1 #Sube de nivel 
            total_gastado -= garments[nivel][hermanos_recorridos[nivel]]
            if nivel >= 0: # Si no se encuentra en la raiz
                hermanos_recorridos[nivel] += 1 #Indica que pasará al siguiente hermano

        elif prubea_mas_hermanos(nivel, hermanos_recorridos[nivel], garments): # faltan hermanos por recorrer
            s, total_gastado = prube_generar(nivel, s, hermanos_recorridos[nivel], garments, total_gastado, budget) # Añade el siguiente hermano
            nivel += 1 #Sube de nivel
            if nivel < num_garments:
                hermanos_recorridos[nivel] = 0
        else:
            nivel -= 1
            if nivel != -1:
                total_gastado -= garments[nivel][hermanos_recorridos[nivel]]
            if nivel >= 0:
                hermanos_recorridos[nivel] += 1
    return all_combinations



def calculate_weight(garments_list):
    weighted_list = []
    for prices in garments_list:
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
    #for garment, weight in weighted_garments:
    #    if best_weight is None or best_weight < weight:
     #       best_weight = weight
      #      best_garment = (garment, weight)
    weighted_garments.sort(key= lambda x: x[1], reverse=True)
    return weighted_garments



def main():
    test_cases = [
    ('901a (Copy).in', '901a.out')
    #('901b.in', '901b.out'),
    #('901c.in', '901c.out'),
    ]
    garments = [
    [2, 5, 8],  # Precios para la prenda 1
    [7, 4, 6, 3, 5],  # Precios para la prenda 2
    [1, 8, 3, 6, 8, 10]  # Precios para la prenda 3
]
    # Validación de los casos de prueba
    for f_in, f_out in test_cases:

        cases = read_cases_from_file(f_in)

        solutions = []

        for case in cases:
            solution = prueba1_backtracking(13, garments, len(garments))
            print(solution)
            #solutions.append(solution)
        #correction, optimization = validation(f_out, solutions)
        #print(f'Corrección para {f_in}: {correction:.0f}%, Optimización: {optimization:.2f}%')




if __name__ == "__main__":
    main()


           #if solucion(nivel, total_actual, budget, num_garments) and total_actual > voa:
        #    if total_actual > voa:
        #        voa = total_actual
        #        soa = s[:]
"""
        if criterio(nivel, total_actual, budget, num_garments): # si todavia tenemos presupuesto y niveles por recorrer
            s, total_actual = prube_generar (total_actual, nivel, s, garment_with_best_weight[nivel])# se añade el modelo más caro de la prenda
            nivel += 1
        else:
            nivel -= 1
            hermanos_recorridos = 0
            while prubea_mas_hermanos(nivel, hermanos_recorridos, garment_with_best_weight) and nivel > 0: #mientras no se recorran todos los hermnanos
                if hermanos_recorridos < len(garment_with_best_weight[nivel][0]):
                    s, price = prueba_retroceder(nivel, s, garment_with_best_weight, hermanos_recorridos)
                #total_actual -= price
                if hermanos_recorridos ==13:
                    pass
                if hermanos_recorridos >=  len(garment_with_best_weight[nivel][0]):
                    s[nivel]= -1
                    nivel -= 1
                hermanos_recorridos += 1
    return soa, voa 
    """