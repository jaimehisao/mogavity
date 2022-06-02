import dataclasses


class Quadruple():
    temporary_register: int
    operator: int
    operand_a: str
    operand_b: str

    def __init__(self, operator, operand_a, operand_b, counter):
        self.operator = operator
        self.operand_a = operand_a
        self.operand_b = operand_b
        if counter is not None:
            self.temporary_register = counter


# Declaring the stacks for quadruple generation
quadruples = []
operand_stack = []
operator_stack = []
type_stack = []
goto_stack = []


def for_loop():
    pass


def if_conditional():
    pass


def while_loop():
    pass
