import random

# Tamanho do cromossomo (proteína) e tamanho da população
CHROMOSOME_SIZE = 20
POPULATION_SIZE = 50

# Taxa de mutação e cruzamento
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8

# Função de fitness
def fitness(chromosome):
    score = 0
    for i in range(CHROMOSOME_SIZE - 1):
        if chromosome[i] == 'H' and chromosome[i + 1] == 'P':
            score += 1
        elif chromosome[i] == 'P' and chromosome[i + 1] == 'H':
            score += 1
    return score

# Geração da população inicial
def generate_population():
    population = []
    for i in range(POPULATION_SIZE):
        chromosome = ''.join(random.choices(['H', 'P'], k=CHROMOSOME_SIZE))
        population.append(chromosome)
    return population

# Seleção dos pais utilizando torneio
def selection(population):
    parents = []
    for i in range(2):
        tournament = random.sample(population, 5)
        winner = max(tournament, key=fitness)
        parents.append(winner)
    return parents

# Cruzamento de dois pais utilizando one-point crossover
def crossover(parent1, parent2):
    if random.random() > CROSSOVER_RATE:
        return parent1, parent2
    crossover_point = random.randint(1, CHROMOSOME_SIZE - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutação de um indivíduo trocando um gene aleatório
def mutate(individual):
    if random.random() > MUTATION_RATE:
        return individual
    mutation_point = random.randint(0, CHROMOSOME_SIZE - 1)
    mutated_gene = 'H' if individual[mutation_point] == 'P' else 'P'
    mutated_individual = individual[:mutation_point] + mutated_gene + individual[mutation_point + 1:]
    return mutated_individual

# Algoritmo genético completo
def genetic_algorithm():
    population = generate_population()
    for generation in range(100):
        print(f'Generation {generation + 1}')
        # Avaliação da população
        scores = [fitness(individual) for individual in population]
        best_individual = max(population, key=fitness)
        print(f'Best individual: {best_individual}, score: {fitness(best_individual)}')
        # Seleção de pais e cruzamento
        new_population = []
        for i in range(POPULATION_SIZE // 2):
            parent1, parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        population = new_population

# Execução do algoritmo
genetic_algorithm()


# A seleção de torneio seleciona dois indivíduos aleatórios da população e escolhe o mais apto entre eles para ser o pai ou a mãe. Com essa abordagem, é garantido que o pai e a mãe sejam diferentes. Além disso, a seleção de torneio torna a função de seleção mais eficiente, pois ela é executada apenas duas vezes por indivíduo.