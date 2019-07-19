class TableCell:
    
    def __init__(self):
        self.items = []
        self.total_value = 0
        self.total_weight = 0

    def add_item(self, item):
        self.items.append(item)
        self.total_value += item.value
        self.total_weight += item.weight

    def get_without_last_item(self):
        cell = TableCell()
        for x in self.items[:-1]:
            cell.add_item(x)
        return cell

    def get_last_item(self):
        return self.items[len(self.items) - 1]

    def contains_item(self, item):
        for x in self.items:
            if(x.id == item.id):
                return True
        return False

    # Devuelve true si el item que se quiere agregar entra en la mochila segun la capacidad pasada por parametro, pero no lo inserta
    def could_add_item(self, item, total_capacity):
        return self.total_weight + item.weight <= total_capacity
    
    #Devuelve el valor posible total si se agregara el item recibido por parametro
    def evaluate_value(self, item):
        return self.total_value + item.value

    def clone(self):
        cell = TableCell()
        #para que se pase por referencia
        for x in self.items:
            cell.add_item(x)
        return cell