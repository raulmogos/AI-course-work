import time
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


def clean_data(data):
    """
        we make the data a little bit smaller
    """
    new_data = deepcopy(data)
    for i in range(len(data)):
        for j in range(len(data[i])):
            new_data[i][j] = 0.001 * data[i][j]
    return new_data


class Controller:
    def __init__(self, data, learning_rate=0.0001, result_column=-1):
        # how much is the step that is taken every iteration
        self.__learning_rate = learning_rate
        print(f'learning rate: {learning_rate}')
        # the actual data
        data = np.array(data.data)
        # get only the attributes: the first 5 columns
        self.__data = data[:, :result_column]
        # insert a column with ones at position 0
        self.__data = np.insert(self.__data, 0, 1, axis=1)
        # get the output column
        self.__output = data[:, result_column]
        # set a random hypothesis
        self.__hypothesis = self.__init_hypothesis()
        # size of the train data
        self.__size = len(self.__data)
        # print(self.__data)
        # print(self.__output)
        self.__errors = []

    def __init_hypothesis(self):
        return np.array([[np.random.rand()] for _ in range(len(self.__data[0]))])

    def add_to_plot(self, error):
        self.__errors.append(error)

    def guess(self, row):
        """
            return f(x) - the guess made by our function
        :param row: list of numbers
        :return: number
        """
        return sum(row[i] * self.__hypothesis[i][0] for i in range(len(row)))

    def d_cost_function(self, prediction_array, index_param):
        """
            computes the derivative of J with respect to param<index_param>
        :param prediction_array: data * hypothesis, where data - matrix and hypothesis - vector
        :param index_param: int
        :return: double
        """
        sm = 0
        for i in range(self.__size):
            sm += (prediction_array[i] - self.__output[i]) * self.__data[i][index_param]
        return (1 / self.__size) * sm

    def J(self, prediction_array):
        """
            J - cost function
        :return: double
        """
        sm = sum((prediction - output) ** 2 for prediction, output in zip(prediction_array, self.__output))
        return (1 / self.__size) * sm

    def make_prediction_array(self):
        """
            matrix_data * predictive_function_vector = prediction_vector
        """
        return np.matmul(self.__data, self.__hypothesis).flatten()

    def gradient_descent(self, iterations=1000):

        derivative = [0] * len(self.__hypothesis)

        for _ in range(iterations):

            # make predictions
            prediction_array = self.make_prediction_array()

            # calculate the total error
            error = self.J(prediction_array)

            # add error to plot
            self.add_to_plot(error)

            # compute the derivatives
            for i in range(len(self.__hypothesis)):
                derivative[i] = self.d_cost_function(prediction_array, i)

            # update the hypothesis accordingly
            for i in range(len(self.__hypothesis)):
                self.__hypothesis[i][0] -= self.__learning_rate * derivative[i]

    def plot(self):
        print('errors', self.__errors)
        print('best: ', self.__errors[-1])
        plt.plot(self.__errors)
        plt.ylabel('error')
        plt.xlabel('iteration')
        plt.show()

