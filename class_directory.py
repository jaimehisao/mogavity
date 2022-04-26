from dataclasses import dataclass
import variable_table
import function_directory

@dataclass()
class Class:
    class_id: str
    attrs: variable_table
    methods: function_directory

class ClassDirectory:
    def __init__(self):
        self.class_table = {}

    def add(self, identifier):
        self.class_table[identifier] = Class(identifier)

    def check_if_exists(self, identifier):
        if identifier in self.class_table.keys():
            print('Class ' + identifier + ' already exists!')
            return True
        else:
            return False

    def add_attrs(self, identifier, vars_table):
        self.class_table[identifier]['attrs'] = vars_table

    def add_methods(self, identifier, func_table):
        self.class_table[identifier]['methods'] = func_table