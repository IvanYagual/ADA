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
                K = line[0] # number of models for each particular garment ??????????
                prices = line[1:]
                garments.append(prices)  # matrix of garments

            # each case is a dictionary that consists of M, C and garments matrix
            cases.append({'budget': budget, 'number_garments': number_garments, 'garments': garments})

    return cases # list of dictionaries


def voraz(case: dict) -> list:
    sol = []
    budget = case['budget'] 
    number_garments = case['number_garments'] 
    garments = case['garments']
    candidates = []

    for garment, models in enumerate(garments):
        for price in models:#REcordar error no gestiona bien el numero de prende
            print(garment)
            candidates.append((price, garment))  # (price, garment_type)
    
    candidates.sort(reverse=True, key=lambda price: price[0])

    while len(candidates) > 0 and not solution(sol, number_garments):
        candidate = candidates.pop(0) # Delete the first candidate
        if factible(sol, candidate, budget):
            insert(sol, candidate)

    if not solution(sol, number_garments):
        return "No se puede encontrar solución"
    
    return sol, sum(price for price, _ in sol) #Solucion y 


def select(candidates:list) -> int:
    return candidates[0]


def factible(sol: list, candidate: tuple, budget: int) -> bool: 
    total_price = sum(price for price, _ in sol)  #!!!!!NO SE SI 'total_price' ES UN NOMBRE ADECUADO!!!

    return (candidate not in sol) and (total_price <= budget)


def solution(sol: list, number_garments: int) -> bool:
    return len(sol) == number_garments


def insert(sol: list, candidate: tuple):
    sol.append(candidate)



#Read file
#Rute Iván
filename = '/home/ivan/Universidad/2º Curso/Analisis y diseños de algoritmos/PRACTICAS/Algoritmo Voraz/tests/T1/901a.in'

#Rute Katerine (no se si se escribe asi (*^_^*)
#filename = '/home/ivan/Universidad/2º Curso/Analisis y diseños de algoritmos/ADA_boletin_P1/enunciados/04 - boda/tests/T1/901a.in'

cases = read_input_from_file(filename) # dictionarys list [{M:Budget, C:number garments, garments: models lists}]


for case in cases:
    #the case are set of garments
    result = voraz(case)  # Result: set of garments opt.
    print(result)
