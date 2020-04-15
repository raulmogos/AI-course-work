import json
import matplotlib.pyplot as plt
import numpy as np


FILE = 'results.json'


class Validation:
    def __init__(self):
        self.__FILE = FILE
        self.__data = {
            'pso': [],
        }

    def store_file(self, data):
        with open('validation/' + self.__FILE, 'r') as file:
            self.__data = json.loads(file.read())
        self.__data[data['problem_name']].append(data['data'])
        with open('validation/' + self.__FILE, 'w') as file:
            json.dump(self.__data, file, indent=4)

    def get_data(self, problem_name):
        with open(self.__FILE, 'r') as file:
            self.__data = json.load(file)
        return self.__data[problem_name]

    def plot_pso(self):
        x = [x['best_fitness'] for x in self.get_data('pso')]
        y = list(range(0, len(x)))
        std = np.std(x)
        mean = np.mean(x)
        print('PARTICLE SWARM OPTIMISATION:')
        print(f'\tSTD: {std}')
        print(f'\tMEAN: {mean}')
        plt.scatter(x, y)
        plt.title('PARTICLE SWARM OPTIMISATION')
        plt.show()

