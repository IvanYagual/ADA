import time



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


filename = 'tests/T1/901a.in'
cases = read_input_from_file(filename)

#for case in cases:
#    print(case)

def voraz(budget, garments, gar_number):
    s = []  # Selected items list
    selected_count = 0  # Track how many garments have been selected
    current_sum = 0 # Track the current sum of selected prices

    #sorted_garments = sorted(garments, key=lambda x: max(x) - min(x))
    #sorted_garments = sorted(garments, key=lambda x: max(x), reverse=True)
    #sorted_garments = sorted(garments, key=lambda x: len(x), reverse=True)

    print(garments)
    print(max(garments))
    # Sort garments by combined criteria
    sorted_garments = sorted(garments, key=lambda x:
    (1 / 8 * -(max(x) - min(x)) +  # prioritize small range
     1 / 8 * max(x) +  # prioritize biggest maximum
     3 / 4 * len(x)),  # prioritize shortest list
                             reverse=True)
    print(sorted_garments)

    for garment in sorted_garments:
        garment.sort(reverse=True) # Sort prices in descending order
        #print(garment)

        while len(garment) > 0:
            model_price = garment.pop(0)
            if feasible(model_price, budget, gar_number, garment, selected_count, current_sum):
                selected_count += 1
                current_sum += model_price
                s.append(model_price)
                #print (model_price)
                break
    if not solution(s, gar_number):
        return "No se puede encontrar solución"

    return s, sum(s)

def feasible(model_price, budget, gar_number, garment, selected_count, current_sum):

    if current_sum + model_price > budget:
        return False

    if len(garment) == 0:
        return True

    return model_price <= (budget - current_sum) / (gar_number - selected_count)


def solution(s, gar_number):
    return len(s) == gar_number




def execution_time(budget: int, garments: list[list], gar_number: int) -> tuple[int, int]:
    start_time = time.time()
    result = voraz(budget, garments, gar_number)
    end_time = time.time()
    exec_time = end_time - start_time
    return result, exec_time



if __name__ == '__main__':

    filename = 'tests/T1/901a.in'
    cases = read_input_from_file(filename)

    for case in cases:
        result, exec_time = execution_time(case['M'], case['garments'], case['C'])
        print(result, case['M'])

