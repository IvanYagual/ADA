import random
import string
import time
from typing import Dict, Tuple, List
import numpy as np
import matplotlib.pyplot as plt


def generate_strings(amount: int, max_window_size: int, max_string_length: int) -> Dict[str, int]:
    """
    Genera casos de prueba aleatorios para el algoritmo.

    Parámetros:
        amount(int): Cantidad de casos a generar.
        max_window_size(int): Valor máximo para tamaño de la subcadena (ventana deslizante).
        max_string_length(int): Longitud máximo de la cadena.
    Devuelve:
        dict: Diccionario con las cadenas generadas como claves y los valores de window_size como valores.
              Formato: {"cadena_generada": window_size}
    Excepciones:
        ValueError: Si `amount`, `max_window_size`, or `max_string_length` no es positivo.
    """
    if amount <= 0 or max_window_size <= 0 or max_string_length <= 0:
        raise ValueError("All parameters must be positive integers.")

    cases = {}

    for _ in range(amount):
        string_length = random.randint(2, max_string_length)
        window_size = random.randint(2, min(max_window_size, string_length))

        # Generamos una cadena aleatoria de longitud n usando solo letras de 'a' a 'z'
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(string_length))

        cases[random_string] = window_size

    return cases


def time_test(cases: Dict[str, int]) -> None:
    """
    Realiza pruebas de tiempo de ejecución para dos métodos diferentes: directo basico, directo optimo y uno basado en
    divide y vencerás, midiendo su rendimiento con diferentes tamaños de entrada.

    Parámetros:
        cases (dict): Un diccionario donde la clave es una cadena aleatoria (`random_string`) y
        el valor es el tamaño de la ventana (`window_size`).
    """

    times_direct = []  # Lista para los tiempos del método directo
    times_direct_optimal = [] # Lista para los tiempos del método directo optimo
    times_dc = []  # Lista para los tiempos del método divide y vencerás
    sizes = []  # Lista para los tamaños de los casos

    # Recorremos todos los casos proporcionados
    for random_string, window_size in cases.items():

        size = window_size

        # Mide el tiempo de ejecución del método directo
        direct_start_time = time.perf_counter()
        direct_method(random_string, window_size)
        direct_end_time = time.perf_counter()

        # Mide el tiempo de ejecución del método directo optimo
        direct_opt_start_time = time.perf_counter()
        direct_method_optimal(random_string, window_size)
        direct_opt_end_time = time.perf_counter()

        # Mide el tiempo de ejecución del método de Divide y Vencerás
        dc_start_time = time.perf_counter()
        divide_and_conquer_method(random_string, window_size)
        dc_end_time = time.perf_counter()

        # Almacena los tiempos de ejecución y el tamaño del caso
        times_direct.append(direct_end_time - direct_start_time)
        times_dc.append(dc_end_time - dc_start_time)
        times_direct_optimal.append(direct_opt_end_time - direct_opt_start_time)
        sizes.append(size)

    # Configura el tamaño de la figura del gráfico
    plt.figure(figsize=(10, 6))

    # Crea un gráfico de dispersión con los tiempos de ambos métodos y tamaños de los casos
    plt.scatter(sizes, times_direct, color='blue', label='Resultados_direct')
    plt.scatter(sizes, times_direct_optimal, color='green', label='Resultados_direct_optimo')
    plt.scatter(sizes, times_dc, color='red', label='Resultados_DyV')

    # Ajuste de primer grado para el método directo
    p_direct = np.polyfit(sizes, times_direct, 2)
    fitted_direct = np.polyval(p_direct, sizes)  #
    plt.plot(sizes, fitted_direct, color='blue', linestyle='dashed', label='Ajuste Directo')

    # Ajuste de primer grado para el método directo
    p_direct_opt = np.polyfit(sizes, times_direct_optimal, 1)
    fitted_direct_opt = np.polyval(p_direct_opt, sizes)  #
    plt.plot(sizes, fitted_direct_opt, color='green', linestyle='dashed', label='Ajuste Directo Optimo')

    # Ajuste de primer grado para el método Divide y Vencerás
    p_dc = np.polyfit(sizes, times_dc, 2)
    fitted_dc = np.polyval(p_dc, sizes)
    plt.plot(sizes, fitted_dc, color='red', linestyle='dashed', label='Ajuste DyV')

    # Etiquetas y título del gráfico
    plt.xlabel('Tamaños')
    plt.ylabel('Tiempos')
    plt.title('Relación entre tamaño y tiempo de ejecución')
    plt.legend()

    # Muestra el gráfico generado
    plt.show()


