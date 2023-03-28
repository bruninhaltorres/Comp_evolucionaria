import random

def fitness(individual):
    "Calcula a pontuação de aptidão de uma solução"
    conflicts = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if individual[i] == individual[j] or abs(i - j) == abs(individual[i] - individual[j]):
                conflicts += 1
    return 1 / (conflicts + 1)

def generate_population(pop_size):
    "Gera uma população inicial de soluções aleatórias"
    population = []
    for i in range(pop_size):
        individual = list(range(8))
        random.shuffle(individual)
        population.append(individual)
    return population

def select_parents(population, fitness_fn):
    "Seleciona dois pais usando o método de seleção por torneio"
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    if fitness_fn(parent1) > fitness_fn(parent2):
        return parent1
    else:
        return parent2

def crossover(parent1, parent2, crossover_rate):
    "Executa o crossover de um ponto entre dois pais com uma determinada taxa de cruzamento"
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, 7)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2

def mutate(individual, mutation_rate):
    "Realiza uma mutação em um indivíduo com uma dada taxa de mutação"
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, 7)
            individual[i], individual[j] = individual[j], individual[i]

def genetic_algorithm(pop_size, crossover_rate, mutation_rate, fitness_fn, max_generations=100):
    "Executa o algoritmo genético para resolver o problema das 8 rainhas"
    population = generate_population(pop_size)
    for i in range(max_generations):
        new_population = []
        for j in range(pop_size // 2):
            parent1 = select_parents(population, fitness_fn)
            parent2 = select_parents(population, fitness_fn)
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)
        population = new_population
        best_individual = max(population, key=fitness_fn)
        if fitness_fn(best_individual) == 1:
            return best_individual
        if i % 2 == 0:
            # A cada 2 gerações, ajusta as taxas de cruzamento e mutação
            crossover_rate = max(crossover_rate - 0.05, 0.1)
            mutation_rate = min(mutation_rate + 0.05, 0.5)
    return None

solution = genetic_algorithm(pop_size=100, crossover_rate=0.8, mutation_rate=0.1, fitness_fn=fitness)
print(solution)
