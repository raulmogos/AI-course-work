"""
    An Individual(Member) contains multiple chromosomes
    A Chromosome contains multiple genes
    A Gene is apiece of information

    In our case:
        gene        -> integer
        chromosome  -> list of integer
        individual  -> list of lists of integers (a matrix)

ps:
    It was nice to have a class for each of them (gene, chromosome),
    but it would have been an overkill since are just lists and numbers.
"""
import pygame

from copy import deepcopy


class Individual:
    def __init__(self, lst):
        # lst - a matrix of information
        self.__fitness = -1
        self.__size = len(lst)
        self.__chromosome_list = deepcopy(lst)

    def set_chromosome(self, index, chromosome):
        self.__chromosome_list[index] = chromosome

    def get_chromosome(self, index):
        return deepcopy(self.__chromosome_list[index])

    def length_chromosome(self):
        return len(self.__chromosome_list[0])

    def get_chromosome_list(self):
        return deepcopy(self.__chromosome_list)

    def set_chromosome_list(self, chromosome_list):
        self.__chromosome_list = chromosome_list

    def length(self):
        return self.__size

    def get_fitness(self):
        return self.__fitness

    def set_fitness(self, value):
        self.__fitness = value

    def show(self, message):
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
                    f'{self.__chromosome_list[i][j]},{self.__chromosome_list[half + j][i]}',
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
        return str(self.__chromosome_list) + ' fitness: ' + str(self.__fitness)

    def __eq__(self, other):
        return self.__chromosome_list == other.__chromosome_list
