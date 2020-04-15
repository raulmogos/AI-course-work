from problem import CONFIG, Problem
from controller import Controller


class Console:
    def __init__(self, controller):
        self.__controller = controller

    def run(self):
        print('MENU: ')
        print('0  --  exit')
        print('1  -- uninformed search - dfs')
        print('2  -- informed search - greedy bfs')
        choice = int(input('enter your choice: '))
        if choice == 0:
            return
        matrix_size = int(input(f'matrix size [{CONFIG["min"]}, {CONFIG["max"]}): '))
        matrix_size = matrix_size if matrix_size in range(CONFIG['min'], CONFIG['max']) else CONFIG['default']
        problem = Problem(matrix_size)
        self.__controller = Controller(problem)
        if choice == 1:
            print('uninformed search:')
            print(self.__controller.dfs())
        elif choice == 2:
            print('informed search:')
            print(self.__controller.greedy())
