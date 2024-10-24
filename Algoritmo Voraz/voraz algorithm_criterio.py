def read_input_from_file(filename):
    cases = []

    with open(filename, 'r') as file:
        N = int(file.readline().strip()) # N - number of cases

        for _ in range(N):

            line = file.readline().strip().split()
            M, C = [int(x) for x in line] # M - budget, C - number of garments

            garments = []

            for _ in range(C):
                line = list(map(int, file.readline().strip().split()))
                #K = line[0] # number of models for each particular garment ??????????
                prices = line[1:]
                garments.append(prices)  # matrix of garments

            # each case is a dictionary that consists of M, C and garments matrix
            cases.append({'M': M, 'C': C, 'garments': garments})

    return cases # list of dictionaries


filename = '901a.in'
cases = read_input_from_file(filename)

#for case in cases:
#    print(case)

def voraz(budget, garments, gar_number):
    s = []  # Selected items list
    selected_count = 0  # Track how many garments have been selected

    #sorted_garments = sorted(garments, key=lambda x: max(x) - min(x))
    #sorted_garments = sorted(garments, key=lambda x: min(x), reverse=True)
    #sorted_garments = sorted(garments, key=lambda x: 0.5 * (max(x) - min(x)) + 0.5 * min(x), reverse=True)


    # Sort garments by combined criteria
    '''sorted_garments = sorted(garments, key=lambda x:
    (1 / 4 * (max(x) - min(x)) +  # prioritize small range
     1 / 4 * min(x) +  # prioritize largest minimum
     1 / 2 * -len(x)),  # prioritize shortest list
                             reverse=True)'''

    for garment in garments:
        garment.sort(reverse=True) # Sort prices in descending order

        while len(garment) > 0:
            x = garment.pop(0)
            if feasible(s, x, budget, gar_number, garment):
                selected_count += 1
                s.append(x)
                break

    if not solution(s, gar_number):
        return "No se puede encontrar solución"

    return s, sum(s)

def feasible(s, x, budget, gar_number, garment):
    current_sum = sum(s) # Total price of selected garments so far

    if current_sum + x > budget:
        return False

    if len(garment) == 0:
        return True

    return x <= (budget - current_sum) / (gar_number - len(s))

def solution(s, gar_number):
    return len(s) == gar_number

for case in cases:
    result = voraz(case['M'], case['garments'], case['C'])
    print(result)


'''
def voraz(c):
    s = []
    budget = c['M']
    garments = c['garments']

    candidates = []
    for i, models in enumerate(garments):
        for price in models:
            candidates.append((price, i))  # (price, garment_type)


    candidates.sort(reverse=True, key=lambda x: x[0])

    while len(candidates) > 0 and not solucion(s, c['C']):
        x = seleccionar(candidates)
        candidates.remove(x)
        if factible(s, x, budget, c['C']):
            # print(s, sum(p[0] for p in s))
            insertar(s, x)

    if not solucion(s, c['C']):
        return "No se puede encontrar solución"
    return s, sum(p[0] for p in s)

def seleccionar(candidates):
    return candidates[0]
'''

'''def factible(s, x, budget):
    used_types = {garment[1] for garment in s}
    price, garment_type = x
    return (garment_type not in used_types) and (sum(p[0] for p in s) + price <= budget)


def factible(s, x, budget, c):
    used_types = {garment[1] for garment in s}
    price, garment_type = x
    if (garment_type not in used_types) and (sum(p[0] for p in s) + price <= budget):
        if (len(s) <= c/2) and (sum(p[0] for p in s) + price > budget/0.75):
            return False
        return  True
    else:
        return False

def factible(s, x, budget):
    used_types = {garment[1] for garment in s}
    price, garment_type = x
    return (garment_type not in used_types) and (sum(p[0] for p in s) + price <= budget)

def solucion(s, C):
    return len(s) == C

def insertar(s, x):
    s.append(x)
    '''