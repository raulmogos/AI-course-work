import numpy as np

from data.data import Data


np.random.seed(1)


def f_linear(x, derivative=False):
    return 1 if derivative else x


def sigmoid(x, derivative=False):
    d_f = x * (1.0 - x)
    f = 1.0 / (np.math.e ** (- x))
    return d_f if derivative else f


class ANN:
    def __init__(self, data=Data(), alpha=.001, activation_function=f_linear, input_columns=[0, 1, 2, 3, 4], output_columns=[5], no_hidden=3):
        self.__alpha = alpha
        # the activation function
        self.__activation_function = activation_function

        # the actual data
        self.__data = np.array(data.data)
        # inputs
        self.__inputs = self.__data[:, input_columns]
        # outputs
        self.__outputs = self.__data[:, output_columns]

        # neurons from input layer
        self.__input_layer = np.array([1] * len(self.__inputs[0]))
        print('input layer', self.__input_layer.shape)

        # neurons from hidden layer
        self.__hidden_layer = np.array([1] * no_hidden)
        print('hidden layer', self.__hidden_layer.shape)

        # neurons from output layer
        self.__output_layer = np.array([1] * len(self.__outputs[0]))
        print('output layer ', self.__output_layer.shape)

        # wights between input layer and hidden layer
        self.__weights_1 = np.array([
            [np.random.rand() for _ in range(len(self.__input_layer))] for _ in range(len(self.__hidden_layer))
        ])
        print(self.__weights_1.shape)

        # wights between hidden layer and output layer
        # number of lines = no of neurons from output layer
        # number of columns = no of neurons from hidden layer
        self.__weights_2 = np.array([
            [np.random.rand() for _ in range(len(self.__hidden_layer))] for _ in range(len(self.__output_layer))
        ])
        print(self.__weights_2.shape)

    def feed_forward(self):
        print('feed forward')
        self.__hidden_layer = np.dot(self.__weights_1, self.__inputs.transpose())
        self.__output_layer = np.dot(self.__weights_2, self.__hidden_layer)
        print(self.__output_layer.shape)

    def back_propagation(self):
        # TODO
        print('back prop')
        # deltas for weights between hidden and output layers
        err = (self.__output_layer.T - self.__outputs) * self.__activation_function(self.__output_layer.T, derivative=True)
        delta_weights_1 = np.dot(self.__hidden_layer, err)

        # deltas for weights between input and hidden layer
        print(self.__inputs.T)
        return
        print(err.shape, self.__weights_2.shape, self.__hidden_layer.shape)
        d = np.dot(err, self.__weights_2) * self.__activation_function(self.__hidden_layer.T)
        delta_weights_2 = np.dot(self.__inputs.T, d)

        self.__weights_1 -= self.__alpha * delta_weights_1
        self.__weights_2 -= self.__alpha * delta_weights_2.T