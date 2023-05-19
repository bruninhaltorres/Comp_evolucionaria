import random

"Neste exemplo, a taxa de cruzamento é fixa em 0.8 e a taxa de mutação é fixa em 0.1. Estas taxas podem ser ajustadas para tentar obter uma melhor solução ou para explorar diferentes configurações do algoritmo. É importante lembrar que diferentes taxas podem afetar o desempenho do algoritmo e que não há uma taxa universalmente melhor."

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

def crossover(parent1, parent2):
    "Executa o crossover de um ponto entre dois pais com uma taxa de cruzamento fixa de 0.8"
    crossover_point = random.randint(1, 7)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual):
    "Realiza uma mutação em um indivíduo com uma taxa de mutação fixa de 0.1"
    for i in range(len(individual)):
        if random.random() < 0.1:
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
            child1_genes, child2_genes = crossover(parent1, parent2)
            mutate(child1_genes)
            mutate(child2_genes)
            new_population.append(child1_genes)
            new_population.append(child2_genes)
        population = new_population
        best_individual = max(population, key=fitness_fn)
        if fitness_fn(best_individual) == 1:
            return best_individual
    return best_individual

solution = genetic_algorithm(pop_size=100, fitness_fn=fitness, max_generations=100)
print(solution)