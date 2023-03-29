import random

# Definindo o valor alvo
valor_alvo = 200

# Definindo a taxa de mutação e cruzamento
taxa_mutacao = 0.1
taxa_cruzamento = 0.5

# Definindo o tamanho da população e o número de gerações
tamanho_populacao = 500
num_geracoes = 1000

# Definindo a função de avaliação
def avaliacao(cromossomo):
    # print(cromossomo)
    resultado =  (cromossomo[1] * -1) / cromossomo[0]
    # print(resultado)
    return abs(valor_alvo - resultado)

# Criando a população inicial
populacao = []
for i in range(tamanho_populacao):
    cromossomo = [random.uniform(-1000, 1000), random.uniform(-1000, 1000)]
    # print(cromossomo)
    populacao.append(cromossomo)

# Evoluindo a população por um número de gerações
for geracao in range(num_geracoes):
    # Avaliando a aptidão de cada indivíduo na população
    aptidoes = [avaliacao(cromossomo) for cromossomo in populacao]
    
    # Selecionando os indivíduos mais aptos para reprodução
    selecionados = []
    for i in range(tamanho_populacao // 2):
        pai1 = populacao[random.choices(range(tamanho_populacao), weights=aptidoes)[0]]
        pai2 = populacao[random.choices(range(tamanho_populacao), weights=aptidoes)[0]]
        selecionados.append((pai1, pai2))
    
    # Realizando o cruzamento entre os indivíduos selecionados
    filhos = []
    for pai1, pai2 in selecionados:
        if random.random() < taxa_cruzamento:
            filho1 = [pai1[0], pai2[1]]
            filho2 = [pai2[0], pai1[1]]
            filhos.append(filho1)
            filhos.append(filho2)
    
    # Realizando a mutação nos filhos gerados
    for filho in filhos:
        if random.random() < taxa_mutacao:
            filho[0] += random.uniform(-1, 1)
            filho[1] += random.uniform(-1, 1)
    
    # Combinando a população anterior com os filhos gerados
    populacao = populacao + filhos
    
    # Selecionando os indivíduos mais aptos para a nova população
    aptidoes = [avaliacao(cromossomo) for cromossomo in populacao]
    populacao = [populacao[i] for i in sorted(range(len(aptidoes)), key=lambda k: aptidoes[k])[:tamanho_populacao]]

# Imprimindo a expressão encontrada
print("Expressão encontrada: {:.2f}x + {:.2f}".format(populacao[0][0], populacao[0][1]))
