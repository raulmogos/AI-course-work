import json


class UI:
    def __init__(self, controller):
        self.__controller = controller
        self.__file = 'config.json'

    def run_on_file_config(self):
        with open('ui/' + self.__file, 'r') as json_file:
            params = json.load(json_file)
        self.__controller.set_problem_params(params)
        self.__run()

    def run_on_console_params(self):
        params = {
            'solution_size': int(input('solution size: ')),
            'q0': float(input('q0 :')),
            'alpha': float(input('alpha: ')),
            'beta': float(input('beta: ')),
            'rho': float(input('rho: ')),
            'epoch_size': int(input('epoch size: ')),
            'iterations': float(input('iterations: '))
        }
        self.__controller.set_problem_params(params)
        self.__run()

    def __run(self):
        print('It will take some time ... ')
        ret = self.__controller.run()
        print(f'best ant:  {ret}')
