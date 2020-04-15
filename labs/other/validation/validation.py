import json
import matplotlib.pyplot as plt
import numpy as np


FILE = 'results.json'


class Validation:
    def __init__(self):
        self.__FILE = FILE
        self.__seed_file = 'validation/seed.txt'
        self.__data = {
            'ea': [],
            'hc': []
        }

    def store_file(self, data):
        with open('validation/' + self.__FILE, 'r') as file:
            self.__data = json.loads(file.read())
        self.__data[data['problem_name']].append(data['data'])
        with open('validation/' + self.__FILE, 'w') as file:
            json.dump(self.__data, file, indent=4)
        pass

    def get_data(self, problem_name):
        with open(self.__FILE, 'r') as file:
            self.__data = json.load(file)
        return self.__data[problem_name]

    def set_seed(self, seed_number):
        with open(self.__seed_file, 'w') as file:
            file.write(str(seed_number))

    def get_seed(self):
        with open(self.__seed_file, 'r') as file:
            seed_number = file.read()
        return int(seed_number)

    def plot_ea(self):
        x = [x['best_fitness'] for x in self.get_data('ea')]
        y = list(range(0, len(x)))
        std = np.std(x)
        mean = np.mean(x)
        print('EVOLUTIONARY ALGORITHM:')
        print(f'\tSTD: {std}')
        print(f'\tMEAN: {mean}')
        plt.scatter(x, y)
        plt.title('EVOLUTIONARY ALGORITHM')
        plt.show()

    def plot_hc(self):
        x = [x['best_fitness'] for x in self.get_data('hc')]
        y = list(range(0, len(x)))
        std = np.std(x)
        mean = np.mean(x)
        print('HILL CLIMBING:')
        print(f'\tSTD: {std}')
        print(f'\tMEAN: {mean}')
        plt.scatter(x, y)
        plt.title('HILL CLIMBING')
        plt.show()
