

import math


def generar(nivel, s):
    s[nivel] += 1
    if s[nivel] == num_modelos: #maximo de modelos 
        total_actual += garments[nivel][s[nivel]]
    return s

def solucion (nivel, s):
    return (nivel == n_garments) and (total_actual <= budget)

def criterio(nivel, s):
    return (nivel < n_garments) and  (total_actual <= budget)
def mas_hermanos(nivel, s):
    return s[nivel] < num_modelos

    

def backtracking(s_inicial):
    nivel = 0
    s = s_inicial
    voa = - math.inf
    soa = None
    total_actual = 0
    while nivel != 0:
        s = generar (nivel, s)
        if solucion(nivel, s) and total_actual > voa:
            voa = total_actual
            soa = s
        if criterio(nivel, s):
            nivel = nivel + 1
        else:
            while not masHermanos(nivel, s) and nivel > 0:
                s = retroceder(nivel, s)
    return s




if __name__ == "__main__":
    s_inicial = [x for x ]