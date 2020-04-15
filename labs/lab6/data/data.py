from copy import deepcopy

import numpy as np


class Data:
    def __init__(self, file_path, train__size=0.8):
        """
        :param file_path: the path to the file
        :param train: the proportion of the tran matrix
        """
        self.__train__size = train__size
        self.__file_path = file_path
        # a matrix containing all data
        self.__matrix = None
        self.__test_matrix = None
        # a list with attributes
        self.__map_attributes = None
        self.__load()

    @property
    def attributes_name(self):
        return deepcopy(self.__map_attributes)

    @property
    def matrix(self):
        return deepcopy(self.__matrix)

    @property
    def test_matrix(self):
        return deepcopy(self.__test_matrix)

    def __load(self):
        with open(self.__file_path, 'r') as file:
            lines = file.readlines()
            __matrix = np.array([[int(item) if item.isnumeric() else item for item in line.replace('\n', '').split(',')] for line in lines])
        attributes_file_path = self.__file_path.split('.')
        attributes_file_path[-2] = attributes_file_path[-2] + '-attributes'
        attributes_file_path = '.'.join(attributes_file_path)
        with open(attributes_file_path, 'r') as file:
            self.__map_attributes = file.readline().split(',')
        np.random.shuffle(__matrix)
        line = int(len(__matrix) * self.__train__size)
        self.__matrix = __matrix[:line]
        self.__test_matrix = __matrix[line:]

    def __str__(self):
        return str(self.__matrix)
