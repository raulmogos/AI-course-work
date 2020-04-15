import math
from copy import deepcopy
from random import random

import pygame

from model.permutation import Permutation


class Particle:
    def __init__(self, size, fitness_function=None):
        self.__particle_size = size
        self.__fitness_function = fitness_function
        self.__fitness = math.inf
        # the matrix aka POSITION at which currently is
        self.__matrix = self.__generate_random_particle()
        # current direction: the vector of probabilities
        self.__velocity = [random() for _ in range(self.__particle_size * 2)]
        # the best matrix aka POSITION until now
        self.__best_matrix = self.__matrix

    def __generate_random_particle(self):
        return [Permutation(self.__particle_size) for _ in range(self.__particle_size * 2)]

    @property
    def best_matrix(self):
        return self.__best_matrix

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = velocity

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness):
        self.__fitness = fitness

    @property
    def matrix(self):
        return deepcopy(self.__matrix)

    @matrix.setter
    def matrix(self, matrix):
        self.__matrix = deepcopy(matrix)
        self.__update_best_position()

    def get_matrix_list(self):
        return deepcopy(perm.permutation for perm in self.matrix)

    def __update_best_position(self):
        self.__best_matrix = min(self.__best_matrix, self.__matrix, key=self.__fitness_function)

    def show(self):
        pygame.init()
        pygame.display.set_caption(f'fitness: {self.__fitness}')
        matrix = []
        length = 100
        margin = 2
        half = self.__particle_size
        width_height = (half * length) + (margin * half - margin)
        screen = pygame.display.set_mode((width_height, width_height))
        screen.fill((255, 255, 255))
        font_obj = pygame.font.Font('freesansbold.ttf', 40)
        pygame.display.update()
        for i in range(half):
            _top = i * length + i * margin
            row = []
            for j in range(half):
                _left = j * length + j * margin
                rect = pygame.Rect(_left, _top, length, length)
                pygame.draw.rect(screen, (22, 111, 77), rect)
                screen.blit(font_obj.render(
                    f'{self.__matrix[i].permutation[j]},{self.__matrix[half + j].permutation[i]}',
                    True, (255, 255, 255), (22, 111, 77)),
                    (_left + length / 5 + 4, _top + length / 5 + 6))
                row.append(rect)
            matrix.append(row)
        pygame.display.update()
        run = True
        while run:
            pygame.time.delay(100)
            for ev in pygame.event.get():
                if ev.type is pygame.QUIT:
                    run = False
                    break
        pygame.quit()

    def __str__(self):
        return str([str(perm) for perm in self.__matrix]) + ' ' + str(self.__fitness)
