import sys


class Temporal:

    def __init__(self):
        self.id = 0
        self.type = ""

    def get_temp(self, _type):
        self.id += 1
        temp = ("t" + str(self.id), _type)
        return temp
