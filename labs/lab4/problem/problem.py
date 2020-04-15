import math
from random import random

from model.particle import Particle
from model.permutation import Permutation


class Problem:
    def __init__(self, swarm_size=100, particle_size=3, inertia_coefficient=1, cognitive_learning_coefficient=1, social_learning_coefficient=1, step_1=0.6, step_2=0.9):
        self.__step_1 = step_1
        self.__step_2 = step_2
        # inertia coefficient
        self.__inertia_coefficient = inertia_coefficient
        # cognitive learning coefficient
        self.__cognitive_learning_coefficient = cognitive_learning_coefficient
        # social learning coefficient
        self.__social_learning_coefficient = social_learning_coefficient
        self.__swarm_size = swarm_size
        self.__particle_size = particle_size
        self.__best_global_particle = None
        self.__swarm = None
        self.__target_fitness = 0

    def set_params(self, swarm_size=100, particle_size=3, inertia_coefficient=1, cognitive_learning_coefficient=1, social_learning_coefficient=1, step_1=0.6, step_2=0.9):
        self.__step_1 = step_1
        self.__step_2 = step_2
        # inertia coefficient
        self.__inertia_coefficient = inertia_coefficient
        # cognitive learning coefficient
        self.__cognitive_learning_coefficient = cognitive_learning_coefficient
        # social learning coefficient
        self.__social_learning_coefficient = social_learning_coefficient
        self.__swarm_size = swarm_size
        self.__particle_size = particle_size
        self.__best_global_particle = None
        self.__swarm = None
        self.__target_fitness = 0

    def get_params(self):
        return {
            'best_fitness': self.__best_global_particle.fitness,
            'swarm_size': self.__swarm_size,
            'particle_size': self.__particle_size,
            'inertia_coefficient': self.__inertia_coefficient,
            'cognitive_learning_coefficient': self.__cognitive_learning_coefficient,
            'social_learning_coefficient': self.__social_learning_coefficient,
            'step_1': self.__step_1,
            'step_2': self.__step_2,
        }

    def initialize_population(self):
        self.__swarm = [Particle(self.__particle_size, self.fitness_function) for _ in range(self.__swarm_size)]
        self.__best_global_particle = min(self.__swarm, key=self.fitness_function)

    def is_solution(self):
        return self.__best_global_particle.fitness == 0

    def get_best_global_particle(self):
        return self.__best_global_particle

    @property
    def swarm(self):
        return self.__swarm

    def iteration(self):
        self.__best_global_particle = min(self.__swarm, key=self.fitness_function)
        for par in self.__swarm:
            par.fitness = self.fitness_function(par)
            self.update_particle_position(par)

    def fitness_function(self, particle):
        output = 0
        try:
            matrix = [perm.permutation for perm in particle.matrix]
        except:
            matrix = [perm.permutation for perm in particle]
        length = len(matrix)
        half = length // 2
        pairs_dict = {}
        # check for pairs
        for i in range(half):
            for j in range(half):
                pair = (matrix[i][j], matrix[half + j][i])
                if pair in pairs_dict:
                    output += 1
                    pairs_dict[pair] += 1
                else:
                    pairs_dict[pair] = 1
        # check for permutation
        for i in range(half):
            perm_1, perm_2 = [], []
            for j in range(half):
                perm_1.append(matrix[j][i])
                perm_2.append(matrix[half + j][i])
            if not Permutation.is_permutation(perm_1):
                output += 1
            if not Permutation.is_permutation(perm_2):
                output += 1
        return output

    @staticmethod
    def subtract_matrices(one, two):
        return [one[i] - two[i] for i in range(len(one))]

    def update_particle_position(self, particle):
        new_velocity = []
        particle_matrix = particle.matrix
        particle_best_matrix = particle.best_matrix
        for vel, i in zip(particle.velocity, range(0, len(particle.velocity))):
            new_vel = self.__inertia_coefficient * vel
            new_vel += self.__cognitive_learning_coefficient * random() * Permutation.manhattan_distance(
                particle_best_matrix[i], particle_matrix[i]
            )
            new_vel += self.__social_learning_coefficient * random() * Permutation.manhattan_distance(
                self.__best_global_particle.matrix[i], particle_matrix[i]
            )
            new_velocity.append(new_vel)
        particle.velocity = new_velocity
        new_matrix = []
        for vel, i in zip(new_velocity, range(0, len(new_velocity))):
            f = 1 / (1 + math.e ** (- vel))
            # print(vel, f)
            # adapted to have all chances: g_best, l_best, inertia
            if f > self.__step_2:
                new_matrix.append(particle_best_matrix[i])
            elif f > self.__step_1:
                new_matrix.append(self.__best_global_particle.matrix[i])
            else:
                new_matrix.append(particle_matrix[i])
        particle.matrix = new_matrix

