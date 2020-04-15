from random import randint, seed

from validation.validation import Validation


class Controller:
    def __init__(self, problem):
        self.__problem = problem
        self.__validation = Validation()

    def set_problem_params(self, params):
        self.__problem.set_params(
            swarm_size=params['swarm_size'],
            particle_size=params['particle_size'],
            inertia_coefficient=params['inertia_coefficient'],
            cognitive_learning_coefficient=params['cognitive_learning_coefficient'],
            social_learning_coefficient=params['social_learning_coefficient'],
        )

    def run_pso(self, iterations_number):
        # seed
        RANDOM_SEED = randint(0, 100000)
        seed(RANDOM_SEED)
        output = {}
        iterations = iterations_number
        self.__problem.initialize_population()
        while not self.__problem.is_solution() and iterations_number:
            print('iteration', iterations_number)
            self.__problem.iteration()
            iterations_number -= 1
        output['solution_found'] = self.__problem.is_solution()
        output['solution'] = self.__problem.get_best_global_particle()
        output['no_more_iteration'] = (iterations_number == 0)
        # save iteration
        data = {'SEED': RANDOM_SEED}
        data.update(self.__problem.get_params())
        data['iterations_number'] = iterations
        self.__validation.store_file({
            'problem_name': 'pso',
            'data': data
        })
        return output
