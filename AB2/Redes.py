
import random
import numpy as np

CHROMOSOME_LENGHT = 4

MUTATION_RATE = 0.02
MUTATION_RANGE = 10

POPULATION_SIZE = 10
TOTAL_GENERATIONS = 100

GSM_VOICE_LIMITS = [0, 125]
GSM_DATA_LIMITS = [0, 30]

WCDMA_VOICE_LIMITS = [0, 150]
WCDMA_DATA_LIMITS = [0, 80]

VOICES_LIMIT = 275
DATA_LIMIT = 110

DESIRED_COST = 0.0

population = []
currentGeneration = 1

bestFitnessOfEachGeneration = []

def GetUserVoices(voices): # Calcula o percentual de uso das vozes
  totalVoices = sum(voices)

  return 1 - (totalVoices / 275)

def GetUserData(data): # Calcula o percentual de uso dos dados
  totalData = sum(data)
  
  return 1 - (totalData / 110)

def GetGSMCost(voice, data): #  Calcula o custo para o uso da rede GSM com base nos valores de voz e dados fornecidos.
  return abs(- 30 + data + 6/25*voice)

def GetWCDMACost(voice, data): # Calcula o custo para o uso da rede WCDMA com base nos valores de voz e dados fornecidos. 
  return abs(-80 + data + 8/15*voice)

def GetCost(userVoice, userData, costGSM, costWCDMA): #  Calcula o custo total levando em consideração os custos e valores
  return (pow(costGSM, 2) + pow(costWCDMA, 2)) * userVoice * userData

class Individual: # Cada indivíduo vai possuir um cromossomo (representado como uma lista de 4 valores), bem como um valor de aptidão (fitness_score) calculado com base em seu cromossomo.
  
  def __init__(self):
    self.chromosome = self.InitializeChromosome()
    self.fitness_score = self.fitness()

  def InitializeChromosome(self): # codificação do cromossomo: lista de tamanho 4. dois primeiros elementos representam as características relacionadas à rede GSM (voz e dados) e os dois últimos elementos representam as características relacionadas à rede WCDMA (voz e dados).
    GSMvoice = random.uniform(GSM_VOICE_LIMITS[0], GSM_VOICE_LIMITS[1])
    GSMdata = random.uniform(GSM_DATA_LIMITS[0], GSM_DATA_LIMITS[1])
    
    WCDMAvoice = random.uniform(WCDMA_VOICE_LIMITS[0], WCDMA_VOICE_LIMITS[1])
    WCDMAdata = random.uniform(WCDMA_DATA_LIMITS[0], WCDMA_DATA_LIMITS[1])

    return [80, 120, 15, 50]

  def fitness(self):
    # pega os respectivos números de voz e dados
    voices = self.chromosome[0:2]
    data = self.chromosome[2:4]
    
    #soma as duas posições de cada (voz e dados)
    userVoices = GetUserVoices(voices)
    userData = GetUserData(data)
    
    #faz o custo de voz e custo de dados (esses cálculos são utilizando fórmulas do tcc)
    costGSM = GetGSMCost(voices[0], data[0])
    costWCDMA = GetWCDMACost(voices[1], data[1])

    #faz o cálculo do custo total também utilizando funções do tcc
    cost = GetCost(userVoices, userData, costGSM, costWCDMA)
    
    #quanto menor o fitness, melhor
    return cost

  def IsValid(self):
    sumVoices = sum(self.chromosome[0:2])
    sumData = sum(self.chromosome[2:4])

    if sumVoices > VOICES_LIMIT:
      return False

    if sumData > DATA_LIMIT:
      return False

    return True

def Crossover(parent1, parent2): # Cruzamento aritmético. Durante o cruzamento entre dois pais, cada posição do cromossomo do filho resultante é calculada como a média aritmética dos valores correspondentes nos cromossomos dos pais.

  child = Individual()
  for i in range(0, CHROMOSOME_LENGHT):
    child.chromosome[i] = (parent1.chromosome[i] + parent2.chromosome[i]) / 2

  return child

def Mutation(individual): # Mutação gaussiana. Em cada posição do cromossomo de um indivíduo, a mutação ocorre com uma probabilidade determinada pela taxa de mutação (MUTATION_RATE), ou seja, itero sobre cada posição e se ela for menor que a taxa de mutação eu pego um número gaussiano e somo a ela
  for i in range(0, CHROMOSOME_LENGHT):
    if random.random() < MUTATION_RATE:
      individual.chromosome[i] += random.gauss(-MUTATION_RANGE, MUTATION_RANGE)

  return individual

def GeneratePopulation(): # vou gerando indivíduos aleatórios de acordo com o número da POPULATION_SIZE
  population = []

  while len(population) <= POPULATION_SIZE:
    individual = Individual()

    if individual.IsValid():
      population.append(individual)

  return population

def roulette_selection(): # Realiza a seleção de pais através do método da roleta. A probabilidade de seleção de cada indivíduo é proporcional à sua aptidão.
  global population

  total_fitness = sum(1/individual.fitness_score for individual in population)
  fitnesses = [1/individual.fitness_score for individual in population]
  probabilities = [fitness/total_fitness for fitness in fitnesses]

  return random.choices(population, probabilities, k=2)

def Evolve(): # gero filhos pelo método da roleta, depois aplico o cruzamento, mutação e seleciono os individuos mais aptos até que eu encontre o custo que quero ou que o número de gerações esgote
  global population, currentGeneration, bestFitnessOfEachGeneration

  while population[0].fitness_score >= DESIRED_COST and currentGeneration < TOTAL_GENERATIONS:
    while len(population) < POPULATION_SIZE*2:
      parent1, parent2 = roulette_selection()

      child = Crossover(parent1, parent2)
      child = Mutation(child)

      child.fitness_score = child.fitness()

      if(child.IsValid()):
        population.append(child)

    population.sort(key=lambda x: x.fitness_score)
    population = population[:POPULATION_SIZE]

    bestFitnessOfEachGeneration.append(population[0].fitness_score)
    currentGeneration += 1

def PrintBestIndividual(): # Imprime o melhor indivíduo encontrado.
  global population, currentGeneration

  bestIndividual = population[0]
  print("Chromosome: ", bestIndividual.chromosome)
  print("Fitness: ", "%.8f" % bestIndividual.fitness_score)
  print("Current Generation: ", currentGeneration, "\n")

def AccessNetworkSelection(): # Função principal que coordena a execução do algoritmo genético.
  global population, currentGeneration, bestFitnessOfEachGeneration
  
  population = GeneratePopulation()
  population.sort(key=lambda x: x.fitness_score)

  bestFitnessOfEachGeneration.append(population[0].fitness_score)

  if(population[0].fitness_score < 0):
    print("Chromosome: ", population[0].chromosome)
    print("Fitness: ", "%.8f" % population[0].fitness_score)
    print("Current Generation: ", currentGeneration)
    return population[0], population[0].fitness_score, bestFitnessOfEachGeneration

  Evolve()
  PrintBestIndividual()

  return population[0], population[0].fitness_score, bestFitnessOfEachGeneration

    
if __name__ == '__main__':
  AccessNetworkSelection()
