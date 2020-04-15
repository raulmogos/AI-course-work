import sys

from PyQt5.QtWidgets import QApplication
 
from problem.problem_ea import ProblemEA
from problem.problem_hc import ProblemHC
from controller.controller import Controller
from ui.ui import UI


app = QApplication(sys.argv)

problem_ea = ProblemEA()
problem_hc = ProblemHC()
controller = Controller(problem_ea, problem_hc)
ui = UI(controller)

ui.show()

sys.exit(app.exec_())

