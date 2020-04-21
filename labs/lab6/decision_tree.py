import math
import numpy as np

from copy import deepcopy

from data.data import Data
from node import Node


class DecisionTree:
    def __init__(self, data=None, class_row_number=0):
        self.__data = data or Data('data/files/balance-scale.csv', train__size=0.8)
        self.__matrix = self.__data.matrix
        self.__class_row_number = class_row_number
        self.__entropy = self.__entropy__()
        self.__root = Node()
        self.__accuracy = 0

    def __entropy__(self):
        # get the classes column
        classes = self.__matrix[:, self.__class_row_number]
        unique_values, count = np.unique(classes, return_counts=True)
        probability = {cls: c / len(classes) for cls, c in zip(unique_values, count)}
        return sum((- p) * math.log2(p) for p in probability.values())

    def entropy_help(self, value, column_number, data):
        # filter rows by value on column: column_number
        filtered_data = np.array(list(filter(lambda row: row[column_number] == value, data)))
        if filtered_data.size == 0: return 0
        # get that classes for that filtered data
        classes = filtered_data[:, self.__class_row_number]
        # get the unique elements and their frequency
        unique_values, count = np.unique(classes, return_counts=True)
        # compute their probability
        probability = {value: c / len(classes) for value, c in zip(unique_values, count)}
        # calculate the entropy
        return sum((- p) * math.log2(p) for p in probability.values())

    def __info_gain(self, column, data):
        # get the values from the desired column
        column_info = self.__matrix[:, column]
        # get the unique element    s and their frequency
        unique_values, count = np.unique(column_info, return_counts=True)
        # compute their probability
        probability = {value: c / len(column_info) for value, c in zip(unique_values, count)}
        # compute the sum: p(v)*en(rows_v) for each value as v
        s = sum([probability[value] * self.entropy_help(value, column, data) for value in unique_values])
        # compute the information gain
        return self.__entropy - s

    def id3(self, data, attributes):
        """
        Constructs the Decision Tree according to the ID3 algorithm
        :param data: a matrix containing the entities
        :param attributes: a list of column numbers
        :return: Node
        """
        # create node N
        node = Node()
        unique_classes, count = np.unique(data[:, self.__class_row_number], return_counts=True)
        # if examples from data belong to a single class C then
        # node N becomes a leaf and is labeled by C
        if len(unique_classes) == 1:
            attr_name_string = self.to_attr_name(self.__class_row_number)
            leaf_node = Node()
            leaf_node.attribute = attr_name_string
            leaf_node.value = unique_classes[0]
            node.add_child(leaf_node)
            return node
        # if there are no attributes then
        # node N becomes a leaf and is labeled by majority class of D
        if not attributes:
            # compute the predominant label
            predominant_value = max([(cls, c) for cls, c in zip(unique_classes, count)], key=lambda item: item[1])[0]
            leaf_node = Node()
            leaf_node.attribute = self.to_attr_name(self.__class_row_number)
            leaf_node.value = predominant_value
            node.add_child(leaf_node)
            return node
        # get the best attribute to select by
        attr = max(attributes, key=lambda attr: self.__info_gain(attr, data))
        # get all values of that attribute
        attribute_values = set(data[:, attr])
        for val in attribute_values:
            # get all data with value val on column attribute
            new_data = data[[row[attr] == val for row in data]]
            if new_data.size == 0:
                node.add_child(Node(self.to_attr_name(attr), val))
            else:
                new_attributes = attributes.copy()
                new_attributes.remove(attr)
                new_node = self.id3(new_data, new_attributes)
                new_node.attribute = self.to_attr_name(attr)
                new_node.value = val
                node.add_child(new_node)
        return node

    def train(self):
        all_attributes = list(range(0, len(self.__matrix[0])))
        all_attributes.remove(self.__class_row_number)
        self.__root = self.id3(deepcopy(self.__matrix),  all_attributes)

    def test(self):
        good = 0
        for row in self.__data.test_matrix:
            predict = self.__predict(row, self.__root)
            print(f'{row} -> prediction: {self.to_attr_name(self.__class_row_number)} -> {predict}')
            good += (predict == row[self.__class_row_number])
        self.__accuracy = (good / len(self.__data.test_matrix)) * 100
#         compute other metrics (Confusion matrix, Precision, recall, F-measure - very important if you deal by an unbalanced dataset)

    def __predict(self, new_row, node):
        """
        :param new_row: a list of attributes
        :param node: Node object
        :return: the class that it is predicted
        """
        index = self.__data.attributes_name.index(node.children[0].attribute)
        if index == self.__class_row_number:
            return node.children[0].value
        val = new_row[index]
        if val not in [c.value for c in node.children]:
            return self.__predict(new_row, node.children[0])
        else:
            c = list(filter(lambda c: c.value == val, node.children))[0]
            return self.__predict(new_row, c)

    def predict(self, new_row):
        return self.__predict(new_row, self.__root)

    @property
    def root(self):
        return self.__root

    @property
    def accuracy(self):
        return self.__accuracy

    def to_attr_name(self, col_number):
        return self.__data.attributes_name[col_number]

    def print_tree(self):
        self.__root.to_string()


# # np.random.seed(1)
# # d = Data('data/files/balance-scale.csv', train__size=0.9)
# # dt = DecisionTree(d, 0)
# d = Data('data/files/test.csv', train__size=0.90)
# dt = DecisionTree(d, 4)
#
# dt.test()
