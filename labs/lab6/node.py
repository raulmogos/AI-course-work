

class Node:
    def __init__(self, attribute='root', value=''):
        self.__children = []
        self.__attribute = attribute
        self.__value = value
        self.__meta = {}

    @property
    def children(self):
        return self.__children

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def attribute(self):
        return self.__attribute

    @attribute.setter
    def attribute(self, attribute):
        self.__attribute = attribute

    def is_leaf(self):
        return len(self.__children) == 0

    def add_child(self, child):
        self.__children.append(child)

    def to_string(self, d=0):
        print('\t' * d + f'|-> {self.__attribute}: {self.__value}')
        for c in self.__children:
            c.to_string(d + 1)

    def __str__(self):
        return f'attribute {self.__attribute} -> value: {self.__value}'

# n = Node('atr1sss', 'val1')
# n2 = Node('atr2', 'val2')
# n2.add_child(Node('atr9', 'val9'))
# n.add_child(n2)
# n.add_child(Node('atr3', 'val3'))
#
# n3 = Node('atr00', 'val00')
# n4 = Node('asdas', 'val')
# n4.add_child(Node('aa', 'valaa'))
# n3.add_child(n4)
# n.add_child(n3)
#
# n.add_child(Node('atr4', 'val4'))
# n.to_string()
