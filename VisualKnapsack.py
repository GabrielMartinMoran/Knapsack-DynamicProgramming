import pygame
from threading import Thread
from KnapsackSolver import *
import time
from TablePlotter import *

WHITE_COLOR = (255, 255, 255)
GREEN_COLOR = (124,252,0)
BLACK_COLOR = (0, 0, 0)
(WIDTH, HEIGHT) = (1000, 600)
WINDOW_NAME = "Knapsack Solver"
FIRST_IMAGE_SIZE_REECALATE = 16
SECOND_IMAGE_SIZE_REECALATE = 49
RESOURCES = {
    "background": pygame.image.load('resources/bg.png'),
    "knapsack": pygame.image.load('resources/Knapsack.png')
}


class VisualKnapsack:

    def __init__(self, items, max_capacity):
        self.__have_to_solve = False
        self.__have_to_display_table = False
        self.__result_table = None
        self.__knapsack_capacity = max_capacity
        self.__items_inside = []
        self.__items_outside = []
        self.__items_to_solve = []
        self.__running = True
        self.__solver = KnapsackSolver()
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.font.init()
        self.__text_renderer = pygame.font.SysFont(
            'Comic Sans MS', self.__get_text_size())
        pygame.display.set_caption(WINDOW_NAME)
        self.__screen.fill(BLACK_COLOR)
        pygame.display.flip()
        self.set_items_to_solve(items)

    def main_loop(self):
        while(self.__running):
            self.__detect_exit()
            self.__check_if_have_to_solve()
            self.__screen.fill(BLACK_COLOR)
            self.__draw_screen()
            pygame.display.flip()            
            self.__check_if_have_to_display_table()
            time.sleep(0.5)

    def __detect_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    def __check_if_have_to_solve(self):
        if(not self.__have_to_solve):
            return
        # Agregamos el texto de resolviendo
        self.__draw_screen()
        self.__draw_solving_message()
        pygame.display.flip()
        print("Solver started!")
        solution, self.__result_table = self.__solver.solve(
            self.__items_to_solve, self.__knapsack_capacity)
        # self.__solver.print_table()
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
        self.__screen.blit(RESOURCES["background"], (0, 0))
        self.__screen.blit(RESOURCES["knapsack"], (int(WIDTH / 2), 0))
        self.__draw_items_inside_knapsack()
        self.__draw_items_outside_knapsack()
        self.__draw_knapsack_capacity()

    def __draw_items_inside_knapsack(self):
        self.__draw_items(self.__items_inside, int(
            WIDTH / 2) + self.__get_images_h_separator())

    def __draw_items_outside_knapsack(self):
        self.__draw_items(self.__items_outside,
                          self.__get_images_h_separator())

    def __draw_items(self, items, initial_x):
        y = HEIGHT - self.__get_images_size() - (self.__get_images_v_separator() * 4)
        x = initial_x
        images_in_line = 0
        for item in items:
            self.__screen.blit(RESOURCES[item.image_path], (x, y))
            value_text = self.__text_renderer.render(
                "Value: " + str(item.value), False, WHITE_COLOR)
            self.__screen.blit(
                value_text, (x + self.__get_text_h_separator(), y + self.__get_images_size()))
            weight_text = self.__text_renderer.render(
                "Weight: " + str(item.weight), False, WHITE_COLOR)
            self.__screen.blit(
                weight_text, (x + self.__get_text_h_separator(), y + self.__get_images_size() + self.__get_text_v_separator()))
            images_in_line += 1
            if(images_in_line % self.__get_max_images_per_line() == 0):
                y -= self.__get_images_size() + (4 * self.__get_images_v_separator())
                x = initial_x
                images_in_line = 0
            else:
                x += self.__get_images_size() + self.__get_images_h_separator()

    def __draw_solving_message(self):
        renderer = pygame.font.SysFont('Comic Sans MS', 60)
        value_text = renderer.render("Resolviendo...", False, GREEN_COLOR)
        self.__screen.blit(value_text, (int(WIDTH / 2) - int(WIDTH / 6), int(HEIGHT / 2) - int(HEIGHT / 8)))


    def __draw_knapsack_capacity(self):
        renderer = pygame.font.SysFont('Comic Sans MS', 20)
        value_text = renderer.render("Capacidad: " + str(self.__knapsack_capacity), False, WHITE_COLOR)
        self.__screen.blit(value_text, (int(WIDTH / 2) + int(WIDTH / 6) + 20, 2))


    def set_items_to_solve(self, items):
        self.__items_to_solve=items
        for x in items:
            if(x.image_path not in RESOURCES):
                RESOURCES[x.image_path]=pygame.image.load(x.image_path)
                RESOURCES[x.image_path]=pygame.transform.scale(
                    RESOURCES[x.image_path], (self.__get_images_size(), self.__get_images_size()))
        self.__items_outside=items
        self.__text_renderer=pygame.font.SysFont(
            'Comic Sans MS', self.__get_text_size())

    def begin_solver(self):
        self.__have_to_solve=True

    def __get_images_size(self):
        if(len(self.__items_to_solve) > SECOND_IMAGE_SIZE_REECALATE):
            return 20
        if(len(self.__items_to_solve) > FIRST_IMAGE_SIZE_REECALATE):
            return 50
        return 100

    def __get_images_h_separator(self):
        if(len(self.__items_to_solve) > SECOND_IMAGE_SIZE_REECALATE):
            return 33
        if(len(self.__items_to_solve) > FIRST_IMAGE_SIZE_REECALATE):
            return 19
        return 20

    def __get_images_v_separator(self):
        if(len(self.__items_to_solve) > SECOND_IMAGE_SIZE_REECALATE):
            return 6
        if(len(self.__items_to_solve) > FIRST_IMAGE_SIZE_REECALATE):
            return 10
        return 12

    def __get_max_images_per_line(self):
        if(len(self.__items_to_solve) > SECOND_IMAGE_SIZE_REECALATE):
            return 9
        if(len(self.__items_to_solve) > FIRST_IMAGE_SIZE_REECALATE):
            return 7
        return 4

    def __get_text_h_separator(self):
        if(len(self.__items_to_solve) > SECOND_IMAGE_SIZE_REECALATE):
            return -10
        if(len(self.__items_to_solve) > FIRST_IMAGE_SIZE_REECALATE):
            return 0
        return 20

    def __get_text_v_separator(self):
        if(len(self.__items_to_solve) > SECOND_IMAGE_SIZE_REECALATE):
            return 9
        if(len(self.__items_to_solve) > FIRST_IMAGE_SIZE_REECALATE):
            return 13
        return 15

    def __get_text_size(self):
        if(len(self.__items_to_solve) > SECOND_IMAGE_SIZE_REECALATE):
            return 9
        if(len(self.__items_to_solve) > FIRST_IMAGE_SIZE_REECALATE):
            return 13
        return 15
