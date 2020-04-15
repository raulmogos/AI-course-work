

class Controller:
    def __init__(self, decision_tree):
        self.__decision_tree = decision_tree

    def run_train(self):
        print('training...')
        self.__decision_tree.train()

    def get_tree(self):
        return self.__decision_tree.root

    def run_tests(self):
        self.__decision_tree.test()
        print(f'accuracy: {self.__decision_tree.accuracy}')
