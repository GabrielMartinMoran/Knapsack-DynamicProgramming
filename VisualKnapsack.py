import pygame
from threading import Thread
from KnapsackSolver import *
import time
from TablePlotter import *

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
(WIDTH, HEIGHT) = (1000, 600)
WINDOW_NAME = "Knapsack Solver"
ITEMS_IMAGE_SIZE = 100
ITEMS_IMAGE_H_SEPARATOR = 20
ITEMS_IMAGE_V_SEPARATOR = 12
IMAGES_PER_LINE = 4
TEXT_SIZE = 15  # PROBAR
RESOURCES = {
    "knapsack": pygame.image.load('resources/Knapsack.png')
}


class VisualKnapsack:

    def __init__(self, items):
        self.__have_to_solve = False
        self.__have_to_display_table = False
        self.__result_table = None
        self.__knapsack_capacity = 0
        self.__items_inside = []
        self.__items_outside = []
        self.__items_to_solve = []
        self.__running = True
        self.__solver = KnapsackSolver()
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.font.init()
        self.__text_renderer = pygame.font.SysFont('Comic Sans MS', TEXT_SIZE)
        pygame.display.set_caption(WINDOW_NAME)
        self.__screen.fill(BLACK_COLOR)
        pygame.display.flip()
        self.__clock = pygame.time.Clock()
        self.set_items_to_solve(items)

    def main_loop(self):
        while(self.__running):
            self.__detect_exit()
            self.__check_if_have_to_solve()
            self.__screen.fill(BLACK_COLOR)
            self.__draw_screen()
            pygame.display.flip()
            self.__clock.tick(5)
            self.__check_if_have_to_display_table()

    def __detect_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    def __check_if_have_to_solve(self):
        if(not self.__have_to_solve):
            return
        print("Solver started!")
        solution, self.__result_table = self.__solver.solve(
            self.__items_to_solve, self.__knapsack_capacity)
        #self.__solver.print_table()
        print("\nSolution:", [x.id for x in solution.items])
        print("Total value:", solution.total_value)
        print("Total weight:", solution.total_weight)
        self.__items_outside = []
        self.__items_inside = []
        items_ids = [x.id for x in solution.items]
        for item in self.__items_to_solve:
            if(item.id in items_ids):
                self.__items_inside.append(item)
            else:
                self.__items_outside.append(item)
        self.__have_to_display_table = True
        self.__have_to_solve = False

    def __check_if_have_to_display_table(self):
        if(not self.__have_to_display_table):
            return
        TablePlotter.plot_table(self.__result_table)
        self.__have_to_display_table = False

    def __draw_screen(self):
        self.__screen.blit(RESOURCES["knapsack"], (int(WIDTH / 2), 0))
        self.__draw_items_inside_knapsack()
        self.__draw_items_outside_knapsack()

    def __draw_items_inside_knapsack(self):
        self.__draw_items(self.__items_inside, int(
            WIDTH / 2) + ITEMS_IMAGE_H_SEPARATOR)

    def __draw_items_outside_knapsack(self):
        self.__draw_items(self.__items_outside, ITEMS_IMAGE_H_SEPARATOR)

    def __draw_items(self, items, initial_x):
        y = HEIGHT - ITEMS_IMAGE_SIZE - (ITEMS_IMAGE_V_SEPARATOR * 4)
        x = initial_x
        images_in_line = 0
        for item in items:
            self.__screen.blit(RESOURCES[item.image_path], (x, y))
            value_text = self.__text_renderer.render(
                "Value: " + str(item.value), False, WHITE_COLOR)
            self.__screen.blit(
                value_text, (x + int(ITEMS_IMAGE_SIZE / 5), y + ITEMS_IMAGE_SIZE))
            weight_text = self.__text_renderer.render(
                "Weight: " + str(item.weight), False, WHITE_COLOR)
            self.__screen.blit(
                weight_text, (x + int(ITEMS_IMAGE_SIZE / 5), y + ITEMS_IMAGE_SIZE + 15))
            images_in_line += 1
            if(images_in_line % IMAGES_PER_LINE == 0):
                y -= ITEMS_IMAGE_SIZE + (4 * ITEMS_IMAGE_V_SEPARATOR)
                x = initial_x
                images_in_line = 0
            else:
                x += ITEMS_IMAGE_SIZE + ITEMS_IMAGE_H_SEPARATOR

    def set_items_to_solve(self, items):
        self.__items_to_solve = items
        for x in items:
            if(x.image_path not in RESOURCES):
                RESOURCES[x.image_path] = pygame.image.load(x.image_path)
        self.__items_outside = items

    def begin_solver(self, knapsack_capacity):
        self.__have_to_solve = True
        self.__knapsack_capacity = knapsack_capacity
