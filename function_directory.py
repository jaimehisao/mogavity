from dataclasses import dataclass


@dataclass()
class Function:
    id: str
    type: str


class FunctionDirectory:
    def __init__(self):
        self.function_table = {}
        self.function_table["global"] = {}

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

    def add_vars(self, identifier, vars_table):
        self.function_table[identifier]["vars"] = vars_table

    def check_for_vars(self, identifier):
        if "vars" in self.function_table[identifier].keys():
            print("Vars Table exists for this function")
            return True
        else:
            return False

    def add_elements(self, identifier, elem_type):
        self.function_table = {'identifier' : identifier, 'type' : elem_type}