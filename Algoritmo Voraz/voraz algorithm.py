def read_input_from_file(filename: str) -> list:
    cases = [] 

    with open(filename, 'r') as file:
        Number_cases = int(file.readline().strip())

        for _ in range(Number_cases):

            line = file.readline().strip().split()
            M, C = [int(x) for x in line] # M - budget, C - number of garments

            garments = []

            for _ in range(C):
                line = list(map(int, file.readline().strip().split()))
                K = line[0] # number of models for each particular garment ??????????
                prices = line[1:]
                garments.append(prices)  # matrix of garments

            # each case is a dictionary that consists of M, C and garments matrix
            cases.append({'M': M, 'C': C, 'garments': garments})

    return cases # list of dictionaries


def voraz(case: list) -> list:
    solution = []
    budget = case['M']
    garments = case['garments']

    candidates = []
    for i, models in enumerate(garments):
        for price in models:
            candidates.append((price, i))  # (price, garment_type)


    candidates.sort(reverse=True, key=lambda x: x[0])

    while len(candidates) > 0 and not solution(solution, case['C']):
        x = select(candidates)
        candidates.remove(x)
        if factible(solution, x, budget):
            insert(solution, x)

    if not solution(solution, case['C']):
        return "No se puede encontrar solución"
    return solution, sum(p[0] for p in solution) #Solucion y 

def select(candidates:list) -> int:
    return candidates[0]

def factible(solution, x, budget: int) -> bool:
    used_types = {garment[1] for garment in solution}
    price, garment_type = x
    return (garment_type not in used_types) and (sum(p[0] for p in solution) + price <= budget)

def solution(solution: list, C: int) -> bool:
    return len(solution) == C

def insert(solution: list, x: tuple):
    solution.append(x)



#Read file
#Rute Iván
filename = '/home/ivan/Universidad/2º Curso/Analisis y diseños de algoritmos/ADA_boletin_P1/enunciados/04 - boda/tests/T1/901a.in'

#Rute Katerine (no se si se escribe asi (*^_^*)
#filename = '/home/ivan/Universidad/2º Curso/Analisis y diseños de algoritmos/ADA_boletin_P1/enunciados/04 - boda/tests/T1/901a.in'

cases = read_input_from_file(filename) # dictionarys list [{M:Budget, C:number garments, garments: models lists}]


for case in cases:
    #the case are set of garments
    result = voraz(case)  # Result: set of garments opt.
    print(result)
