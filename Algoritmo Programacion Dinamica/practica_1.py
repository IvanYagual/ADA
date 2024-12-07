#

def encontrar_solucion(i,j,sol,v):
    if i == 0:    
        print(sol)
    else: 
        if v[i, j] == v[i-1, j]:
            s = sol.copy()
            s[i] = 0
            encontrar_solucion(i-1, j, s)

        if v[i, j] == b_i + v[i-1, j-p_1]:
            s = sol.copy()
            s[i] = 1
            encontrar_solucion(i - 1, j - p_1, s) 