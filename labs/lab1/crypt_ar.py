from random import randint, choice
from copy import deepcopy


DATA = [
    {
        'op_1': 'SEND',
        'op_2': 'MORE',
        'result': 'MONEY',
        'sign': '+'
    }, {
        'op_1': 'TAKE',
        'op_2': 'A',
        'op_3': 'CAKE',
        'result': 'KATE',
        'sign': '+'
    }, {
        'op_1': 'EAT',
        'op_2': 'THAT',
        'result': 'APPLE',
        'sign': '+'
    }, {
        'op_1': 'NEVER',
        'op_2': 'DRIVE',
        'result': 'RIDE',
        'sign': '-'
    },
]

NADA = -1


class Crypt:
    def __init__(self, option=None):
        if option is None or option not in [0, 1, 2, 3]:
            option = randint(0, 3)
        self.__option = option
        self.__data = deepcopy(DATA[self.__option])
        print(self.__data)
        self.__dict = {}
        # initialize out dict
        for item in self.__data['op_1']:
            self.__dict[item] = NADA
        for item in self.__data['op_2']:
            self.__dict[item] = NADA
        for item in self.__data['result']:
            self.__dict[item] = NADA
        if 'op_3' in self.__data.keys():
            for item in self.__data['op_3']:
                self.__dict[item] = NADA

    def print_dict(self):
        print(self.__data)
        for key in self.__dict.keys():
            print(f'{key} -> {self.__dict[key]}')

    def refresh(self):
        for key in self.__dict.keys():
            self.__dict[key] = None

    def generate_random_solution(self):
        assigned = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for key in self.__dict.keys():
            if not self.__dict[key]:
                chosen = choice(assigned)
                assigned.remove(chosen)
                self.__dict[key] = chosen

    def is_solution(self):
        op_1 = 0
        op_2 = 0
        op_3 = 0
        result = 0
        for i in range(len(self.__data['op_1'])):
            char = self.__data['op_1'][i]
            number = self.__dict[char]
            if i == 0 and number == 0:
                return False
            op_1 = op_1 * 10 + number
        for i in range(len(self.__data['op_2'])):
            char = self.__data['op_2'][i]
            number = self.__dict[char]
            if i == 0 and number == 0:
                return False
            op_2 = op_2 * 10 + number
        for i in range(len(self.__data['result'])):
            char = self.__data['result'][i]
            number = self.__dict[char]
            if i == 0 and number == 0:
                return False
            result = result * 10 + number
        if 'op_3' in self.__data:
            for i in range(len(self.__data['op_3'])):
                char = self.__data['op_3'][i]
                number = self.__dict[char]
                if i == 0 and number == 0:
                    return False
                op_3 = op_3 * 10 + number
        my_result = 0
        if self.__data['sign'] == '-':
            my_result = op_1 - op_2
        elif self.__data['sign'] == '+':
            my_result = op_1 + op_2 + op_3
        return my_result == result
