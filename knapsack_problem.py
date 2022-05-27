import random

# Starting population
def init_solutions(population_size, solution_size):
    solutions = []
    
    for i in range(population_size):
        solutions.append(get_random_solution(solution_size))
    return solutions

# Generate a random solution of 1's and 0's
def get_random_solution(solution_size):
    return [random.randint(0, 1) for i in range(solution_size)]


# Find the best solution
def optimize(solutions, generations, num_elitists, crossover_rate, mutation_rate, possible_items, max_weight):
    for i in range(generations):
        # print("Generation: " + str(i))
        solutions = evolve(solutions, num_elitists, crossover_rate,
                           mutation_rate, possible_items, max_weight)
        # print(solutions)
    return solutions

# Breed the solutions together
def evolve(solutions, num_elitists, crossover_rate, mutation_rate, possible_items, max_weight):
    new_solutons = []
    
    # Sort by fitness
    solutions.sort(key=lambda x: fitness(
        x, possible_items, max_weight), reverse=True)
    normalized_fitness = normalize_fitness(solutions, possible_items, max_weight)
    
    # Add the best to the next generation
    for i in range(num_elitists):
        new_solutons.append(solutions[i])
    
    # Breed the rest
    while len(new_solutons) < len(solutions):
        # Select parents based on fitness
        parent1 = choose_parent(solutions, normalized_fitness)
        parent2 = choose_parent(solutions, normalized_fitness)
        # Breed the parents
        child1, child2 = breed(parent1, parent2, crossover_rate)
        # Mutate the child
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)
        # Add the child to the next generation
        new_solutons.append(child1)
        new_solutons.append(child2)
    
    return new_solutons


def fitness(solution, possible_items, max_weight):
    total_weight = 0
    total_value = 0

    for i in range(len(solution)):
        if solution[i] == 1:
            total_weight += possible_items[i]["weight"]
            total_value += possible_items[i]["value"]
    
    if total_weight > max_weight:
        return 1e-10
    else:
        return total_value


def normalize_fitness(solutions, possible_items, max_weight):
    total_fitness = 0
    normalized_fitness = []
    
    for solution in solutions:
        total_fitness += fitness(solution, possible_items, max_weight)
    for solution in solutions:
        normalized_fitness.append(fitness(solution, possible_items, max_weight) / total_fitness)
    
    return normalized_fitness


def choose_parent(solutions, normalized_fitness):
    rand = random.random()
    index = 0
    
    while rand > 0:
        rand -= normalized_fitness[index]
        index += 1
    
    index -= 1
    return solutions[index]


def breed(parent1, parent2, crossover_rate):
    child1 = []
    child2 = []
    
    if random.random() < crossover_rate:
        # Perform crossover
        index = random.randint(1, len(parent1) - 1)
        child1 = parent1[:index] + parent2[index:]
        child2 = parent2[:index] + parent1[index:]
    else:
        # Perform mutation
        child1 = parent1
        child2 = parent2
    return child1, child2

def mutate(solution, mutation_rate):
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            solution[i] = 1 if solution[i] == 0 else 0
    return solution

possible_items = [
  # random weights and values
    {"name": "A", "weight": 3, "value": 2},
    {"name": "B", "weight": 2, "value": 3},
    {"name": "C", "weight": 1, "value": 4},
    {"name": "D", "weight": 4, "value": 5},
    {"name": "E", "weight": 5, "value": 6},
    {"name": "F", "weight": 3, "value": 7},
    {"name": "G", "weight": 2, "value": 4},
    {"name": "H", "weight": 1, "value": 5},
    {"name": "I", "weight": 4, "value": 6},
    {"name": "J", "weight": 5, "value": 7},
    {"name": "K", "weight": 3, "value": 8},
    {"name": "L", "weight": 2, "value": 5},
    {"name": "M", "weight": 1, "value": 6},
    {"name": "N", "weight": 4, "value": 7},
    {"name": "O", "weight": 5, "value": 8},
    {"name": "P", "weight": 3, "value": 9},
    {"name": "Q", "weight": 2, "value": 6},
    {"name": "R", "weight": 1, "value": 7},
    {"name": "S", "weight": 4, "value": 8},
    {"name": "T", "weight": 5, "value": 9},
    {"name": "U", "weight": 3, "value": 10},
    {"name": "V", "weight": 2, "value": 7},
    {"name": "W", "weight": 1, "value": 8},
    {"name": "X", "weight": 4, "value": 9},
    {"name": "Y", "weight": 5, "value": 10},
    {"name": "Z", "weight": 3, "value": 11},
]
def max_fitness(solutions, possible_items, max_weight):
    max_fitness = 0
    max_items = []
    for solution in solutions:
        current_fitness = fitness(solution, possible_items, max_weight)
        if current_fitness > max_fitness:
            max_fitness = current_fitness
            max_items = solution
    return max_fitness, max_items

max_weight = 7
generations = 1000
population_size = 300
num_elitists = 2
crossover_rate = 0.8
mutation_rate = 0.05

solutions = init_solutions(population_size, len(possible_items))
print(solutions)
print("Max fitness: " + str(max_fitness(solutions, possible_items, max_weight)[0]))
print("Max items: " + str(max_fitness(solutions, possible_items, max_weight)[1]))
solutions = optimize(solutions, generations, num_elitists, crossover_rate, mutation_rate, possible_items, max_weight)
print("Max fitness: " + str(max_fitness(solutions, possible_items, max_weight)[0]))
print("Max items: " + str(max_fitness(solutions, possible_items, max_weight)[1]))