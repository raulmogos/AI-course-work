
from controller.controller import Controller
from problem.problem import Problem
from ui.ui import UI

problem = Problem()
controller = Controller(problem)
ui = UI(controller)

ui.run_on_file_config()
# ui.run_on_console_params()
