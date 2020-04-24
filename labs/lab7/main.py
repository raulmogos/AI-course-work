from controller import Controller
from data.data import Data


c = Controller(Data(filename='data\data.csv'), learning_rate=0.0001)
c.gradient_descent(iterations=500)
c.plot()
