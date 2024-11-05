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

        max_feasible_price = None
        max_price_per_garment = (budget - current_total) / (num_garments - len(selected_prices))

        for price in garment_prices:
            if is_feasible(price, max_price_per_garment):
                if max_feasible_price is None or max_feasible_price < price:
                    max_feasible_price = price

        if max_feasible_price is None:
            min_price = min(garment_prices)
            if current_total + min_price <= budget:
                max_feasible_price = min_price

        if max_feasible_price is not None:
            current_total += max_feasible_price
            selected_prices.append(max_feasible_price)
        else:
            break

    if not is_solution_complete(selected_prices, num_garments):
        return None, None

    return selected_prices, sum(selected_prices)


def is_feasible(price, max_price):
    return price <= max_price


def is_solution_complete(selected_prices, num_garments):
    return len(selected_prices) == num_garments


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



def validation(in_file, out_file, function):

    # Read and process cases
    cases = read_cases_from_file(in_file)
    greedy_solution = [
        0 if (total_price := function(case['budget'], case['garments'], case['num_garments'])[
            1]) is None else total_price
        for case in cases
    ]

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
            percentage = (greedy_solution[i] * 100) / actual_solutions[i]# Calculate percentage normally
            percentages.append(round(percentage, 2))

    accuracy = round(sum(percentages) / len(percentages), 2)
    return percentages, accuracy

# List of test cases
test_cases = [
    ('901a.in', '901a.out'),
    ('901b.in', '901b.out'),
    ('901c.in', '901c.out'),
]

# Execute validation for each test case and print the accuracy
for f_in, f_out in test_cases:
    accuracy = validation(f_in, f_out, greedy_selection)[1]
    print(f'Accuracy for {f_in}: {accuracy:.2f}')