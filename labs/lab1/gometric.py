import numpy as np
import functools
from random import randint, choice, shuffle
from copy import deepcopy

BOARD = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

OBJECTS = [
    [
        [1, 1, 1, 1]
    ],
    [
        [2, 0, 2],
        [2, 2, 2]
    ],
    [
        [0, 3, 0],
        [3, 3, 3]
    ],
    [
        [4, 0, 0],
        [4, 4, 4]
    ],
    [
        [5, 5, 5],
        [0, 0, 5]
    ],
]

board_size = len(BOARD) * len(BOARD[0])
sum_objects_size = 0
for obj in OBJECTS:
    for line in obj:
        for nr in line:
            if nr != 0:
                sum_objects_size += 1
# minimum number of zeros on the board with the objects on it
OPTIM_MIN = board_size - sum_objects_size

class Geometric:
    def __init__(self):
        self.__objects = OBJECTS
        self.__board = BOARD
        self.__height = len(BOARD)
        self.__width = len(BOARD[0])
        self.__size = len(BOARD) * len(BOARD[0])
        print(self.__height)
        print(self.__width)
        print(self.__size)

    def refresh(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__board[i][j] = 0

    def rotated(self, obj, times=1):
        new_obj = deepcopy(obj)
        for i in range(times % 4):
            new_obj = np.rot90(new_obj).tolist()
        return new_obj

    def put_object(self, x, y, obj):
        height, width = len(obj), len(obj[0])
        # verification first
        for i in range(height):
            for j in range(width):
                x_new = x + i
                y_new = y + j
                if x_new >= self.__height or y_new >= self.__width:
                    return
                if self.__board[x_new][y_new] != 0 and obj[i][j] != 0:
                    # there is already another object there
                    return
        for i in range(height):
            for j in range(width):
                x_new = x + i
                y_new = y + j
                # put the non-zero number in the cell
                self.__board[x_new][y_new] = obj[i][j] if obj[i][j] != 0 else self.__board[x_new][y_new]

    def generate_random_solution(self):
        shuffle(self.__objects)
        for obj in self.__objects:
            # poz = choice(self.__get_list_positions_zeros())
            # x, y = poz[0], poz[1]
            x, y = randint(0, self.__height), randint(0, self.__width)
            rotated_obj = self.rotated(obj, times=randint(0, 3))
            self.put_object(x, y, rotated_obj)

    def __get_list_positions_zeros(self):
        lst = []
        for i in range(self.__height):
            for j in range(self.__width):
                lst.append((i, j)) if self.__board[i][j] == 0 else None
        return lst

    def get_zeros(self):
        zeros = 0
        for line in self.__board:
            for item in line:
                if item == 0:
                    zeros += 1
        return zeros

    def is_solution(self):
        zeros = 0
        for line in self.__board:
            for item in line:
                if item == 0:
                    zeros += 1
        return zeros == OPTIM_MIN

    def print_board(self):
        print()
        for line in self.__board:
            print(line)
        print()

    def get_board(self):
        return deepcopy(self.__board)

# ge = Geometric()
# print(ge.rotated(OBJECTS[1], 1))
# ge.print_board()
#
# ge.put_object(3, 0, OBJECTS[1])
# ge.print_board()
# ge.put_object(2, 0, ge.rotated(OBJECTS[2], 2))
# ge.print_board()
#
# ge.put_object(2, 3, ge.rotated(OBJECTS[0]))
# ge.print_board()
#
# ge.put_object(0, 0, OBJECTS[3])
# ge.print_board()
#
# ge.put_object(0, 1, OBJECTS[4])
# ge.print_board()
#
# print(ge.is_solution())