def validation(cases: Dict[str, int]) -> None:
    """
        Valida los resultados de los métodos de algoritmo comparando las salidas
        de las soluciones generadas por los métodos directo y divide y vencerás.

        Parámetros:
            cases (dict): Diccionario con las cadenas generadas como claves y los valores de window_size como valores.
              Formato: {"cadena_generada": window_size}

        Devuelve:
            None: La función imprime el resultado de la comparación entre los dos métodos.
                  Si hay discrepancias, se muestran los casos fallidos,
                  de lo contrario, se indica que todos los tests pasaron.
    """
    mismatched = []

    for index, (random_string, window_size) in enumerate(cases.items()):

        # Ejecutar ambos métodos
        direct_results = direct_method(random_string, window_size)
        dc_results = divide_and_conquer_method(random_string, window_size)

        print(f"  Case: {index + 1}")
        print(f"  String: {random_string}, Window size: {window_size}")
        print(f"  Direct Method Valid Results: {direct_results}")
        print(f"  Divide and Conquer Method Result: {dc_results}\n")

        # Verificar si los resultados no coinciden
        if dc_results not in direct_results:
            mismatched.append((index, random_string, window_size, direct_results, dc_results))

    if mismatched:
        print("Mismatched found: ")
        for mismatch in mismatched:
            print(f"  Case: {mismatch[0] + 1}")
            print(f'  String: {mismatch[1]}, Window size: {mismatch[2]}')
            print(f'  Direct Method Valid Results: {mismatch[3]}')
            print(f'  Divide and Conquer Method Result: {mismatch[4]}')

    else:
        print("All tests passed!!!")



def direct_method_optimal(letters_str: str, window_size: int) -> List[Tuple[int, int]]:
    """
    Encuentra las subcadenas de longitud `window_size` con la mayor diferencia total en los valores ASCII
    entre caracteres consecutivos en una cadena dada.

    Parámetros:
        letters_str (str): Cadena de letras sobre la que se realiza el análisis.
        window_size (int): Tamaño de la subcadena (ventana deslizante).

    Devuelve:
        list: Una lista de tuplas, donde cada tupla contiene:
            - max_total (int): La suma máxima de las diferencias absolutas entre caracteres consecutivos en la subcadena.
            - position (int): La posición (índice) donde comienza la subcadena que tiene la suma máxima de diferencias.

    Excepciones:
        ValueError: Si el tamaño de la subcadena `whole_num` es mayor que la longitud de la cadena `letters_str`,
                    o si `whole_num` es menor que 2.
    """
    n = len(letters_str)

    # Verificamos que los parámetros sean válidos
    if n < window_size or window_size < 2:
        raise ValueError(
            'Invalid parameters: The length of the string must be greater than or equal to the window size (n >= m), '
            'and the window size must be at least 2.')

    # Calculamos las diferencias entre caracteres consecutivos
    difference = [abs(ord(letters_str[i]) - ord(letters_str[i + 1])) for i in range(n - 1)]

    # Calculamos la diferencia total para la primera subcadena
    total = sum(difference[:window_size - 1])
    max_total = total
    position = 1  # La primera posición es 1, ya que las posiciones son 1-basadas

    valid_solutions = [(max_total, position)]

    # Recorremos la cadena con una subcadena deslizante
    for i in range(1, n - window_size + 1):  # Corrected loop boundary
        # Actualizamos la suma restando el carácter que sale y sumando el carácter que entra
        total -= difference[i - 1]
        total += difference[i + window_size - 2]  # Corrected index for entering character

        # Verificamos si la suma actual es mayor que el máximo
        if total > max_total:
            max_total = total
            valid_solutions = [(total, i + 1)]  # Nueva subcadena con una mayor suma
        elif total == max_total:
            valid_solutions.append((total, i + 1))  # Igualando el máximo, agregamos la solución

    return valid_solutions


def direct_method(letters_str: str, window_size: int) -> list[Tuple[int, int]]:
    """
    Encuentra las subcadenas de longitud `window_size` con la mayor diferencia total en los valores ASCII
    entre caracteres consecutivos en una cadena dada, sin utilizar ventana deslizante.

    Parámetros:
        letters_str (str): Cadena de letras sobre la que se realiza el análisis.
        window_size (int): Tamaño de la subcadena.

    Devuelve:
        list: Una lista de tuplas, donde cada tupla contiene:
            - max_total (int): La suma máxima de las diferencias absolutas entre caracteres consecutivos en la subcadena.
            - position (int): La posición (índice) donde comienza la subcadena que tiene la suma máxima de diferencias.

    Excepciones:
        ValueError: Si el tamaño de la subcadena `whole_num` es mayor que la longitud de la cadena `letters_str`,
                    o si `whole_num` es menor que 2.
    """
    n = len(letters_str)

    # Verificamos que los parámetros sean válidos
    if n < window_size or window_size < 2:
        raise ValueError(
            'Invalid parameters: The length of the string must be greater than or equal to the window size (n >= m), '
            'and the window size must be at least 2.')

    valid_solutions = []
    max_total = float('-inf')  # Inicializamos la diferencia máxima con el valor más bajo posible
    difference = [abs(ord(letters_str[i]) - ord(letters_str[i + 1])) for i in range(n - 1)]

    # Recorremos todas las posibles subcadenas de tamaño `window_size`
    for i in range(n - window_size + 1):
        # Calculamos la diferencia total para la subcadena actual
        total = sum(difference[i:i + window_size - 1])

        # Verificamos si la suma es mayor que la máxima encontrada hasta ahora
        if total > max_total:
            max_total = total
            valid_solutions = [(total, i + 1)]  # Nueva subcadena con una mayor suma
        elif total == max_total:
            valid_solutions.append((total, i + 1))  # Igualando el máximo, agregamos la solución

    return valid_solutions


