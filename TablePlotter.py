import matplotlib.pyplot as plt
import numpy as np


class TablePlotter:

    @staticmethod
    def __get_font_size(items_quantity):
        if(items_quantity >= 30):
            return 5
        if(items_quantity >= 25):
            return 6
        if(items_quantity >= 20):
            return 8
        return 10

    @staticmethod
    def plot_table(table):
        columns = []#['Capacidad']
        for x in range(len(table)):
            columns.append("Item " + str(x))
        row_labels = ["Capacidad: " + str(x) for x in range(len(table[0]))]
        cell_data = []
        row_colors = ['#d6e2d5' for x in range(len(table[0]))]
        column_colors = ['#c0d6e4' for x in columns]
        for x in table:
            cell_data.append([y.total_value for y in x])
        cell_data = np.transpose(cell_data)
        the_table = plt.table(cellText=cell_data, rowLabels=row_labels, colLabels=columns,
                              colColours=column_colors, rowColours=row_colors, loc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(TablePlotter.__get_font_size(len(table) + 1))
        plt.axis('off')
        plt.show()
