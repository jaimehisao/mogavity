import sys
import logging


class Function:
    id: str
    return_type: str
    variable_table = {}

    def __init__(self, _id, return_type):
        self.variable_table = {}
        self.id = _id
        self.return_type = return_type


class Variable:
    id: str
    type: str
    address: int

    def __init__(self, _id, _type, address):
        self.id = _id
        self.type = _type
        self.address = address


constants_table = {}  # We have this dictionary to hold our constants


class FunctionDirectory:
    def __init__(self):
        self.function_table = {"global": Function("global", "void")}
        self.tmp_type = ""

    def add_function(self, identifier, return_type):
        """
        Add new function scope to the Function Table
        """
        if identifier in self.function_table.keys():
            logging.error('Function ' + identifier + ' already exists!')  # Might be redundant but important in case
            # we export the logs to a file
            error('Function ' + identifier + ' already exists!')
        else:
            self.function_table[identifier] = Function(identifier, return_type)
            logging.info("Scope " + identifier + " created!")

    def add_global_variable(self, identifier, data_type):
        self.function_table['global']['vars'][identifier] = {'data_type': data_type,
                                                             'address': None}

    def add_variable(self, identifier, scope, _type):
        logging.info("Added variable with ID " + identifier + " in scope " + scope + " and type " + _type)
        self.function_table[scope].variable_table[identifier] = Variable(identifier, _type,
                                                                         0)  ## TODO fill address when we handle that

    def print_variable_table(self, current_scope):
        print(self.function_table[current_scope].variable_table)

    def print_all_variable_tables(self):
        for key, value in self.function_table.items():
            print(key, ' : ', value.variable_table)

        # TODO cleanup pending on certain functions

    def add_function_variables(self):
        """This is called after vars is detected inside a function, we will need a way to manage the scope"""
        pass

    def remove(self, identifier):
        """Removes Scope from the table"""
        self.function_table.pop(identifier)

    def check_if_exists(self, identifier):
        """Will verify if the given scope exists in the function table"""
        if identifier in self.function_table.keys():
            return True
        else:
            return False

    def check_for_vars(self, identifier):
        if "vars" in self.function_table[identifier].keys():
            error("Vars Table already exists for this function")
            return True
        else:
            return False

    def get_var_type(self, identifier, scope):
        print("SCOPEEEEE " + scope)
        var_in_global_scope_type = None
        var_in_local_scope_type = None
        # Check for variable in global scope
        if scope is not "global":
            if identifier in self.function_table["global"].variable_table.keys():
                var_in_global_scope_type = self.function_table["global"].variable_table[identifier].type
            else:
                print("Var " + identifier + " is not in global scope!")
        # Check for variable in local scope
        if identifier in self.function_table[scope].variable_table.keys():
            var_in_local_scope_type = self.function_table[scope].variable_table[identifier].type

        if scope is "global":
            return var_in_local_scope_type
        else:
            if var_in_global_scope_type is not None and var_in_local_scope_type is not None:
                warning("Variable " + identifier + " exists in global scope")
                return var_in_local_scope_type  # Local Scope maintains preference over global scope
            elif var_in_local_scope_type is not None:
                return var_in_local_scope_type
            elif var_in_global_scope_type is not None:
                return var_in_global_scope_type
            else:
                error("Variable " + identifier + " has not been declared")

    def add_elements(self, identifier, elem_type):
        self.function_table = {'identifier': identifier, 'type': elem_type}


def error(message: str):
    print(message)  # use raise?
    sys.exit()


def warning(message: str):
    print("WARNING -> " + message)  # use raise?

