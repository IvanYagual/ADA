def read_input_from_file(filename: str) -> list[dict]:
    cases = [] 

    with open(filename) as file:
        Number_cases = int(file.readline().strip())

        for _ in range(Number_cases):
            line = file.readline().strip().split()
            budget, number_garments = [int(x) for x in line] # M - budget, C - number of garments
            garments = []

            for _ in range(number_garments):
                line = list(map(int, file.readline().strip().split()))
                prices = line[1:]
                garments.append(prices)  # matrix of garments

            # each case is a dictionary that consists of M, C and garments matrix
            cases.append({'budget': budget, 'number_garments': number_garments, 'garments': garments})

    return cases # list of dictionaries


def voraz(case: dict) -> tuple:
    sol = []
    budget = case['budget'] 
    number_garments = case['number_garments'] 
    garments = case['garments']
    candidates = []
    money = budget

   # for garment, models in enumerate(garments):
    #    for price in models:
     #       candidates.append((price, garment + 1))  # (price, garment_type)
    for garment, models in enumerate(garments):
        candidates.append((models, garment + 1))  # (price, garment_type)


    type_garment_added = []
    while len(candidates) > 0 and not solution(sol, number_garments):
        candidate = candidates.pop(0) # Delete the first candidate
        #if candidate[1] not in type_garment_added:
            #if cont % 2 == 0 and budget != 62:
            #insert(sol, candidate, budget)

        money, sol = prueba(sol,candidate, money, budget)
        
        type_garment_added.append(candidate[1])


    
#    if not solution(sol, number_garments):
 #       print("No se puede encontrar solución")
    
    print(sol)
    return sol, budget #sol:  




def solution(sol: list, number_garments: int) -> bool:
    return len(sol) == number_garments


def prueba(sol,candidate, money, budget):
    candidate[0].sort(reverse=True, key= lambda x: x)
    type_garment = candidate[1]
    prices = candidate[0]

    for price in prices:
        if money < budget:
            sol.append((price, type_garment))
            money = money - price
    
        low_price = min(prices)
        sol.append((low_price, type_garment))

    return money, sol

            


#center value
def insert(sol: list, candidate: tuple, budget:int):
    l = candidate[0]
    l.sort()
    medio = len(l) // 2
    price_min = l[medio]
    price_total = 0
    for price, _ in sol:
        price_total = price + price_total 
    if price_total < budget/len(l):
        sol.append((price_min, candidate[1]))
    else:
        prueba


#Read file
#Rute Iván
filename = '/home/ivan/Universidad/2º Curso/Analisis y diseños de algoritmos/PRACTICAS/Algoritmo Voraz/tests/T1/901a.in'
filename_out = '/home/ivan/Universidad/2º Curso/Analisis y diseños de algoritmos/PRACTICAS/Algoritmo Voraz/tests/T1/901a (Copiar2).out'

#Rute Katerine (no se si se escribe asi (*^_^*)
#filename = '/home/ivan/Universidad/2º Curso/Analisis y diseños de algoritmos/ADA_boletin_P1/enunciados/04 - boda/tests/T1/901a.in'

cases = read_input_from_file(filename) # dictionarys list [{M:Budget, C:number garments, garments: models lists}]
for case in cases:
    #the case are set of garments
    sol, budget = voraz(case)  # Result: set of garments opt.
    if len(sol) > 0:
        price_total = 0
        print("")
        for price, gurment in sol:
            price_total = price_total + price
            #print(f"La prenda {gurment} cuesta {price} presupuesto {budget}")
        if price_total < budget:    
            print(f"Se gasto un total de: {price_total} con presupuesto de {budget}")
        else:
            print(f"Se gasto un total de: {price_total} con presupuesto de {budget} FALLO")
    