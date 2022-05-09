import string


import sys


class Quadruple:
    id: int
    operator: str
    left_operator: str
    right_operator: str
    result: str

    def __init__(self, id, operator, left_operator, right_operator, result):
        self.id = id
        self.operator = operator
        self.left_operator = left_operator
        self.right_operator = right_operator
        self.result = result

    def generate_quad(self, op, left_op, right_op, res):
        self.id += 1
        quad = Quadruple(self.id, op, left_op, right_op, res)
        return quad

    def fill_quad(self, cont):
        self.result = cont

    def print_quad(self):
        print("[" + str(self.id) + "," + str(self.operator) + "," + str(self.left_operator) + "," + str(self.right_operator) + "," + str(self.result) + "]")

