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
    n = m_max
    for _ in range(amount):
        # Aseguramos que n,m >= 2 y n >= m
        #n = random.randint(2, n_max)
        m = random.randint(2, min(m_max, n))

        # Generamos una cadena aleatoria de longitud n usando solo letras de 'a' a 'z'
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

        cases[random_string] = m

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


def divide(DyV):
    count = 0
    l_div = []
    r = ''
    for x in DyV:
        count += 1 
        r += x
        if count == 10:
            count = 0
            l_div.append(r)
            r = ''
    return l_div


if __name__ == '__main__':
    letters1 = 'cddabcdacc'
    m1 = 5
    print(direct_method(letters1, m1))
    directo = ''
    DyV = ''
    test_cases = generate_strings(1, 40990000, 20)
    n = 5
    for random_string, m in test_cases.items():
        directo = random_string
        DyV = random_string
        #print(f"Cadena: {random_string}, m: {m}, direct_method: {direct_method(random_string, m)}")
    start = time.time()
    print(direct_method(random_string, n))
    final = time.time()
    print(final - start)
    l_DyV = divide(DyV)
    start = time.time()
    for x in l_DyV:
        direct_method(x, n)
    end = time.time()
    print(end - start)
    print("ya se hizo")