from random import seed, randint

from validation.validation import Validation


class Controller:
    def __init__(self, problem_ea, problem_hc):
        self.__problem_ea = problem_ea
        self.__problem_hc = problem_hc
        self.__validation = Validation()

    def set_problem_ea_params(self, problem_ea_params):
        self.__problem_ea.set_params(
            probability_of_mutation=problem_ea_params['probability_of_mutation'],
            probability_of_crossover=problem_ea_params['probability_of_crossover'],
            individual_size=problem_ea_params['individual_size'],
            population_size=problem_ea_params['population_size']
        )

    def set_problem_hc_params(self, problem_hc_params):
        self.__problem_hc.set_params(
            point_size=problem_hc_params['point_size']
        )

    def run_problem_ea(self, no_iterations):
        # seed
        RANDOM_SEED = randint(0, 100000)
        seed(RANDOM_SEED)
        output = {
            'no_population': False,
            'solution_found': False,
            'solution': None,
            'best_individual_so_far': None,
            'no_more_iterations': False
        }
        number_iterations = no_iterations
        self.__problem_ea.initialisation()
        while no_iterations:
            print(f'iteration {no_iterations}')
            self.__problem_ea.iteration()
            if self.__problem_ea.no_population():
                output['no_population'] = True
                break
            if self.__problem_ea.is_solution_found():
                output['solution_found'] = True
                output['solution'] = self.__problem_ea.get_solution()
                break
            no_iterations -= 1
        output['best_individual_so_far'] = self.__problem_ea.get_best_solution_so_far()
        output['no_more_iterations'] = True if not no_iterations else None
        # save iteration
        data = {'SEED': RANDOM_SEED}
        data.update(self.__problem_ea.get_params())
        data['number_iterations'] = number_iterations
        self.__validation.store_file({
            'problem_name': 'ea',
            'data': data
        })
        return output

    def run_problem_hc(self):
        # seed
        RANDOM_SEED = randint(0, 100000)
        seed(RANDOM_SEED)
        output = {}
        self.__problem_hc.initialisation()
        no_iterations = 0
        while not self.__problem_hc.is_solution_found():
            print(f'iteration {no_iterations}')
            self.__problem_hc.iteration()
            no_iterations += 1
        output['solution'] = self.__problem_hc.get_current_point()
        # save iteration
        data = {'SEED': RANDOM_SEED}
        data.update(self.__problem_hc.get_params())
        self.__validation.store_file({
            'problem_name': 'hc',
            'data': data
        })
        return output
