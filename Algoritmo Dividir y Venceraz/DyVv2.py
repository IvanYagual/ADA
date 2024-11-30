import random
import string
import time

def generate_strings(amount, m_max, n_max):
    """
    Genera casos de prueba aleatorios para el algoritmo.

    Parámetros:
        amount(int): Cantidad de casos a generar.
        m_max(int): Valor máximo para m (tamaño de la subcadena)
        n_max(int): Longitud máximo de la cadena.
    Devuelve:
        dict: Diccionario con las cadenas generadas como claves y los valores de m como valores.
              Formato: {"cadena_generada": m}
    """
    cases = {}

    for _ in range(amount):
        n = random.randint(2, n_max)
        m = random.randint(2, min(m_max, n))

        # Generamos una cadena aleatoria de longitud n usando solo letras de 'a' a 'z'
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))

        cases[random_string] = 3

    return cases


def direct_method(letters_str, whole_num):
    """
    Encuentra la subcadena de longitud `whole_num` con la mayor diferencia total en los valores ASCII
    entre caracteres consecutivos en una cadena dada.

    Parámetros:
        letters_str (str): Cadena de letras sobre la que se realiza el análisis.
        whole_num (int): Tamaño de la subcadena (ventana deslizante).

    Devuelve:
        tuple: Tupla con dos elementos:
            - max_total (int): La suma máxima de las diferencias absolutas entre caracteres consecutivos en la subcadena.
            - position (int): La posición (índice) donde comienza la subcadena que tiene la suma máxima de diferencias.

        Excepciones:
            ValueError: Si el tamaño de la subcadena `whole_num` es mayor que la longitud de la cadena `letters_str`,
                        o si `whole_num` es menor que 2.
        """
    n = len(letters_str)
    # Verificamos que los parámetros sean válidos
    if n < whole_num or whole_num < 2:
        raise ValueError(
            'Invalid parameters: The length of the string must be greater than or equal to the window size (n >= m), '
            'and the window size must be at least 2.')

    # Calculamos la diferencia total para la primera subcadena
    total = sum(abs(ord(letters_str[i]) - ord(letters_str[i + 1])) for i in range(whole_num - 1))
    max_total = total
    position = 1

    # Recorremos la cadena con una subcadena deslizante
    for i in range(1, n - whole_num + 1):
        # Actualizamos la suma restando el carácter que sale y sumando el carácter que entra
        total -= abs(ord(letters_str[i - 1]) - ord(letters_str[i]))
        total += abs(ord(letters_str[i + whole_num - 2]) - ord(letters_str[i + whole_num - 1]))

        # Verificamos si la suma actual es mayor que el máximo
        if total > max_total:
            max_total = total
            position = i + 1

    return max_total, position



