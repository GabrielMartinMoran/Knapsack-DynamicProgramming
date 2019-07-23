from TableCell import *
from copy import deepcopy

USE_BACKTRACE = True


class KnapsackSolver:

    def __init__(self):
        self.__table = None
        self.__table_index = 0

    def solve(self, items, capacity):
        self.__generate_table(items, capacity)
        for i_index, item in enumerate(items):
            self.__add_item_to_table(item)
        if(USE_BACKTRACE):
            return self.__backtrace_table(items)
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
    """
    def __get_best_cell_where_fits(self, current_row, column, item):
        max_weight = current_row
        max_cell = column[0]
        for i in range(len(column)):
            if(current_row - i <= 0):
                return max_cell
            cell = column[current_row - i]
            evaluated_value = cell.evaluate_value(item)
            if(cell.could_add_item(item, max_weight) and evaluated_value > max_cell.total_value + item.value):
                max_cell = cell
    """

    def __get_previous_value_in_column(self, current_row, column):
        comparison_value = column[current_row].total_value
        for i in range(1, len(column)):
            if(current_row - i < 0):
                return column[0]
            if(column[current_row - i].total_value == comparison_value - column[current_row].get_last_item().value):
                return column[current_row - i]

    def __get_best_cell_where_fits(self, max_weight, column, item):
        prev_cell = column[max_weight]
        prev_cell_without_weight = column[max_weight - item.weight]
        cell_without_item = self.__get_previous_value_in_column(max_weight, column)
        ret = None
        prev_cell_value_for_compare = 0
        if(prev_cell.could_add_item(item, max_weight)):
            ret = prev_cell
            prev_cell_value_for_compare += item.value
        if(prev_cell_without_weight.could_add_item(item, max_weight) and prev_cell_without_weight.evaluate_value(item) > prev_cell_value_for_compare):
            ret = prev_cell_without_weight
        return ret

    def __add_item_to_table(self, item):
        for x in range(len(self.__table[0])):
            # ESTRUCTURA DE LA TABLA: self.__table [COLUMNA] [FILA]
            if(x >= item.weight):
                best_cell_where_fits = self.__get_best_cell_where_fits(
                    x, self.__table[self.__table_index - 1], item)
                if(best_cell_where_fits == None):
                    best_cell_where_fits = TableCell()
                else:
                    best_cell_where_fits = best_cell_where_fits.clone()
                best_cell_where_fits.add_item(item)
                # Comparamos la mejor celda donde entra el item contra la celda de la misma fila en la columna anterior
                if(best_cell_where_fits.total_value > self.__table[self.__table_index - 1][x].total_value):
                    self.__table[self.__table_index][x] = best_cell_where_fits
                else:
                    self.__table[self.__table_index][x] = self.__table[self.__table_index - 1][x].clone()
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
