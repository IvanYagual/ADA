
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

                prices = line[1:]
                garments.append(prices)  # matrix of garments

            # each case is a dictionary that consists of M, C and garments matrix
            cases.append({'M': M, 'C': C, 'garments': garments})

    return cases # list of dictionaries


filename = '901a.in'
cases = read_input_from_file(filename)

def voraz(budget, garments, gar_number):
    s = []  # Selected items list
    current_sum = 0 # Track the current sum of selected prices

    sorted_garments = sorted(garments, key=lambda x:
    (1 / 8 * (max(x) - min(x)) +  # prioritize small range
     1 / 8 * max(x) +  # prioritize biggest maximum
     3 / 4 * -len(x)),  # prioritize shortest list
                             reverse=True)

    for garment in sorted_garments:

        max_feasible_value = None

        actual_maximum_prize = (budget - current_sum) / (gar_number - len(s))

        #garment.sort(reverse=True) # Sort prices in descending order
        for model_price in garment:
            if feasible(model_price, garment, actual_maximum_prize, current_sum, budget, max_feasible_value):
                if max_feasible_value is None or max_feasible_value < model_price:
                    max_feasible_value = model_price
        if max_feasible_value is not None:
            current_sum += max_feasible_value
            s.append(max_feasible_value)
        else: break

    if not solution(s, gar_number):
        return "No se puede encontrar solución"

    return s, sum(s)

def feasible(model_price, garment, actual_maximum_prize, current_sum, budget, max_feasible_value):

    if current_sum + model_price > budget:
        return False

    if model_price == garment[-1] and max_feasible_value is None:
        return True

    return model_price <= actual_maximum_prize

def solution(s, gar_number):
    return len(s) == gar_number

for case in cases:
    result = voraz(case['M'], case['garments'], case['C'])
    print(result, case['M'])

'''sorted_garment = sorted(garment, key=lambda x:
        3 / 4 * abs(1 - actual_maximum_prize/x) + 1 / 4 * -x)'''
'''# Sort garments by combined criteria
    sorted_garments = sorted(garments, key=lambda x:
    (1 / 8 * (max(x) - min(x)) +  # prioritize small range
     1 / 8 * max(x) +  # prioritize biggest maximum
     3 / 4 * -len(x)),  # prioritize shortest list
                             reverse=True)'''

'''def voraz(budget, garments, gar_number):
    s = []  # Selected items list
    current_sum = 0 # Track the current sum of selected prices
    max_feasible_value = None

    for garment in sorted_garments:
        actual_maximum_prize = (budget - current_sum) / (gar_number - len(s))
        garment.sort(reverse=True) # Sort prices in descending order
        selected_garment = False
        for model_price in garment:
            if feasible(model_price, garment, actual_maximum_prize, current_sum, budget):
                current_sum += model_price
                s.append(model_price)
                selected_garment = True
                #print (model_price)
                break
        if not selected_garment: break

    if not solution(s, gar_number):
        return "No se puede encontrar solución"

    return s, sum(s)

def feasible(model_price, garment, actual_maximum_prize, current_sum, budget):

    if current_sum + model_price > budget:
        return False

    if model_price == garment[-1]:
        return True

    return model_price <= actual_maximum_prize
'''