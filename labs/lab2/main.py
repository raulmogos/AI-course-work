from problem import Problem
from controller import Controller
from ui import Console


problem = Problem()
controller = Controller(problem)
console = Console(controller)

console.run()
