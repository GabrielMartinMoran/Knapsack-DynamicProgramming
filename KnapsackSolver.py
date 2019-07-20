from TableCell import *
from copy import deepcopy

USE_BACKTRACE = True


class KnapsackSolver:

    def __init__(self):
        self.__table = None
        self.__table_index = 0

    def solve(self, items, capacity):
        print("Knapsack capacity:", capacity)
        sorted_items = self.__sort_items(items)
        self.__generate_table(sorted_items, capacity)
        for i_index, item in enumerate(sorted_items):
            self.__add_item_to_table(item)
        if(USE_BACKTRACE):
            return self.__backtrace_table(sorted_items)
        return self.__table[len(self.__table) - 1][capacity], self.__table

    def __backtrace_table(self, items):
        cell = TableCell()
        col = len(self.__table) - 1
        row = len(self.__table[0]) - 1
        while(col > 0):
            if(self.__table[col][row].total_value != self.__table[col - 1][row].total_value):
                item = items[col - 1]
                cell.add_item(item)
                dif = self.__table[col][row].total_value - item.value
                while(row > 1 and self.__table[col - 1][row - 1].total_value >= dif):
                    row -= 1
            col -= 1
        self.__validate_backtrace(cell)
        return cell, self.__table

    def __validate_backtrace(self, cell):
        quant_in = 0
        for x in self.__table[len(self.__table) - 1][len(self.__table[0]) - 1].items:
            for y in cell.items:
                if(x.id == y.id):
                    quant_in += 1
        if((quant_in != len(cell.items) or len(cell.items) != len(self.__table[len(self.__table) - 1][len(self.__table[0]) - 1].items)) and
                (cell.total_value != self.__table[len(self.__table) - 1][len(self.__table[0]) - 1].total_value)):
            print("Validacion de backtrace erronea!")
            print("El resultado correcto es:", [x.id for x in self.__table[len(
                self.__table) - 1][len(self.__table[0]) - 1].items])

    def __sort_items(self, items):
        return sorted(items, key=lambda item: item.value / item.weight, reverse=False)

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
                    self.__table[self.__table_index][x] = self.__table[self.__table_index - 1][x].clone()
                    self.__table[self.__table_index][x].add_item(item)
                else:
                    prev = self.__table[self.__table_index - 1][x]
                    prev_without_item = self.__get_prev_without_last_item(
                        prev.get_last_item(), self.__table[self.__table_index - 1])
                    if(prev_without_item.could_add_item(item, x) and prev_without_item.evaluate_value(item) > prev.total_value):
                        self.__table[self.__table_index][x] = prev_without_item.clone(
                        )
                        self.__table[self.__table_index][x].add_item(item)
                    elif (self.__table[self.__table_index - 1][x].total_value > self.__table[self.__table_index][x - 1].total_value):
                        self.__table[self.__table_index][x] = self.__table[self.__table_index - 1][x].clone()
                    else:
                        self.__table[self.__table_index][x] = self.__table[self.__table_index][x - 1].clone()
            else:
                self.__table[self.__table_index][x] = self.__table[self.__table_index - 1][x].clone()
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
