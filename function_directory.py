import logging
from tkinter.ttk import Sizegrip
from memory_manager import MemoryManager

from error_handling import error, warning, info

class NodeArray:
    m: int
    k: int
    lim_inf: int
    lim_sup: int
    next_node = None
    
    def __init__(self, r = 0, m = 0, k = 0, lim_inf = 0, lim_sup = 0, next_node = None) -> None:
        self.r = r
        self.m = m
        self.k = k
        self.lim_inf = lim_inf
        self.lim_sup = lim_sup
        self.next_node = next_node

class Function:
    id: str
    return_type: str

    #  Tables
    variable_table = {}  # id: Variable(id, type, address)
    constants_table = {}  # key(constant): address (only in global)
    parameter_table_types = []  # [type1 ... typeN]
    parameter_table = []  # (id, addr)
    resources_size = {}  # Dict to store the resources needed to calculate the workspace required
    starting_quadruple: int
    memory_manager: MemoryManager

    number_of_ints: int
    number_of_floats: int

    def __init__(self, _id, return_type):
        self.variable_table = {}
        self.constants_table = {}
        self.parameter_table_types = []
        self.parameter_table = []
        self.id = _id
        self.return_type = return_type
        if _id == "global":
            self.memory_manager = MemoryManager(True)
        else:
            self.memory_manager = MemoryManager(False)

    def add_variable(self, identifier, _type):
        address = ""
        if _type == "int":
            address = self.memory_manager.assign_new_int_address()
            self.variable_table[identifier] = Variable(
                identifier, _type, address)
        elif _type == "float":
            address = self.memory_manager.assign_new_float()
            self.variable_table[identifier] = Variable(
                identifier, _type, address)
        elif _type == "char":
            address = self.memory_manager.assign_new_char()
            self.variable_table[identifier] = Variable(
                identifier, _type, address)
        logging.info(
            "Added variable with ID "
            + identifier
            + " in scope "
            + self.id
            + " with type "
            + _type
            + " and address "
            + str(address)
        )
        return address

    def get_constant(self, cte_value):
        if cte_value not in self.constants_table.keys():
            addr = self.memory_manager.assign_new_constant()
            self.constants_table[cte_value] = addr
            return addr
        else:
            return self.constants_table[cte_value]
            #  TODO might be problematic when storing different types as keys will differ (eg, ints and chars)

    # Set the amount of temporals used
    def set_temporals(self, temporals):
        self.resources_size["temporals"] = temporals

    # Set the initial address (current quad)
    def set_quadruple(self, quad_id):
        self.starting_quadruple = quad_id

    # Deletes the local var table
    def release_var_table(self):
        pass
        #self.variable_table.clear()

    # Set the amount of local variables defined
    def set_vars(self):
        self.resources_size["vars"] = len(self.variable_table)

    # We add the type of parameter into our Params list
    def add_param(self, _type):
        self.parameter_table_types.append(_type)

    # Set the amount of params defined
    def set_params(self, params):
        if params == len(self.parameter_table_types):
            self.resources_size["params"] = len([params])  # TODO parche
        else:
            error("Incorrect number of Parameters")

    # Get the size of resources
    def get_resources_size(self):
        return self.resources_size["temporals"] + self.resources_size["vars"] + self.resources_size["params"]

    # Mark the variable as an array
    def set_array(self, identifier):
        self.variable_table[identifier].has_dimensions = True

    # Store the node within the array variable
    def add_node(self, identifier, node : NodeArray):
        self.variable_table[identifier].nodes.append(node)

    # Get the first node of the array varible
    def get_first_node(self, identifier):
        return self.variable_table[identifier].nodes[0]

    # Get the last node of the array varible
    def get_last_node(self, identifier):
        return self.variable_table[identifier].nodes[-1]


class Variable:
    id: str
    type: str
    address: int
    has_dimensions: bool
    nodes = []  # NodeArray

    def __init__(self, _id, _type, address, has_dimensions = False):
        self.id = _id
        self.type = _type
        self.address = address
        self.has_dimensions = has_dimensions
        self.nodes = []


