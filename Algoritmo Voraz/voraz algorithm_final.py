import time

def read_cases_from_file(filename):
    cases = []

    with open(filename, 'r') as file:
        num_cases = int(file.readline().strip())  # Number of cases

        for _ in range(num_cases):
            # Read budget and number of garment types
            budget, num_garments = map(int, file.readline().strip().split())

            garments = []
            # Read garment prices for each type
            for _ in range(num_garments):
                garment_prices = list(map(int, file.readline().strip().split()[1:]))
                garments.append(garment_prices)

            # Append case dictionary with budget, number of garments, and price matrix
            cases.append({'budget': budget, 'num_garments': num_garments, 'garments': garments})

    return cases


def greedy_selection(budget, garments, num_garments):
    selected_prices = []  # List to store selected item prices
    current_total = 0  # Track total of selected prices
    weighted_garments = calculate_weights(garments)

    for _ in range(len(weighted_garments)):
        garment_with_best_weight = select_best_weighted_garment(weighted_garments)
        weighted_garments.remove(garment_with_best_weight)
        garment_prices = garment_with_best_weight[0]

        max_price_per_garment = (budget - current_total) / (num_garments - len(selected_prices))

        max_feasible_price = selection(garment_prices, max_price_per_garment, current_total, budget)

        if max_feasible_price is not None:
            current_total += max_feasible_price
            selected_prices.append(max_feasible_price)
        else:
            break

    if not len(selected_prices) == num_garments: # solution function
        return None

    return sum(selected_prices)

def selection(garment_prices, max_price_per_garment, current_total, budget):
    max_feasible_price = None
    for price in garment_prices:
        if price <= max_price_per_garment:
            if max_feasible_price is None or max_feasible_price < price:
                max_feasible_price = price

    if max_feasible_price is None:
        min_price = min(garment_prices)
        if current_total + min_price <= budget:
            max_feasible_price = min_price

    return max_feasible_price

def calculate_weights(garment_list):
    weighted_list = []
    for prices in garment_list:
        price_range = max(prices) - min(prices)
        model_count = len(prices)
        # Weight calculation: prioritize smaller range and fewer models
        weight = (1 / (model_count + 1)) + (1 / (price_range + 1))
        weighted_list.append((prices, weight))
    return weighted_list


def select_best_weighted_garment(weighted_garments):
    best_weight = None
    best_garment = None
    for garment, weight in weighted_garments:
        if best_weight is None or best_weight < weight:
            best_weight = weight
            best_garment = (garment, weight)
    return best_garment



def validation(out_file, greedy_solution):

    greedy_solution = [greed_sol or 0 for greed_sol in greedy_solution]

    # Read expected solutions from file
    with open(out_file, 'r') as out_file:
        actual_solutions = [
            0 if line.strip() == 'no solution' else int(line.strip())
            for line in out_file
        ]

    percentages = []
    for i in range(len(actual_solutions)):

        if actual_solutions[i] == 0:
            if greedy_solution[i] == 0:
                percentages.append(100.0)  # Both are zero, so perfect match
            else:
                percentages.append(0.0)  # Expected is zero, but actual is not
        else:
            percentage = (greedy_solution[i] * 100) / actual_solutions[i]# Calculate percentage
            percentages.append(round(percentage, 2))


    accuracy = round(sum(percentages) / len(percentages), 2)
    return accuracy, percentages

# List of test cases
test_cases = [
    ('901a.in', '901a.out'),
    ('901b.in', '901b.out'),
    ('901c.in', '901c.out'),
]

for f_in, f_out in test_cases:

    cases = read_cases_from_file(f_in)

    solutions = []
    times = []

    for case in cases:
        time_start = time.time()
        solution = greedy_selection(case['budget'], case['garments'], case['num_garments'])
        time_end = time.time()
        times.append(time_end - time_start)
        solutions.append(solution)
        print(f'Number of garments: {case['num_garments']}, time of execution: {time_end - time_start:.7f} s')
    accuracy, pr = validation(f_out, solutions)
    print(f'Accuracy for {f_in}: {accuracy}, Times: {(sum(times) / len(times)):.7f} s')
    #print(accuracy)