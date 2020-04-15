from random import randint
from math import sqrt
from copy import deepcopy


MATRIX_4X4 = [
    [3, 0, 0, 2],
    [0, 1, 4, 0],
    [1, 2, 0, 4],
    [0, 3, 2, 1]
]

MATRIX_9X9 = [
    [1, 2, 0, 6, 0, 8, 9, 4, 5],
    [5, 8, 0, 0, 0, 9, 7, 0, 1],
    [0, 0, 7, 0, 4, 0, 0, 2, 8],
    [3, 7, 0, 4, 0, 1, 5, 0, 0],
    [6, 0, 0, 5, 8, 0, 0, 7, 4],
    [0, 0, 8, 0, 9, 2, 0, 1, 3],
    [8, 0, 6, 0, 2, 0, 1, 0, 0],
    [0, 0, 9, 8, 0, 0, 0, 3, 6],
    [7, 4, 5, 3, 0, 6, 0, 9, 0],
]


class Board:
    def __init__(self, size=4):
        if size not in [4, 9]:
            raise ValueError('size must be 4 or 9')
        self.__size = size
        # self.__matrix = [[0 for _ in range(size)] for _ in range(size)]
        self.__matrix = None
        self.__generated = [[0 for _ in range(size)] for _ in range(size)]

    def is_valid_position(self, x, y, value):
        self.__validate(x, y)
        for i in range(self.__size):
            if i != y:
                if self.__matrix[x][i] == value:
                    return False
            if i != x:
                if self.__matrix[i][y] == value:
                    return False
        x_min, x_max, y_min, y_max = self.get_sub_matrix(x, y)
        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if i == x and j == y:
                    pass
                else:
                    if self.__matrix[i][j] == value:
                        return False
        return True

    def __validate(self, x, y):
        if x not in range(0, self.__size) or y not in range(0, self.__size):
            raise ValueError(f'x or y not in range [0, {self.__size - 1}]')

    def put_value(self, x, y, value):
        self.__matrix[x][y] = value

    def delete_value(self, x, y):
        self.__validate(x, y)
        self.__matrix[x][y] = 0

    def get_value(self, x, y):
        self.__validate(x, y)
        return self.__matrix[x][y]

    def get_sub_matrix(self, x, y):
        x_min = x
        x_max = x + 1
        y_min = y
        y_max = y + 1
        sq = int(sqrt(self.__size))
        while x_min % sq != 0:
            x_min -= 1
        while x_max % sq != 0:
            x_max += 1
        while y_min % sq != 0:
            y_min -= 1
        while y_max % sq != 0:
            y_max += 1
        return x_min, x_max, y_min, y_max

    # generates a VALID random initial state of the sudoku board
    def generate(self):
        self.__matrix = deepcopy(MATRIX_4X4) if self.__size == 4 else deepcopy(MATRIX_9X9)
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j] != 0:
                    self.__generated[i][j] = 1

    # random search
    def find_random_solution(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j] == 0 and self.__generated[i][j] == 0:
                    self.__matrix[i][j] = randint(1, self.__size)

    # put 0 in all places except those generated in initial state
    def refresh_board(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__generated[i][j] is 0:
                    self.__matrix[i][j] = 0

    def is_solution(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j] == 0:
                    return False
                else:
                    if not self.is_valid_position(i, j, self.__matrix[i][j]):
                        return False
        return True

    @staticmethod
    def __is_perfect_square(number):
        return int(sqrt(number)) ** 2 == number

    def print_matrix(self):
        print()
        for line in self.__matrix:
            print(line)
        print()


# bo = Board(9)
# bo.generate()
# bo.print_matrix()
#
# bo.put_value(0, 1, 4)
# bo.put_value(0, 2, 1)
#
# bo.put_value(1, 0, 2)
# bo.put_value(1, 3, 3)
#
# bo.put_value(2, 2, 3)
#
# bo.put_value(3, 0, 4)
#
#
# bo.print_matrix()
# print(bo.is_solution())

