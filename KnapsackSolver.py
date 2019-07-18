from TableCell import *
from copy import deepcopy


class KnapsackSolver:

    def __init__(self):
        self.__table = None
        self.__table_index = 0

    def solve(self, items, capacity):
        sorted_items = self.__sort_items(items)
        self.__generate_table(sorted_items, capacity)
        for i_index, item in enumerate(sorted_items):
            self.__add_item_to_table(item)
        return self.__table[len(self.__table) - 1][capacity], self.__table

    def __sort_items(self, items):
        return sorted(items, key=lambda item: item.value / item.weight, reverse=True)

    def __get_prev_without_last_item(self, prev_item, column):
        for i, x in enumerate(column):
            if(x.contains_item(prev_item)):
                return column[i - 1]
        return column[0]

    def __add_item_to_table(self, item):
        for x in range(len(self.__table[0])):
            if(x >= item.weight):
                # Si el peso de los items que ya tiene mas el actual es menor o igual que el tamano de la mochila
                if(self.__table[self.__table_index - 1][x].total_weight + item.weight <= x):
                    self.__table[self.__table_index][x] = deepcopy(
                        self.__table[self.__table_index - 1][x])
                    self.__table[self.__table_index][x].add_item(item)
                else:
                    prev = self.__table[self.__table_index - 1][x]
                    prev_without_item = self.__get_prev_without_last_item(prev.get_last_item(), self.__table[self.__table_index - 1]) # self.__table[self.__table_index - 1][x].get_without_last_item()
                    if(prev_without_item.could_add_item(item, x) and prev_without_item.evaluate_value(item) > prev.total_value):
                        self.__table[self.__table_index][x] = deepcopy(prev_without_item)
                        self.__table[self.__table_index][x].add_item(item)
                    elif (self.__table[self.__table_index - 1][x].total_value > self.__table[self.__table_index][x - 1].total_value):
                        self.__table[self.__table_index][x] = deepcopy(
                            self.__table[self.__table_index - 1][x])
                    else:
                        self.__table[self.__table_index][x] = deepcopy(self.__table[self.__table_index][x - 1])                        
            else:
                self.__table[self.__table_index][x] = deepcopy(
                    self.__table[self.__table_index - 1][x])
        if(self.__table_index < len(self.__table) - 1):
            self.__table_index += 1

    def __generate_table(self, items, capacity):
        self.__table = []
        self.__table_index = 1
        for x in range(len(items) + 1):
            self.__table.append([TableCell() for y in range(capacity + 1)])
        return self.__table

    def print_table(self):
        i = 0
        first_line = "Capacity | "
        for x in range(len(self.__table)):
            first_line += str(x).rjust(4) + "   "
        print(first_line)
        separator = ""
        for x in first_line:
            separator += "_"
        print(separator)
        while(i < len(self.__table[0])):
            line = str(i).rjust(8) + " | "
            for x in range(len(self.__table)):
                line += str(self.__table[x][i].total_value).rjust(4) + "   "
            print(line)
            i += 1

    """
     def __add_item_to_table(self, item):
        for x in range(len(self.__table[0])):
            if(x >= item.weight):
                # Si el peso de los items que ya tiene mas el actual es menor o igual que el tamano de la mochila
                if(self.__table[self.__table_index - 1][x].total_weight + item.weight <= x):
                    self.__table[self.__table_index][x] = deepcopy(
                        self.__table[self.__table_index - 1][x])
                    self.__table[self.__table_index][x].add_item(item)
                else:
                    # vemos cual es mas valioso
                    # Si los dos entran, el actual se tiene que comparar contra el primer anterior distinto de cero
                    if(item.value > self.__get_first_cell_with_value_disctint_than_zero(self.__table[self.__table_index - 1]).total_value):
                        self.__table[self.__table_index][x].add_item(item)
                    elif (self.__table[self.__table_index - 1][x].total_value > self.__get_first_cell_with_value_disctint_than_zero(self.__table[self.__table_index - 1]).total_value and
                        self.__get_first_cell_with_value_disctint_than_zero(self.__table[self.__table_index - 1]).total_weight + item.weight <= x and
                        self.__table[self.__table_index - 1][x].total_value < self.__get_first_cell_with_value_disctint_than_zero(self.__table[self.__table_index - 1]).total_value + item.value):
                        print("ENTRO:", self.__table_index, x)
                        self.__table[self.__table_index][x] = deepcopy(self.__get_first_cell_with_value_disctint_than_zero(self.__table[self.__table_index - 1]))
                        self.__table[self.__table_index][x].add_item(item)
                    else:
                        self.__table[self.__table_index][x] = deepcopy(
                            self.__table[self.__table_index - 1][x])
            else:
                self.__table[self.__table_index][x] = deepcopy(
                    self.__table[self.__table_index - 1][x])
        if(self.__table_index < len(self.__table) - 1):
            self.__table_index += 1
    """
