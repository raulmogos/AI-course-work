import sys

from PyQt5.QtWidgets import QApplication

from controller.controller import Controller
from problem.problem import Problem
from ui.ui import UI

app = QApplication(sys.argv)

problem = Problem()
controller = Controller(problem)
ui = UI(controller)

ui.show()

sys.exit(app.exec_())

