from board import Board
from crypt_ar import Crypt
from gometric import Geometric
import time


# 160 SECONDS
MAX_TRIALS = 10 ** 6


def sudoku():
    print('sudoku')
    size = int(input('size of the board: '))
    no_of_trials = int(input('number of trials: '))
    board = Board(size)
    board.generate()
    board.print_matrix()
    found = False
    start = time.time()
    while no_of_trials:
        board.find_random_solution()
        # time.sleep(1)
        # board.print_matrix()
        # print()
        if board.is_solution():
            print('found one solution')
            board.print_matrix()
            found = True
            break
        board.refresh_board()
        print(no_of_trials)
        no_of_trials -= 1
    end = time.time()
    print(end - start)
    if not found:
        print('no solution was found')


def arithmetic():
    print('crypto arithmetic')
    choice = int(input('enter 0, 1, 2, 3'))
    no_of_trials = int(input('number of trials: '))
    crypt = Crypt(choice)
    found = False
    while no_of_trials:
        crypt.generate_random_solution()
        # time.sleep(1)
        # crypt.print_dict()
        # print()
        if crypt.is_solution():
            print('solution found')
            crypt.print_dict()
            found = True
            break
        crypt.refresh()
        print(no_of_trials)
        no_of_trials -= 1
    if not found:
        print('no solution was found')


def geometric():
    print('geometric objects')
    no_of_trials = int(input('number of trials: '))
    geom = Geometric()
    found = False
    min_zeros = 99
    board = []
    while no_of_trials:
        geom.generate_random_solution()
        # time.sleep(1)
        # geom.print_board()
        # print()
        if min_zeros >= geom.get_zeros():
            min_zeros = geom.get_zeros()
            board = geom.get_board()
        if geom.is_solution():
            print('solution found')
            geom.print_board()
            found = True
            break
        geom.refresh()
        print(no_of_trials)
        no_of_trials -= 1
    if not found:
        for line in board:
            print(line)
        print(min_zeros)
        print('no solution was found')


def main():
    while True:
        print('menu')
        print('1 - sudoku')
        print('2 - arithmetic operations')
        print('3 - geometric objects')
        print('4 - exit')
        choice = int(input('enter your choice:'))
        if choice == 1:
            sudoku()
        elif choice == 2:
            arithmetic()
        elif choice == 3:
            geometric()
        elif choice == 4:
            return
        else:
            print('invalid option')


main()