class FunctionDirectory:
    def __init__(self):
        self.function_table = {"global": Function("global", "void")}
        self.tmp_type = ""

    def add_function(self, identifier, return_type):
        """
        Add new function scope to the Function Table
        """
        if identifier in self.function_table.keys():
            logging.error(
                "Function " + identifier + " already exists!"
            )  # Might be redundant but important in case
            # we export the logs to a file
            error("Function " + identifier + " already exists!")
        else:
            self.function_table[identifier] = Function(identifier, return_type)
            logging.info("Scope " + identifier + " created!")

    def add_global_variable(self, identifier, data_type):
        self.function_table["global"]["vars"][identifier] = {
            "data_type": data_type,
            "address": None,
        }
        # print("x-x-x-x", self.function_table[scope].variable_table[identifier].id,
        # self.function_table[scope].variable_table[identifier].type,
        # self.function_table[scope].variable_table[identifier].address)

    def print_variable_table(self, current_scope):
        pass
        #info(str(self.function_table[current_scope].variable_table))

    def print_all_variable_tables(self):
        pass
        for key, value in self.function_table.items():
            print(key, " : ", value.variable_table)

        # TODO cleanup pending on certain functions

    def add_function_variables(self):
        """This is called after vars is detected inside a function, we will need a way to manage the scope"""
        pass

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
        var_in_global_scope_type = None
        var_in_local_scope_type = None
        # Check for variable in global scope
        if scope != "global":
            if identifier in self.function_table["global"].variable_table.keys():
                var_in_global_scope_type = (
                    self.function_table["global"].variable_table[identifier].type
                )
            else:
                info("Var " + str(identifier) + " is not in global scope!")
        # Check for variable in local scope
        if identifier in self.function_table[scope].variable_table.keys():
            var_in_local_scope_type = (
                self.function_table[scope].variable_table[identifier].type
            )
        if scope == "global":
            return var_in_local_scope_type
        else:
            if (
                    var_in_global_scope_type is not None
                    and var_in_local_scope_type is not None
            ):
                warning("Variable " + identifier + " exists in global scope")
                return var_in_local_scope_type  # Local Scope maintains preference over global scope
            elif var_in_local_scope_type is not None:
                return var_in_local_scope_type
            elif var_in_global_scope_type is not None:
                return var_in_global_scope_type
            else:
                error("Variable " + str(identifier) + " has not been declared previously!")

    def add_elements(self, identifier, elem_type):
        self.function_table = {"identifier": identifier, "type": elem_type}

    def check_if_function_exists(self, identifier, line_no):
        if identifier not in self.function_table.keys():
            error("Function " + identifier + " on line " + line_no + " does not exist!")

    def get_function(self, identifier) -> Function:
        return self.function_table[identifier]

    def get_variable_address(self, identifier, scope):
        # Check for variable in global scope
        print("SCOPE", scope, "ID", identifier)
        #print(self.function_table["global"].variable_table.keys())
        var_in_global_scope_address = None
        var_in_local_scope_address = None
        if scope != "global":
            if identifier in self.function_table["global"].variable_table.keys():
                var_in_global_scope_address = self.function_table["global"].variable_table[identifier].address
                #print("var_in_global_scope_address", var_in_global_scope_address)
            else:
                info("Var " + identifier + " is not in global scope!")
        # Check for variable in local scope
        if identifier in self.function_table[scope].variable_table.keys():
            var_in_local_scope_address = self.function_table[scope].variable_table[identifier].address
            #print("var_in_local_scope_address", var_in_local_scope_address)
        if scope == "global":
            return var_in_local_scope_address
        else:
            if (
                    var_in_global_scope_address is not None
                    and var_in_local_scope_address is not None
            ):
                warning("Variable " + identifier + " exists in global scope")
                return var_in_local_scope_address  # Local Scope maintains preference over global scope
            elif var_in_local_scope_address is not None:
                return var_in_local_scope_address
            elif var_in_global_scope_address is not None:
                return var_in_global_scope_address
            else:
                error("Variable " + identifier + " has not been declared previously!")


    def get_var_from_address(self, scope, address):
        for key, item in self.function_table[scope].variable_table.items():
            #print("KEY AND ITEM", key, item.address)
            if str(item.address) == str(address):
                return item
    #  TODO move to Function class

    def get_constant(self, cte_value):
        if cte_value not in self.function_table["global"].constants_table.keys():
            addr = self.function_table["global"].memory_manager.assign_new_constant()
            self.function_table["global"].constants_table[cte_value] = addr
            return addr
        else:
            return self.function_table["global"].constants_table[cte_value]
            #  TODO might be problematic when storing different types as keys will differ (eg, ints and chars)
