from dataclasses import dataclass

@dataclass()
class Function:
    id: str
    type: str


class FunctionDirectory:
    def __init__(self):
        self.function_table = {}

    def add(self, identifier, func_type):
        if identifier in self.function_table.keys():
            print('Function ' + identifier + ' already exists!')
        else:
            self.function_table[id] = Function(identifier, func_type)

    def remove(self, identifier):
        self.function_table.pop(identifier)

    def check_if_exists(self, identifier):
        if identifier in self.function_table.keys():
            return True
        else:
            return False
