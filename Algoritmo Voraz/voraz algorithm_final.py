
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
    weight_garments = add_weights(garments)

    for _ in range(len(weight_garments)):
        garment_weight = better_weight(weight_garments)
        weight_garments.remove(garment_weight)
        garment = garment_weight[0]

        max_feasible_value = None

        actual_maximum_prize = (budget - current_sum) / (gar_number - len(s))
        #print(garment, actual_maximum_prize)

        #garment.sort(reverse=True) # Sort prices in descending order
        for model_price in garment:
            if feasible(model_price, actual_maximum_prize):
                if max_feasible_value is None or max_feasible_value < model_price:
                    max_feasible_value = model_price

        if max_feasible_value is None:
            min_price = min(garment)
            if current_sum + min_price <= budget:
                max_feasible_value = min_price

        if max_feasible_value is not None:
            current_sum += max_feasible_value
            #print(max_feasible_value, current_sum)
            s.append(max_feasible_value)
        else: break

    if not solution(s, gar_number):
        return "No se puede encontrar solución"

    return s, sum(s)

def feasible(model_price, actual_maximum_price):

    return model_price <= actual_maximum_price

def solution(s, gar_number):
    return len(s) == gar_number


def add_weights(var_list):
    list_tuple = []
    for value in var_list:
        price_range = max(value) - min(value)
        model_count = len(value)

        # Weight formula prioritizing smaller length and smaller range
        weights = (1 / (model_count + 1)) + (1 / (price_range + 1))
        list_tuple.append((value, weights))
    return list_tuple


def better_weight(weight_garments):
    max_weight = None
    best_garment = None
    for garment in weight_garments:
        if max_weight is None or max_weight < garment[1]:
            max_weight = garment[1]
            best_garment = garment
    return best_garment


for case in cases:
    result = voraz(case['M'], case['garments'], case['C'])
    print(result, case['M'])

