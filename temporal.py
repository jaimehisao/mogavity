import sys

class Temporal:

    def __init__(self):
        self.id = 0
        self.type = ""

    def get_temp(self, type):
        self.id += 1
        temp = ("t"+self.id, type)
        return temp
