from dataclasses import dataclass
import sys


@dataclass()
class Function:
    id: str
    return_type: str


class FunctionDirectory:
    def __init__(self):
        self.function_table = {"global": {}}  # Initialize with global scope already

    def add_function(self, identifier):
        """
        Add new function scope to the Function Table
        """
        if identifier in self.function_table.keys():
            error('Function ' + identifier + ' already exists!')
        else:
            self.function_table[identifier] = {}
            print("Scope " + identifier + "Created!")

    def add_global_variable(self, identifier, data_type):
        self.function_table['global']['vars'][identifier] = {'data_type': data_type,
                                                             'address': None}

    def add_function_variables(self):
        """This is called after vars is detected inside a function, we will need a way to manage the scope"""



    def remove(self, identifier):
        """Removes Scope from the table"""
        self.function_table.pop(identifier)

    def check_if_exists(self, identifier):
        """Will verify if the given scope exists in the function table"""
        if identifier in self.function_table.keys():
            return True
        else:
            return False

    def add_vars(self, identifier, vars_table):
        self.function_table[identifier]["vars"] = vars_table

    def check_for_vars(self, identifier):
        if "vars" in self.function_table[identifier].keys():
            error("Vars Table already exists for this function")
            return True
        else:
            return False


def error(message: str):
    print(message)  # use raise?
    sys.exit()
