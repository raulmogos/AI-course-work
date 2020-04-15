from copy import deepcopy
from random import sample
from time import sleep

from models.point import Point


class ProblemHC:
    def __init__(self, point_size=3):
        self.__point_size = point_size
        self.__current_point = None
        self.__target = 0
        self.__solution_found = False

    def set_params(self, point_size=3):
        self.__point_size = point_size
        self.__current_point = None
        self.__target = 0
        self.__solution_found = False

    def initialisation(self):
        self.__current_point = self.__generate_position_point()
        self.__current_point.set_fitness(self.fitness_function(self.__current_point))

    def get_params(self):
        return {
            'best_fitness': self.__current_point.get_fitness(),
            'point_size': self.__point_size
        }

    def __generate_position_point(self):
        return Point(
            [sample(list(range(1, self.__point_size + 1)), self.__point_size) for _ in range(self.__point_size * 2)]
        )

    def get_current_point(self):
        return deepcopy(self.__current_point)

    def is_solution_found(self):
        return self.__solution_found

    def iteration(self):
        self.__current_point.set_fitness(self.fitness_function(self.__current_point))
        neighbours = self.__current_point.generate_neighbours()
        nada = True
        for neigh in neighbours:
            self.fitness_function(neigh)
            if self.__current_point.get_fitness() > neigh.get_fitness():
                self.__current_point = neigh
                nada = False
        self.__solution_found = nada
        self.__current_point.set_fitness(self.fitness_function(self.__current_point))

    def fitness_function(self, point):
        output = 0
        matrix = point.get_inside_list()
        half = len(matrix) // 2
        pair_dict = {}
        for i in range(half):
            for j in range(half):
                item_1 = matrix[i][j]
                item_2 = matrix[half + j][i]
                pair = (item_1, item_2)
                if pair in pair_dict:
                    output += 1
                    pair_dict[pair] += 1
                else:
                    pair_dict[pair] = 1
        for i in range(half):
            perm_1, perm_2 = [], []
            for j in range(half):
                perm_1.append(matrix[j][i])
                perm_2.append(matrix[half + j][i])
            if not self.is_permutation(perm_1):
                output += 1
            if not self.is_permutation(perm_2):
                output += 1
        point.set_fitness(output)
        return output

    def is_permutation(self, perm):
        p = sorted(perm)
        identity = list(range(1, len(perm) + 1))
        return p == identity

    def __str__(self):
        return str(self.__current_point)
