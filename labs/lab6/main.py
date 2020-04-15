from controller import Controller
from ui import UI
from data.data import Data
from decision_tree import DecisionTree

import numpy as np


# np.random.seed(2)

data = Data('data/files/balance-scale.csv', train__size=0.9)
dt = DecisionTree(data, class_row_number=0)

# data = Data('data/files/test.csv', train__size=0.85)
# dt = DecisionTree(data, class_row_number=4)

controller = Controller(dt)
ui = UI(controller)

ui.run()