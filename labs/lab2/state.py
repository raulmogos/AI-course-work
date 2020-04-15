from texttable import Texttable
from copy import deepcopy


class State:
    def __init__(self, n=8):
        self.__n = n
        self.__ones = 0
        self.__matrix = [[0 for _ in range(n)] for _ in range(n)]

    def occupy(self, x, y):
        self.__ones += 1
        self.__matrix[x][y] = 1

    def free(self, x, y):
        self.__ones -= 1
        self.__matrix[x][y] = 0

    def get(self):
        return deepcopy(self.__matrix), self.__n

    def clone(self):
        return deepcopy(self)

    def set(self, matrix):
        if len(matrix) != self.__n or len(matrix[0]) != self.__n:
            assert False
        self.__matrix = matrix

    def get_density(self):
        return self.__ones

    def get_list_occupied(self):
        return [(x, y) for x in range(self.__n) for y in range(self.__n) if self.__matrix[x][y]]

    def __str__(self):
        table = Texttable()
        for line in self.__matrix:
            table.add_row(['Q' if x else ' ' for x in line])
        return table.draw()

    def __eq__(self, other):
        if len(self.__matrix) != len(other.__matrix) or len(self.__matrix[0]) != len(other.__matrix[0]):
            return False
        for i in range(self.__n):
            for j in range(self.__n):
                if self.__matrix[i][j] != other.__matrix[i][j]:
                    return False
        return True
