from itertools import permutations
from copy import deepcopy
from random import choice, random, choices

from model.ant import Ant


MIN_FITNESS = 0.1  # added this so that I can divide and multiply without errors


class Problem:
    def __init__(self, solution_size=3, q0=0.1, alpha=0.9, beta=0.9, rho=0.05):
        self.__rho = rho
        self.__solution_size = solution_size
        new_sets_steps = list(permutations(list(range(1, self.__solution_size + 1)) * 2))
        new_ants = []
        for x in new_sets_steps:
            a = Ant(self.__solution_size)
            a.add_to_solution(x)
            new_ants.append(a)
        p = list(filter(lambda a: self.fitness_function(a) == MIN_FITNESS, new_ants))
        new_sets_steps = [ant.last() for ant in p]
        self.__steps = [list(step) for step in new_sets_steps]
        self.__beta = beta
        self.__alpha = alpha
        self.__q0 = q0
        self.__best_ant = None
        self.__colony_size = 0
        self.__colony = []
        self.__pheromone_matrices = []
        # generate these matrices
        for _ in range(self.__solution_size * 2):
            self.__pheromone_matrices.append(
                [[1 for _ in range(self.__solution_size + 1)] for _ in range(self.__solution_size + 1)]
            )

    def set_params(self, solution_size=3, q0=0.1, alpha=0.9, beta=0.9, rho=0.05):
        # this is the same as __init__
        self.__rho = rho
        self.__solution_size = solution_size
        new_sets_steps = list(permutations(list(range(1, self.__solution_size + 1)) * 2))
        new_ants = []
        for x in new_sets_steps:
            a = Ant(self.__solution_size)
            a.add_to_solution(x)
            new_ants.append(a)
        p = list(filter(lambda a: self.fitness_function(a) == MIN_FITNESS, new_ants))
        new_sets_steps = [ant.last() for ant in p]
        self.__steps = [list(step) for step in new_sets_steps]
        self.__beta = beta
        self.__alpha = alpha
        self.__q0 = q0
        self.__best_ant = None
        self.__colony_size = 0
        self.__colony = []
        self.__pheromone_matrices = []
        # generate these matrices
        for _ in range(self.__solution_size * 2):
            self.__pheromone_matrices.append(
                [[1 for _ in range(self.__solution_size + 1)] for _ in range(self.__solution_size + 1)]
            )

    def get_params(self):
        return {
            "solution_size": self.__solution_size,
            "q0": self.__q0,
            "alpha": self.__alpha,
            "beta": self.__beta,
            "rho": self.__rho,
        }

    def epoch(self, colony_size):
        self.__colony_size = colony_size
        # create the colony
        self.__colony = [Ant(self.__solution_size) for _ in range(self.__colony_size)]
        for ant in self.__colony:
            ant.add_to_solution(deepcopy(choice(self.__steps)))
        # put the ants in random order
        for _ in range(self.__solution_size):
            for ant in self.__colony:
                self.add_move_to_ant(ant)
        # update the pheromone matrices
        for ant in self.__colony:
            self.update_pheromone_matrix(ant)
        # update the best ant
        if self.__best_ant:
            self.__best_ant = min(min(self.__colony, key=self.fitness_function), self.__best_ant, key=self.fitness_function)
        else:
            self.__best_ant = min(self.__colony, key=self.fitness_function)

    def add_move_to_ant(self, ant):
        next_steps = self.next_steps(ant)
        zero_fitness_moves = list(filter(lambda x: x[1] == MIN_FITNESS, next_steps))
        last_ant_move = ant.last()
        # a dict in which we store key=permutation, value=[fitness, pheromone, weight]
        final = {}
        for step in next_steps:
            t = tuple(step[0])
            final[t] = [step[1], 0]  # fitness, pheromone
        # compute the final
        for matrix, i in zip(self.__pheromone_matrices, range(self.__solution_size * 2)):
            for step in next_steps:
                index_last_move = last_ant_move[i]
                index_new_move = step[0][i]
                pheromone_found = matrix[index_last_move][index_new_move]
                final[tuple(step[0])][1] += pheromone_found
        # compute the weight
        for ke in final.keys():
            fitness = final[ke][0]  # fitness gain on the move
            pheromone = final[ke][1]  # pheromone on that move
            # pheromone^alpha * fitness^beta
            new = (pheromone ** self.__alpha) * ((1 / fitness) ** self.__beta)
#             here some representation problems could appear
#             if you have a large fitness value, 1/fitness^beta -> 0 (very very small values)
            final[ke].append(new)
        # add the move
        if random() < self.__q0:
            # add the best move
            best = max(final.keys(), key=lambda key: final[key][2])
            ant.add_to_solution(list(best))
            ant.fitness = self.fitness_function(ant)
        else:
            # add a random move based on probability
            new = choices(list(final.keys()), weights=[final[k][2] for k in final.keys()], k=1)
            ant.add_to_solution(list(new[0]))
            ant.fitness = self.fitness_function(ant)

    def update_pheromone_matrix(self, ant):
        last_last = ant.last_last()
        last = ant.last()
        fitness = ant.fitness
        for matrix, i in zip(self.__pheromone_matrices, range(self.__solution_size * 2)):
            matrix[last_last[i]][last[i]] *= (1 - self.__rho)
            matrix[last_last[i]][last[i]] += (1.0 / fitness) / (self.__solution_size * 2)

    def next_steps(self, ant):
        # generate a sets of moves for the ant
        # and compute the cost aka fitness of each new step
        new_sets_steps = deepcopy(self.__steps)
        steps_with_costs = []
        for step in new_sets_steps:
            ant.add_to_solution(step)
            new_fitness = self.fitness_function(ant)
            steps_with_costs.append([step, new_fitness])
            ant.pop_last()
        return steps_with_costs

    def get_best_ant(self):
        return self.__best_ant

    def fitness_function(self, ant):
        output = 0
        matrix = ant.solution
        actual_length, final_length = len(matrix[0]), ant.solution_size * 2
        half = final_length // 2
        pairs_dict = {}
        # check for pairs
        for i in range(half):
            for j in range(half):
                if j < actual_length and i < actual_length:
                    pair = (matrix[i][j], matrix[half + j][i])
                    if pair in pairs_dict:
                        output += 1
                        pairs_dict[pair] += 1
                    else:
                        pairs_dict[pair] = 1
        # check for duplicates
        for i in range(half):
            perm_1, perm_2 = [], []
            perm_3, perm_4 = [], []
            for j in range(half):
                j < actual_length and i < actual_length and perm_1.append(matrix[j][i])
                i < actual_length and perm_2.append(matrix[half + j][i])
                j < actual_length and perm_3.append(matrix[i][j])
                j < actual_length and perm_4.append(matrix[half + i][j])
            output += 1 if len(perm_1) != len(set(perm_1)) else 0
            output += 1 if len(perm_2) != len(set(perm_2)) else 0
            output += 1 if len(perm_3) != len(set(perm_3)) else 0
            output += 1 if len(perm_4) != len(set(perm_4)) else 0
        ant.fitness = output + 0.1
        return output + 0.1
