import math


class Ant:
    def __init__(self, solution_size):
        self.__solution_size = solution_size
        self.__solution = [[] for _ in range(self.__solution_size * 2)]
        self.__fitness = math.inf

    @property
    def solution_size(self):
        return self.__solution_size

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness):
        self.__fitness = fitness

    @property
    def solution(self):
        return self.__solution

    def add_to_solution(self, item):
        for i in range(len(item)):
            self.__solution[i].append(item[i])
        if len(self.__solution[0]) > self.__solution_size:
            for item in self.__solution:
                item.pop(0)

    def has_solution(self):
        return self.__solution_size == len(self.__solution[0])

    def pop_last(self):
        for item in self.__solution:
            item.pop(-1)

    def last(self):
        return [item[-1] for item in self.__solution]

    def last_last(self):
        return [item[-2] for item in self.__solution]

    def __str__(self):
        return str(self.__solution) + ' ' + str(self.__fitness)


# a = Ant(3)
# a.add_to_solution([1,2,3,1,2,3])
# a.add_to_solution([3,3,1,3,3,3])
# print(a.last())
# print(a.last_last())
