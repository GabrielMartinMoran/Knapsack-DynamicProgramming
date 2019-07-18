from KnapsackSolver import *
from Item import *
from ItemGenerator import *
from VisualKnapsack import *
from TablePlotter import *
import time
from threading import Thread

RUN_VISUAL = False

WAIT_UNTIL_SOLVE = 5 #Segundos
KNAPSACK_CAPACITY = 20
ITEMS_TO_GENERATE = 16 # Max visible 117


def main():
    solver = KnapsackSolver()
    items = [
        Item("Item 1",  8, 4),
        Item("Item 2",  5, 6),
        Item("Item 3",  2, 5),
        Item("Item 4",  7, 8),
        Item("Item 5",  2, 1),
        Item("Item 6",  8, 2),
        Item("Item 7",  4, 6),
        Item("Item 8",  3, 4),
        Item("Item 9",  2, 5),
        Item("Item 10", 9, 7),
    ]
    solution, table = solver.solve(items, KNAPSACK_CAPACITY)
    solver.print_table()
    #TablePlotter.plot_table(table)
    print("\nSolution:", [x.id for x in solution.items])
    print("Total value:", solution.total_value)
    print("Total weight:", solution.total_weight)


def delayed_solve(visual_knspsack):
    time.sleep(WAIT_UNTIL_SOLVE)
    visual_knspsack.begin_solver(KNAPSACK_CAPACITY)


def visual_main():
    item_generator = ItemGenerator()
    items = item_generator.generate(ITEMS_TO_GENERATE)
    knapsack = VisualKnapsack(items)
    thread = Thread(target=delayed_solve, args=(knapsack,))
    thread.start()
    knapsack.main_loop()


if __name__ == "__main__":
    if(RUN_VISUAL):
        visual_main()
    else:
        main()