def divide_and_conquer_method_1(letters_str, whole_num):
    """
    Método de divide y vencerás para encontrar la subcadena con la mayor diferencia
    total en valor absoluto entre caracteres consecutivos en una cadena.
    
    :param letters_str: Cadena de caracteres en la que buscar la subcadena.
    :param whole_num: Tamaño de la subcadena a evaluar (ventana deslizante).
    :return: Diferencia total máxima y posición (1-based) de la subcadena óptima.
    """

    def calculate_total_diff_substring(start):
        """
        Calcula la diferencia total entre caracteres consecutivos en una subcadena.
        
        :param letters_str: La cadena de entrada.
        :param start: El índice inicial de la subcadena a evaluar.
        :param whole_num: El tamaño de la subcadena (ventana deslizante).
        :return: La suma de las diferencias absolutas entre caracteres consecutivos.
        """
        # Calcula la diferencia absoluta entre caracteres consecutivos en la subcadena.
        return sum(abs(ord(letters_str[j]) - ord(letters_str[j + 1])) for j in range(start, start + whole_num - 1))

    def divide_and_conquer(i, j):
        """
        Función recursiva que divide la cadena en subproblemas más pequeños y los resuelve.
        Si una subcadena tiene tamaño suficiente (mayor o igual que 'whole_num'),
        se divide, de lo contrario, se evalúa usando el método directo (ventana deslizante).
        
        :param i: El índice inicial de la subcadena.
        :param j: El índice final de la subcadena.
        :return: La diferencia total máxima y la posición (1-based) de la subcadena óptima.
        """
        
        # Caso base 1: Si la subcadena es más pequeña que el tamaño de la ventana (no se puede dividir más)
        if j - i + 1 < whole_num:
            max_total = float('-inf')  # Inicializamos con el valor más bajo posible
            position = -1  # Inicializamos la posición con valor inválido

            # Evaluamos todas las posiciones posibles para subcadenas de tamaño 'whole_num'
            for start in range(i, j - whole_num + 2):
                total = calculate_total_diff_substring(start)  # Calculamos la diferencia total
                # Si encontramos una subcadena con mayor diferencia, la actualizamos
                if total > max_total:
                    max_total = total
                    position = start + 1  # Convertimos la posición a base 1

            return max_total, position

        # Caso base 2: Si la subcadena tiene el tamaño exacto de 'whole_num', simplemente calculamos la diferencia total
        if j - i + 1 == whole_num:
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

    def frontera_case_solution(i, m, j):
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
        for k in range(max(i, m - whole_num + 1), m + 1):
            if k + whole_num - 1 > j:
                break  # Si la subcadena es demasiado grande, terminamos
            total = calculate_total_diff_substring(k)  # Calculamos la diferencia total
            if total > max_diff:  # Si encontramos una mejor diferencia, actualizamos
                max_diff = total
                position = k + 1  # Convertimos la posición a base 1

        return max_diff, position  # Retornamos la mejor solución en la frontera

    # Verificamos que la longitud de la cadena sea válida para el tamaño de la subcadena
    n = len(letters_str)
    if n < whole_num or whole_num < 2:
        raise ValueError(
            'Invalid parameters: The length of the string must be greater than or equal to the window size (n >= m), '
            'and the window size must be at least 2.'
        )

    # Llamamos a la función recursiva para empezar el proceso de dividir y vencer
    return divide_and_conquer(0, n - 1)



if __name__ == '__main__':
    letters1 = 'cddabcdacc'
    m1 = 5
    test_cases = generate_strings(500, 10, 20)
    for random_string, m in test_cases.items():
        try:
            print(f"Random String {random_string}, m={m}")
            max_total1, position1 = divide_and_conquer_method_1(random_string, m)
            print(f"Divide and Conquer method 1: divide into 2")
            print(f"Maximum Total Difference: {max_total1}")
            print(f"Starting Position (1-based): {position1}")
            max_total2, position2 = direct_method(random_string, m)
            print(f"Direct method")
            print(f"Maximum Total Difference: {max_total2}")
            print(f"Starting Position (1-based): {position2}")
            if max_total1 != max_total2 or position1!=position2:
                print("error en ", random_string)
                l = []
                for x in random_string:
                    l.append(ord(x))
                r=[]
                for x in range(0, len(l)-1):
                    r.append(abs(l[x] - l[x+1]))
                print(r)
                break
                
        except ValueError as e:
            print(f"Error: {e}")

    # time_test_case = generate_strings(1, 10000000, 150000000)
    # for random_string, m in time_test_case.items():
    #     try:
    #         #print(f"Random String {random_string}, m={m}")
    #         '''start_time = time.time()
    #         max_total1, position1 = divide_and_conquer_method_1(random_string, m)
    #         end_time = time.time()
    #         print(f"Divide and Conquer method 1: divide into 2")
    #         print(f"Time: {end_time - start_time}")
    #         print(f"Maximum Total Difference: {max_total1}")
    #         print(f"Starting Position (1-based): {position1}")'''
    #         start_time = time.time()
    #         max_total2, position2 = direct_method(random_string, m)
    #         end_time = time.time()
    #         print(f"Direct method")
    #         print(f"Time: {end_time - start_time}")
    #         print(f"Maximum Total Difference: {max_total2}")
    #         print(f"Starting Position (1-based): {position2}")
    #         start_time = time.time()
    #         max_total3, position3 = divide_and_conquer_method_2(random_string, m)
    #         end_time = time.time()
    #         print(f"Divide and conquer method 2: divide into k")
    #         print(f"Time: {end_time - start_time}")
    #         print(f"Maximum Total Difference: {max_total3}")
    #         print(f"Starting Position (1-based): {position3}")
    #     except ValueError as e:
    #         print(f"Error: {e}")
    # l = []

    
    # for x in "ovebmrfuitsz":
    #     l.append(ord(x))
    # print(y)
    # r=[]
    # for x in range(0, len(l)-1):
    #     r.append(abs(l[x] - l[x+1]))
    # print(r)








