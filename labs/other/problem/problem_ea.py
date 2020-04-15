"""
problem description in pdf

params:
    generational
"""

from random import randint, sample, choice, shuffle, random, seed

from models.individual import Individual


class ProblemEA:
    def __init__(self, probability_of_mutation=1, probability_of_crossover=1, individual_size=3, population_size=100):
        self.__individual_size = individual_size
        self.__no_chromosomes = individual_size * 2
        self.__target = 0
        self.__population_size = population_size
        self.__probability_of_mutation = probability_of_mutation
        self.__probability_of_crossover = probability_of_crossover
        self.__population = None
        self.__best_individual = None
        self.__best_individual_fitness = float('inf')

    def set_params(self, probability_of_mutation=1, probability_of_crossover=1, individual_size=3, population_size=100):
        self.__individual_size = individual_size
        self.__no_chromosomes = individual_size * 2
        self.__target = 0
        self.__population_size = population_size
        self.__probability_of_mutation = probability_of_mutation
        self.__probability_of_crossover = probability_of_crossover
        self.__population = None
        self.__best_individual = None
        self.__best_individual_fitness = float('inf')

    def get_params(self):
        return {
            'best_fitness': self.__best_individual.get_fitness(),
            'individual_size': self.__individual_size,
            'population_size': self.__population_size,
            'probability_of_mutation': self.__probability_of_mutation,
            'probability_of_crossover': self.__probability_of_crossover,
        }

    def initialisation(self):
        self.__generate_population(self.__population_size)

    def __generate_population(self, size):
        self.__population_size = size
        self.__population = [self.__generate_an_individual() for _ in range(self.__population_size)]

    def __generate_an_individual(self):
        # generate a matrix of
        return Individual([
            sample(range(1, self.__individual_size + 1), self.__individual_size)
            for _ in range(self.__no_chromosomes)
        ])

    def is_solution(self, individual):
        return self.fitness_function(individual) == self.__target

    def is_solution_found(self):
        for ind in self.__population:
            if self.is_solution(ind):
                return True
        return False

    def get_solution(self):
        for ind in self.__population:
            if self.is_solution(ind):
                self.__best_individual = ind
                return ind

    def get_population_size(self):
        return self.__population_size

    def no_population(self):
        return self.__population_size == 0

    def __update_best_solution(self):
        for ind in self.__population:
            fit = self.fitness_function(ind)
            if fit < self.__best_individual_fitness:
                self.__best_individual = ind
                self.__best_individual_fitness = fit

    def get_best_solution_so_far(self):
        return self.__best_individual

    def fitness_function(self, individual):
        output = 0
        chrom_list, chrom_length = individual.get_chromosome_list(), individual.length_chromosome()
        individual_length = individual.length()
        pairs_dict = {}
        half = individual_length // 2
        for i in range(half):
            for j in range(chrom_length):
                gene_j_row = chrom_list[i][j]
                gene_j_col = chrom_list[half + j][i]
                pair = (gene_j_row, gene_j_col)
                if pair in pairs_dict:
                    output += 1
                    pairs_dict[pair] += 1
                else:
                    pairs_dict[pair] = 1
        for i in range(half):
            perm_1, perm_2 = [], []
            for j in range(chrom_length):
                perm_1.append(chrom_list[j][i])
                perm_2.append(chrom_list[half + j][i])
            if not self.is_permutation(perm_1):
                output += 1
            if not self.is_permutation(perm_2):
                output += 1
        individual.set_fitness(output)
        return output

    def iteration(self):
        new_population = []
        items = list(range(self.__population_size))
        while items:
            index_p1 = choice(items)
            items.remove(index_p1)
            if len(items) == 0:
                break
            index_p2 = choice(items)
            items.remove(index_p2)
            parent_1 = self.__population[index_p1]
            parent_2 = self.__population[index_p2]
            child_1, child_2 = self.crossover(parent_1, parent_2)
            if child_1:
                new_population += [child_1, child_2]
        self.__population = new_population
        self.__population_size = len(new_population)
        self.__update_best_solution()

    def population(self):
        return self.__population

    def crossover(self, individual_1, individual_2):
        # since the chromosomes are permutation
        # we keep multiplying two permutation in order to get
        # 2 children somehow related to the parents
        if self.__probability_of_crossover < random():
            return None, None
        assert individual_1.length() == individual_2.length()
        length = individual_1.length()
        ind_1_chromosome_list = individual_1.get_chromosome_list()
        ind_2_chromosome_list = individual_2.get_chromosome_list()
        child_1, child_2 = [], []
        for i in range(length):
            index_1, index_2 = randint(0, length - i - 1), randint(0, length - i - 1)
            chrom_1, chrom_2 = ind_1_chromosome_list[index_1], ind_2_chromosome_list[index_2]
            ind_1_chromosome_list.pop(index_1)
            ind_2_chromosome_list.pop(index_2)
            new_chrom_1 = sample(self.multiply_permutations(chrom_1, chrom_2), len(chrom_1))
            new_chrom_2 = sample(self.multiply_permutations(chrom_2, chrom_1), len(chrom_2))
            if randint(0, 1):
                child_1.append(new_chrom_1)
                child_2.append(new_chrom_2)
            else:
                child_1.append(new_chrom_2)
                child_2.append(new_chrom_1)
        return Individual(child_1), Individual(child_2)

    def mutation(self, individual):
        # get a random chromosome
        rand_index = randint(0, individual.length() - 1)
        chrom = individual.get_chromosome(rand_index)
        shuffle(chrom)
        print(rand_index)
        individual.set_chromosome(rand_index, chrom)

    def __permutation_difference(self, permutation):
        # number of transpositions aka ..
        # number of swaps to make in order to turn it into a identity permutation
        swaps = 0
        visited = [0] * (len(permutation) + 1)
        for i in range(len(permutation)):
            item = permutation[i]
            number = 0
            while not visited[item]:
                visited[item] = 1
                item = permutation[item - 1]
                number += 1
            if number:
                swaps += number - 1
        return swaps

    def is_permutation(self, perm):
        p = sorted(perm)
        identity = list(range(1, len(perm) + 1))
        return p == identity

    def multiply_permutations(self, perm_1, perm_2):
        # it is just a way to get one permutation related to perm_1 and perm_2
        assert self.is_permutation(perm_1)
        assert self.is_permutation(perm_2)
        return [perm_1[i - 1] for i in perm_2]

    def __str__(self):
        s = ''
        for ind in self.__population:
            s += str(ind)
            s += '\n'
        return s


# seed(1)

p = ProblemEA(probability_of_crossover=1, probability_of_mutation=1, individual_size=4)
# p.initialisation(100)


# l0 = Individual([[2, 1, 3], [1, 3, 2], [2, 3, 1], [3, 2, 1], [3, 2, 1], [2, 3, 1]])
# l1 = Individual([[3, 2, 1], [2, 1, 3], [2, 1, 3], [2, 3, 1], [2, 3, 1], [2, 1, 3]])
# l2 = Individual([[1, 2, 3], [2, 3, 1], [3, 1, 2], [1, 3, 2], [2, 1, 3], [3, 2, 1]])
# l3 = Individual([
#     [1, 2, 3, 4],
#     [2, 1, 4, 3],
#     [3, 4, 1, 2],
#     [4, 3, 2, 1],
#     [1, 2, 3, 4],
#     [3, 4, 1, 2],
#     [4, 3, 2, 1],
#     [2, 1, 4, 3]
# ])
# #
# print(p.fitness_function(l0))
# print(p.fitness_function(l1))
# print(p.fitness_function(l2))
# print(p.fitness_function(l3))
