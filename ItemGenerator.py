import json
import random
from datetime import datetime
import hashlib
from Item import *


class ItemGenerator:

    def __init__(self):
        pass

    def generate(self, max_quantity):
        template_json = None
        with open("ItemsTemplate.json", "r") as file:
            template_json = json.loads(file.read())
        items = []
        for x in range(max_quantity):
            picked = random.choice(template_json)
            item = Item(self.__generate_id(), self.__random_from_range(
                picked["weight"]), self.__random_from_range(picked["value"]), picked["image"])
            items.append(item)
        return items

    def __generate_id(self):
        now = datetime.now()
        word = str(now.microsecond) + str(now.second) + str(now.minute) + str(now.hour) + str(
            now.day) + str(now.month) + str(now.year) + str(random.randrange(1000000000, 9999999999))
        hashed_word = hashlib.sha256(bytes(word, "utf-8"))
        return hashed_word.hexdigest()

    def __random_from_range(self, range):
        return random.randrange(range[0], range[1])
