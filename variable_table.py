from dataclasses import dataclass


@dataclass()
class Variable:
    id: str
    type: str


class VariableTable:
    def __init__(self):
        self.variable_table = {}

    def add(self, identifier, var_type):
        if identifier in self.function_table.keys():
            print('Variable ' + identifier + ' already exists!')
        else:
            self.variable_table[id] = Variable(identifier, var_type)

    def remove(self, identifier):
        self.variable_table.pop(identifier)

    def check_if_exists(self, identifier):
        if identifier in self.variable_table.keys():
            return True
        else:
            return False
