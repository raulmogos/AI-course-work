class Data:
    def __init__(self, filename='data\data.csv'):
        self.__filename = filename
        self.__data = []
        self.__load()

    def __load(self):
        with open(self.__filename, 'r') as f:
            lines = f.readlines()
        self.__data = [[float(nr) for nr in line.split(',')] for line in lines]

    @property
    def data(self):
        return self.__data
