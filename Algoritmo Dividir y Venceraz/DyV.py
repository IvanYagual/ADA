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
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

        cases[random_string] = m

    return cases

def calculate_total_diff(letters_str, start, whole_num):
    """Calculate the total absolute difference for a substring of size `whole_num` starting at `start`."""
    return sum(abs(ord(letters_str[j]) - ord(letters_str[j + 1])) for j in range(start, start + whole_num - 1))


def divide_and_conquer_method_1(letters_str, whole_num):

    def frontera_case_solution(letters_str, i, m,  j, whole_num):

        solution = float('-inf')
        position = -1

        for k in range(max(i, whole_num - m + 1), m + 1):

            if k + whole_num - 1 > j:
                break

            total = calculate_total_diff(letters_str, k, whole_num)

            # Verificamos si la suma actual es mayor que el máximo
            if total > solution:
                solution = total
                position = k + 1

        return solution, position

    def divide_and_conquer(i,j):
        if j - i + 1 < whole_num: #caso basico zero (i,j)
            return float('-inf'), -1 #direct_solution(i,j)
        if j - i + 1 == whole_num:  #caso basico algo (i,j)
            total_sum = calculate_total_diff(letters_str, 0, whole_num)
            return total_sum, i + 1

        m = (i + j) // 2 #devide(i,j)
        left_solution, left_position = divide_and_conquer(i, m)
        right_solution, right_position = divide_and_conquer(m + 1, j)

        border_total, border_position = frontera_case_solution(letters_str, i, m, j, whole_num)

        if left_solution >= right_solution and left_solution >= border_total:
            return left_solution, left_position
        elif right_solution >= left_solution and right_solution >= border_total:
            return right_solution, right_position
        else:
            return border_total, border_position

    n = len(letters_str)

    # Verificamos que los parámetros sean válidos
    if n < whole_num or whole_num < 2:
        raise ValueError(
            'Invalid parameters: The length of the string must be greater than or equal to the window size (n >= m), '
            'and the window size must be at least 2.')

    return divide_and_conquer(0, n - 1)


def divide_and_conquer_method_2(letters_str, whole_num, k = 10):

    def like_direct_method_but_index(letters_str, i, j, whole_num):

        total = calculate_total_diff(letters_str, i, whole_num)
        max_total = total
        position = i

        # Recorremos la cadena con una subcadena deslizante
        for l in range(i + 1, min(j - whole_num + 2, len(letters_str) - whole_num + 1)):
            # Actualizamos la suma restando el carácter que sale y sumando el carácter que entra
            total -= abs(ord(letters_str[l - 1]) - ord(letters_str[l]))
            total += abs(ord(letters_str[l + whole_num - 2]) - ord(letters_str[l + whole_num - 1]))

            # Verificamos si la suma actual es mayor que el máximo
            if total > max_total:
                max_total = total
                position = l + 1

        return max_total, position

    max_sol = float('-inf')
    max_index = -1

    n = len(letters_str)
    if n < 2 * m:
        k = 1
    division_size = (n + k - 1) // k #we need our string to be divided into k parts, so we use celling division

    for i in range(k):
        start = i * division_size
        end = min(start + division_size - 1, n - 1)

        if end - start  + 1 < whole_num: #only gonna be the case in the last division or if k is to big
            continue

        sol_div, pos_div = like_direct_method_but_index(letters_str, start, end, whole_num)

        if sol_div > max_sol:
            max_sol = sol_div
            max_index = pos_div
        '''
        if i < k - 1:
            overlap_start = end - whole_num + 2  # Overlap region start
            overlap_end = min(end + whole_num - 1, n - 1)  # Overlap region end
            overlap_max_diff, overlap_index = like_direct_method_but_index(letters_str, overlap_start, overlap_end, whole_num)

            if overlap_max_diff > max_sol:
                max_sol = overlap_max_diff
                max_index = overlap_index'''

    return max_sol, max_index



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


if __name__ == '__main__':
    letters1 = 'cddabcdacc'
    m1 = 5
    print(divide_and_conquer_method_1(letters1, m1))
    test_cases = generate_strings(5, 10, 20)
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
            max_total3, position3 = divide_and_conquer_method_2(random_string, m)
            print(f"Divide and conquer method 2: divide into k")
            print(f"Maximum Total Difference: {max_total3}")
            print(f"Starting Position (1-based): {position3}")
        except ValueError as e:
            print(f"Error: {e}")

    time_test_case = generate_strings(1, 10000000, 150000000)
    for random_string, m in time_test_case.items():
        try:
            #print(f"Random String {random_string}, m={m}")
            '''start_time = time.time()
            max_total1, position1 = divide_and_conquer_method_1(random_string, m)
            end_time = time.time()
            print(f"Divide and Conquer method 1: divide into 2")
            print(f"Time: {end_time - start_time}")
            print(f"Maximum Total Difference: {max_total1}")
            print(f"Starting Position (1-based): {position1}")'''
            start_time = time.time()
            max_total2, position2 = direct_method(random_string, m)
            end_time = time.time()
            print(f"Direct method")
            print(f"Time: {end_time - start_time}")
            print(f"Maximum Total Difference: {max_total2}")
            print(f"Starting Position (1-based): {position2}")
            start_time = time.time()
            max_total3, position3 = divide_and_conquer_method_2(random_string, m)
            end_time = time.time()
            print(f"Divide and conquer method 2: divide into k")
            print(f"Time: {end_time - start_time}")
            print(f"Maximum Total Difference: {max_total3}")
            print(f"Starting Position (1-based): {position3}")
        except ValueError as e:
            print(f"Error: {e}")