def divide_and_conquer_method(letters_str: str, window_size: int) -> Tuple[int, int]:
    """
    Método de divide y vencerás para encontrar la subcadena con la mayor diferencia
    total en valor absoluto entre caracteres consecutivos en una cadena.

    :param letters_str: Cadena de caracteres en la que buscar la subcadena.
    :param window_size: Tamaño de la subcadena a evaluar (ventana deslizante).
    :return: Diferencia total máxima y posición (1-based) de la subcadena óptima.
    """

    def calculate_total_diff_substring(start: int) -> int:
        """
        Calcula la diferencia total entre caracteres consecutivos en una subcadena.

        :param start: El índice inicial de la subcadena a evaluar.
        :param window_size: El tamaño de la subcadena (ventana deslizante).
        :return: La suma de las diferencias absolutas entre caracteres consecutivos.
        """
        # Calcula la diferencia absoluta entre caracteres consecutivos en la subcadena.
        return sum(difference[start:start + window_size])

    def divide_and_conquer(i: int, j: int) -> Tuple[int, int]:
        """
        Función recursiva que divide la cadena en subproblemas más pequeños y los resuelve.
        Si una subcadena tiene tamaño suficiente (mayor o igual que 'whole_num'),
        se divide, de lo contrario, se evalúa usando el método directo (ventana deslizante).

        :param i: El índice inicial de la subcadena.
        :param j: El índice final de la subcadena.
        :return: La diferencia total máxima y la posición (1-based) de la subcadena óptima.
        """

        # Caso base 1: Si la subcadena es más pequeña que el tamaño de la ventana (no se puede dividir más)
        if j - i + 1 < window_size:
            return float('-inf'), -1  # No hay solución válida en este caso

        # Caso base 2: Si la subcadena tiene el tamaño exacto de 'whole_num', simplemente calculamos la diferencia total
        if j - i + 1 == window_size:
            total_sum = calculate_total_diff_substring(i)
            return total_sum, i + 1  # Devolvemos la posición (1-based)

        # Caso recursivo: Si la subcadena es suficientemente grande, la dividimos
        m = (i + j) // 2  # Calculamos el punto medio de la subcadena
        left_solution, left_position = divide_and_conquer(i, m)  # Resolvemos el subproblema izquierdo
        right_solution, right_position = divide_and_conquer(m + 1, j)  # Resolvemos el subproblema derecho

        # Evaluamos la "frontera" entre las dos mitades
        border_solution, border_position = frontera_case_solution(i, m, j)

        # Seleccionamos la mejor solución entre las tres opciones
        if left_solution >= right_solution and left_solution >= border_solution:
            return left_solution, left_position  # Mejor solución en la mitad izquierda
        elif right_solution >= left_solution and right_solution >= border_solution:
            return right_solution, right_position  # Mejor solución en la mitad derecha
        else:
            return border_solution, border_position  # Mejor solución en la frontera

    def frontera_case_solution(i: int, m: int, j: int) -> Tuple[int, int]:
        """
        Evalúa las subcadenas de la "frontera" entre las mitades izquierda y derecha.
        Esto se refiere a subcadenas que incluyen caracteres tanto de la mitad izquierda
        como de la mitad derecha de la subcadena original.

        :param i: El índice inicial de la subcadena.
        :param m: El índice medio (división de la subcadena).
        :param j: El índice final de la subcadena.
        :return: La diferencia total máxima y la posición (1-based) de la subcadena en la frontera.
        """
        max_diff = float('-inf')  # Inicializamos la diferencia máxima con el valor más bajo posible
        position = -1  # Inicializamos la posición con valor inválido

        # Evaluamos todas las subcadenas en la frontera
        for k in range(max(i, m - window_size + 2), m + 1):
            if k + window_size - 1 > j:
                break  # Si la subcadena es demasiado grande, terminamos
            total = calculate_total_diff_substring(k)  # Calculamos la diferencia total
            if total > max_diff:  # Si encontramos una mejor diferencia, actualizamos
                max_diff = total
                position = k + 1  # Convertimos la posición a base 1

        return max_diff, position  # Retornamos la mejor solución en la frontera

    # Verificamos que la longitud de la cadena sea válida para el tamaño de la subcadena
    n = len(letters_str)

    if n < window_size or window_size < 2:
        raise ValueError(
            'Invalid parameters: The length of the string must be greater than or equal to the window size (n >= m), '
            'and the window size must be at least 2.'
        )

    # Calculamos las diferencias entre caracteres consecutivos
    difference = [abs(ord(letters_str[i]) - ord(letters_str[i + 1])) for i in range(n - 1)]
    window_size -= 1 # actualizamos para la lista de diferencias

    # Llamamos a la función recursiva para empezar el proceso de dividir y vencer
    return divide_and_conquer(0, n - 2)


if __name__ == '__main__':
    validation_test_cases = generate_strings(50, 200, 500)

    validation(validation_test_cases)

    time_test_cases = generate_strings(100, 20000, 30000)

    time_test(time_test_cases)
















