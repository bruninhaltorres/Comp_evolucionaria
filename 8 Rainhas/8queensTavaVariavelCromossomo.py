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
        population.append({"genes": individual, "crossover_rate": random.uniform(0.5, 0.9), "mutation_rate": random.uniform(0.01, 0.1)})
    return population

def select_parents(population, fitness_fn):
    "Seleciona dois pais usando o método de seleção por torneio"
    parent1 = random.choice(population)["genes"]
    parent2 = random.choice(population)["genes"]
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

def genetic_algorithm(pop_size, fitness_fn, max_generations):
    "Executa o algoritmo genético para resolver o problema das 8 rainhas"
    population = generate_population(pop_size)
    for i in range(max_generations):
        new_population = []
        for j in range(pop_size // 2):
            parent1 = select_parents(population, fitness_fn)
            parent2 = select_parents(population, fitness_fn)
            child1_genes, child2_genes = crossover(parent1, parent2, min(parent1["crossover_rate"], parent2["crossover_rate"]))
            mutate(child1_genes, min(parent1["mutation_rate"], parent2["mutation_rate"]))
            mutate(child2_genes, min(parent1["mutation_rate"], parent2["mutation_rate"]))
            child1 = {"genes": child1_genes, "crossover_rate": random.uniform(0.5, 0.9), "mutation_rate": random.uniform(0.01, 0.1)}
            child2 = {"genes": child2_genes, "crossover_rate": random.uniform(0.5, 0.9), "mutation_rate": random.uniform(0.01, 0.1)}
            new_population.append(child1)
            new_population.append(child2)
        population = new_population
        best_individual = max(population, key=fitness_fn)
        if fitness_fn(best_individual) == 1:
            return best_individual
    return best_individual

solution = genetic_algorithm(pop_size=100, fitness_fn=fitness, max_generations=100)
print(solution)