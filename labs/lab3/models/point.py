import itertools

from copy import deepcopy

import pygame


class Point:
    def __init__(self, point):
        # point a matrix
        self.__matrix = deepcopy(point)
        self.__fitness = 0
        self.__size = len(point)

    def set_fitness(self, fitness):
        self.__fitness = fitness

    def get_fitness(self):
        return self.__fitness

    def clone(self):
        return deepcopy(self)

    def get_inside_list(self):
        return deepcopy(self.__matrix)

    def generate_neighbours(self):
        neighbours = []
        # neighbours of level two (that are two steps away)
        for i in range(self.__size - 1):
            for j in range(i + 1, self.__size):
                perm_1 = self.__matrix[i]
                perm_2 = self.__matrix[j]
                # print(i, perm_1, j, perm_2)
                permutations_1_rank_1 = self.__generate_permutations_rank_1(perm_1)
                permutations_2_rank_1 = self.__generate_permutations_rank_1(perm_2)
                for item_1 in permutations_1_rank_1:
                    for item_2 in permutations_2_rank_1:
                        neighbour = deepcopy(self.__matrix)
                        neighbour[i] = item_1
                        neighbour[j] = item_2
                        neighbours.append(Point(neighbour))
        # neighbours of level one (that are one step away)
        for i in range(self.__size):
            perm = self.__matrix[i]
            # print(i, perm_1, j, perm_2)
            permutations_rank_1 = self.__generate_permutations_rank_1(perm)
            for item in permutations_rank_1:
                neighbour = deepcopy(self.__matrix)
                neighbour[i] = item
                neighbours.append(Point(neighbour))
        return neighbours

    def __generate_permutations_rank_1(self, perm):
        output = []
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                new_perm = deepcopy(perm)
                new_perm[i], new_perm[j] = new_perm[j], new_perm[i]
                output.append(new_perm)
        return output

    def show(self, message=''):
        pygame.init()
        pygame.display.set_caption(f'fitness: {self.__fitness}')
        matrix = []
        length = 100
        margin = 2
        half = self.__size // 2
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
                    f'{self.__matrix[i][j]},{self.__matrix[half + j][i]}',
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

    def __eq__(self, other):
        return self.__matrix == other.__matrix

    def __str__(self):
        return str([str(item) for item in self.__matrix]) + ' fitness: ' + str(self.__fitness)
