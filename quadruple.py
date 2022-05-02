import string


import sys

class Quadruple:
    id: int
    operator: str
    left_operator: str
    right_operator: str
    result: str

    def __init__(self):
        self.id = 0
        self.quads = []

    def generate_quad(self, op, left_op, right_op, res):
        self.id += 1
        quad = Quadruple(self.id, op, left_op, right_op, res)
        self.quads.append(quad)

