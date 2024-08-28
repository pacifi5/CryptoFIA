import trigrammi
import random
import string 
dizionario_valutazione = trigrammi.trigrams
POPULATION_SIZE = 1200   # Mantiene la diversità con un costo computazionale ragionevole
GENOME_LENGTH = 26      # Fisso per il problema
MUTATION_RATE = 0.4   # Evita troppi cambiamenti casuali, mantenendo comunque la diversità
CROSSOVER_RATE = 0.8   # Combina efficacemente le soluzioni dei genitori
GENERATIONS = 1000 
MAX = 0
BEST_TEXT = 0

def convert(ciphertext, testkey):
    ciphertext = ciphertext.upper()
    testkey = testkey.upper()
    for i in range(len(testkey)):
        plain = chr(i+65).lower()
        ciphertext = ciphertext.replace(testkey[i], plain)
    return ciphertext.upper()

def fitness(testo):
    testo = testo.upper()
    trigrams = [testo[i:i+3] for i in range(len(testo)-1)]
    valutazione = 0
    global MAX
    global BEST_TEXT
    for tri in trigrams:
        if tri in dizionario_valutazione:
            valutazione += dizionario_valutazione[tri]
        if valutazione >= MAX:
            MAX = valutazione
            BEST_TEXT = testo
    return valutazione

def random_genome():
    alfabeto = list(string.ascii_lowercase)
    random.shuffle(alfabeto)
    return ''.join(alfabeto)

def initial_population(populationSize):
    return [random_genome() for _ in range(populationSize-100)]

def select_parent(population, fitness_values):
    paired_population = list(zip(population, fitness_values))
    paired_population.sort(key=lambda x: x[1], reverse=True)
    sorted_population = [genome for genome, _ in paired_population]
    selected_index = random.choices(range(len(sorted_population)), weights=range(len(sorted_population), 0, -1), k=1)[0]
    return sorted_population[selected_index]

def crossover(parent1, parent2):
    if random.random() > CROSSOVER_RATE:
        return parent1, parent2

    crossover_point = random.randint(1, GENOME_LENGTH - 2)
    child1 = list(parent1[:crossover_point])
    child2 = list(parent2[:crossover_point])

    for gene in parent2:
        if gene not in child1:
            child1.append(gene)
    for gene in parent1:
        if gene not in child2:
            child2.append(gene)
    return ''.join(child1), ''.join(child2)

def mutate(genome):
    genome = list(genome)
    if random.random() < MUTATION_RATE + 2 * MAX:
        idx1, idx2 = random.sample(range(GENOME_LENGTH), 2)
        genome[idx1], genome[idx2] = genome[idx2], genome[idx1]
    return ''.join(genome)

def decodifica(ciphertext: str):
    ciphertext = ciphertext.upper()
    ciphertext.replace(" ", "")
    population = initial_population(POPULATION_SIZE)
    #TODO: AGGIUNGI CHIAVI PROBABILI PER ANALISI FREQUENZE


    for generation in range(GENERATIONS):
        fitness_values = [fitness(convert(ciphertext, genome)) for genome in population]
        best_genome = population[fitness_values.index(max(fitness_values))]
        new_population = [best_genome]

        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = new_population[:POPULATION_SIZE]

    fitness_values = [fitness(convert(ciphertext, genome)) for genome in population]
    best_genome = population[fitness_values.index(max(fitness_values))]
    plaintext = convert(ciphertext, best_genome)

    return plaintext, best_genome


if __name__ == '__main__':
    x,y = decodifica("ZqdawhqdkdsydllogdqolouwusdbifaiwuawsduadwsduzwaotzizqdtougxogdifzqdhtowuzdbzDugtwlqlhdordklaottzqwlduaknhzwiuokwlziakozwfzqdkdokdlhoadlikhozkwlziakozwfzqdkdokduilhoadlpdzvdduviksl".replace(" ",""))

    print(BEST_TEXT)