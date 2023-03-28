import random

# Define o tamanho da população e o número de gerações
POPULATION_SIZE = 50
GENERATIONS = 100

# Define a taxa de mutação e cruzamento
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8

# Define o tamanho da sequência de aminoácidos
SEQUENCE_SIZE = 20

# Define a sequência de aminoácidos
SEQUENCE = "HPHPHPHPPHH"

# Define a função de fitness
def fitness_function(sequence):
    # Cálculo da pontuação de fitness
    score = 0
    for i in range(len(sequence)-1):
        for j in range(i+1,len(sequence)):
            if abs(i-j) > 2:
                score += 1 if sequence[i]=="H" and sequence[j]=="H" else 0
                score += 1 if sequence[i]=="P" and sequence[j]=="P" else 0
                score += 1 if sequence[i]=="H" and sequence[j]=="P" else 0
    return score

# Define a função para criar a população inicial
def create_population(size):
    population = []
    for i in range(size):
        sequence = ''.join(random.sample(SEQUENCE, SEQUENCE_SIZE))
        population.append(sequence)
    return population

# Define a função de seleção de pais por torneio
def selection(population):
    parents = []
    for i in range(2):
        tournament = random.sample(population, 5)
        winner = max(tournament, key=lambda x: fitness_function(x))
        parents.append(winner)
    return parents

# Define a função de crossover
def crossover(parents):
    if random.random() < CROSSOVER_RATE:
        index = random.randint(1, SEQUENCE_SIZE-1)
        child1 = parents[0][:index] + parents[1][index:]
        child2 = parents[1][:index] + parents[0][index:]
        return child1, child2
    else:
        return parents

# Define a função de mutação
def mutation(individual):
    if random.random() < MUTATION_RATE:
        index = random.randint(0, SEQUENCE_SIZE-1)
        new_char = random.choice(SEQUENCE)
        individual = individual[:index] + new_char + individual[index+1:]
    return individual

# Cria a população inicial
population = create_population(POPULATION_SIZE)

# Executa o algoritmo genético por um número de gerações especificado
for generation in range(GENERATIONS):
    print("Generation", generation+1)
    
    # Avalia a população atual
    population_fitness = [(individual, fitness_function(individual)) for individual in population]
    population_fitness = sorted(population_fitness, key=lambda x: x[1], reverse=True)
    best_individual, best_fitness = population_fitness[0]
    print("Best individual:", best_individual, "Fitness:", best_fitness)
    
    # Seleciona os pais para a próxima geração
    new_population = []
    for i in range(POPULATION_SIZE//2):
        parents = selection(population)
        children = crossover(parents)
        child1 = mutation(children[0])
        child2 = mutation(children[1])
        new_population.extend([child1, child2])
    population = new_population
