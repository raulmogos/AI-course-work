from validation.validation import Validation


class Controller:
    def __init__(self, problem):
        self.__validation = Validation()
        self.__problem = problem
        self.__problem_params = None

    def set_problem_params(self, params):
        self.__problem_params = params
        self.__problem.set_params(
            solution_size=params['solution_size'],
            q0=params['q0'],
            alpha=params['alpha'],
            beta=params['beta'],
            rho=params['rho']
        )

    def run(self):
        iterations = self.__problem_params['iterations']
        while iterations:
            self.__problem.epoch(self.__problem_params['epoch_size'])
            print(f'iteration {iterations}')
            iterations -= 1
        solution = self.__problem.get_best_ant()
        # save data
        data = {}
        data.update(self.__problem.get_params())
        data['iterations'] = self.__problem_params['iterations']
        data['epoch_size'] = self.__problem_params['epoch_size']
        data['best_fitness'] = solution.fitness
        self.__validation.store_file({
            'problem_name': 'aco',
            'data': data
        })
        return solution
