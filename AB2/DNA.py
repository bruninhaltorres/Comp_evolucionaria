import random
import matplotlib.pyplot as plt

GERACAO = 100
N_POPULACAO = 500
TAXA_MUTACAO = 0.1

# codificação do cromossomo: lista com cadeia de caracteres
DNAs = [
    'ATG', 'ATC', 'ATGC'
]

class Individuo: # Cada indivíduo possui uma sequência de DNA, seu fitness (avaliação da qualidade da sequência) e os métodos para gerar a sequência e calcular o fitness.
    def __init__(self):
        self.sequencias = self.gerar_sequencias()
        self.fitness = self.calcular_fitness()

    def gerar_sequencias(self): # Gera sequências aleatórias para cada DNA definido na lista
        tamanho_max = max(len(seq) for seq in DNAs)
        tamanho_max += tamanho_max // 2

        sequencia = []
        for seq in DNAs:
            seq = list(seq)
            while len(seq) < tamanho_max:
                seq.insert(random.randint(0, len(seq)), '-')
            sequencia.append(seq)

        return sequencia

    def calcular_fitness(self):
        fitness = 0
        tamanho = max(len(seq) for seq in self.sequencias)

        for j in range(tamanho):
            for i in range(len(DNAs)):
                for k in range(i + 1, len(DNAs)):
                    if self.sequencias[i][j] == '-' or self.sequencias[k][j] == '-':
                        continue
                    elif self.sequencias[i][j] == self.sequencias[k][j]:
                        fitness += 1
                    else:
                        fitness -= 1

        return fitness


def crossover(pai, mae): # cruzamento uniforme onde é escolhido aleatoriamente as sequências de DNA dos pais para compor a sequência do filho.
    filho = Individuo()
    sequencia_gerada = []

    for i in range(len(pai.sequencias)): # Escolha de pais de forma aleatória
        if random.random() < 0.5:
            sequencia_gerada.append(pai.sequencias[i])
        else:
            sequencia_gerada.append(mae.sequencias[i])

    filho.sequencias = sequencia_gerada
    filho.fitness = filho.calcular_fitness()

    return filho


def mutacao(novo): # mutação por inserção - criamos uma sequencia de hifens e depois embaralhamos com a cadeia de caracteres
    nova_sequencias = []

    for seq in novo.sequencias:
        seq = list(seq)
        if random.random() < TAXA_MUTACAO:
            contador = seq.count('-')
            seq = [base for base in seq if base != '-']
            random.shuffle(seq)
            seq = seq + ['-'] * contador

        nova_sequencias.append(seq)

    novo.sequencias = nova_sequencias
    novo.fitness = novo.calcular_fitness()

    return novo


def gerar_populacao(): # Gera uma população inicial de indivíduos aleatórios
    populacao = []
    while len(populacao) < N_POPULACAO:
        novo = Individuo()
        populacao.append(novo)

    populacao.sort(key=lambda individual: individual.fitness, reverse=True) # A população é ordenada em ordem decrescente com base no fitness.

    return populacao


def selecao(populacao): # Método da roleta. O fitness de cada indivíduo é utilizado para determinar a probabilidade de seleção. Quanto maior o fitness, maior a chance de ser selecionado.
    fitness_total = sum(individual.fitness for individual in populacao)
    roleta = []
    acumulado = 0

    for individual in populacao:
        probabilidade = individual.fitness / fitness_total
        acumulado += probabilidade
        roleta.append(acumulado)

    r = random.random()
    for i, individual in enumerate(populacao):
        if r <= roleta[i]:
            return individual


def evoluir(populacao): # Seleciona dois indivíduos pais, realiza o crossover e a mutação, gerando um novo indivíduo. Esse processo é repetido até que a nova população tenha o mesmo tamanho da população original
    nova_populacao = populacao.copy()

    for _ in range(N_POPULACAO):
        mae = selecao(populacao)
        pai = selecao(populacao)

        novo = crossover(pai, mae)
        novo = mutacao(novo)

        nova_populacao.append(novo)

    nova_populacao.sort(key=lambda individual: individual.fitness, reverse=True)

    return nova_populacao[:N_POPULACAO]

def plotagem(melhores_individuos): # Plotagem dos melhores fitness das gerações
    plt.plot(range(GERACAO), melhores_individuos, color='red')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.savefig('grafico_fitness.png')

def main():
    melhores_individuos = []

    populacao = gerar_populacao()

    for geracao_atual in range(1, GERACAO + 1): 
        populacao = evoluir(populacao)
        melhor_fitness = populacao[0].fitness
        melhores_individuos.append(melhor_fitness)

    for seq in populacao[0].sequencias:
        print("".join(seq))
    print("Score:", populacao[0].fitness) # A população está ordenada em ordem decrescente com base no fitness, logo o primeiro indivíduo da população é o de melhor resultado

    plotagem(melhores_individuos)

if __name__ == "__main__":
    main()
