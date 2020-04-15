import itertools
from random import sample


class Permutation:
    def __init__(self, size):
        self.__size = size
        self.__identity = list(range(1, self.__size + 1))
        self.__perm = self.__generate()

    @property
    def permutation(self):
        return self.__perm

    @permutation.setter
    def permutation(self, perm):
        self.__perm = perm
        self.__size = len(perm)

    def __generate(self):
        return sample(self.__identity, self.__size)

    @staticmethod
    def permutation_difference(perm):
        # returns the number of swaps needed to get to an identity permutation
        swaps, size = 0, len(perm)
        visited = [0] * (size + 1)
        for i in range(size):
            item, number = perm[i], 0
            while not visited[item]:
                visited[item] = 1
                item = perm[item - 1]
                number += 1
            if number:
                swaps += number - 1
        return swaps

    @staticmethod
    def manhattan_distance(perm_1, perm_2):
        return sum(abs(item_1 - item_2) for item_1, item_2 in zip(perm_1.__perm, perm_2.__perm))

    @staticmethod
    def swap_distance(perm_1, perm_2):
        hack = [(item_1, item_2) for item_1, item_2 in zip(perm_1.__perm, perm_2.__perm)]
        hack_2 = sorted(hack, key=lambda x: x[0])
        hack_3 = [item[1] for item in hack_2]
        return Permutation.permutation_difference(hack_3)

    @staticmethod
    def is_permutation(perm):
        return sorted(perm) == list(range(1, len(perm) + 1))

    @staticmethod
    def generate_permutations(number):
        return list(itertools.permutations(range(1, number + 1)))

    def __eq__(self, other):
        return self.__perm == other.__perm

    def __str__(self):
        return str(self.__perm)
