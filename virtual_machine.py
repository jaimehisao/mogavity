"""
virtual_machine.py - Virtual Machine for the Mogavity Compiler
The VM for the Mogavity compiler is an efficient machine that helps us run the intermediate code
generated during compilation.
"""
from function_directory import FunctionDirectory, Function
from quadruple import Quadruple
from constants import STARTING_ADDRESS, GLOBAL_OFFSET
from error_handling import info, error
from Stack import Stack


class ExecutionMemory:
    """This way we can handle memory in scopes rather than having a ton of variables."""

    ## TODO check if overflow validation should be done here or is it fine with the one we already do
    def __init__(self, _id):
        self.scope_memory = {}
        self.id = _id

    def insert(self, address, value):
        self.scope_memory[address] = value

    def get_value_by_address(self, address):
        return self.scope_memory[address]

    def return_val(self):
        return self.scope_memory


global current_local_memory
current_local_memory = ExecutionMemory(None)
global_memory = ExecutionMemory("global")

memory_stack = Stack()  # To store different memory segments
memory_stack.push(global_memory)
pending_jumps = []  # Addresses to return to previous point of executions


def start_virtual_machine(function_directory: FunctionDirectory, quadruples: [Quadruple]):
    print("")
    print("")
    print("")
    print("")
    print("")
    print("Starting the Mogavity Virtual Machine")
    pending_jumps.append(len(quadruples) - 1)  # TODO parche
    ## Initial VM Declarations

    instruction_pointer = 0
    #  Load Global Memory
    global_scope = function_directory.function_table["global"]
    print("Global scope", global_scope)

    #  Constants are stored in a table only inside the global scope, so we load them from here
    # print(global_scope.constants_table)
    #####################
    # LOADING CONSTANTS #
    #####################
    for constant, addr in global_scope.constants_table.items():
        ## TODO make sure compatibility is validated.
        save_to_memory(addr, constant)

    #####################
    # LOADING CONSTANTS #
    #####################

    #####################
    #  LOADING LOCALS   #
    #####################

    # print(global_memory.scope_memory)

    while quadruples[instruction_pointer][1] != "EOF":
        # print("Quad", quadruples[instruction_pointer][0])
        # rint(global_memory.scope_memory)
        quadruples[instruction_pointer].print_quad()
        global current_local_memory

        ##############
        # ASSIGNMENT #
        ##############
        if quadruples[instruction_pointer][1] == "=":
            value = get_var_from_address(quadruples[instruction_pointer][2])
            addr = quadruples[instruction_pointer][4]
            save_to_memory(addr, value)
            instruction_pointer += 1

        ##############
        # ARITHMETIC #
        ##############
        elif quadruples[instruction_pointer][1] == "+":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left + right
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "-":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left - right
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "/":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left / right
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "*":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left * right
            save_to_memory(res, value)
            instruction_pointer += 1

        ##############
        # COMPARISON #
        ##############
        elif quadruples[instruction_pointer][1] == "<":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left < right)
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == ">":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left > right)
            print("resval", res, value)
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "!=":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left != right)
            save_to_memory(res, value)
            instruction_pointer += 1
        ############
        # BOOLEANS #
        ############
        elif quadruples[instruction_pointer][1] == "AND":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left and right)
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "OR":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left or right)
            save_to_memory(res, value)
            instruction_pointer += 1

        ########
        # GOTO #
        ########
        elif quadruples[instruction_pointer][1] == "GOTO":
            # if quadruples[instruction_pointer][4] is not None:
            info("GOTO detected, changing IP to quadruple " + str(quadruples[instruction_pointer][4] - 1))
            instruction_pointer = quadruples[instruction_pointer][4] - 1
            ## TODO ALERTA DE PARCHE AQUI; PROBLEMA DE GOTO o bueno talvez ya no
            # else:
            # instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "GOTOF":
            # print("GOTOF",quadruples[instruction_pointer][2])
            # print("GOTOF VAL", get_var_from_address(quadruples[instruction_pointer][2]))
            if not get_var_from_address(quadruples[instruction_pointer][2]):
                info("GOTOF detected, changing IP to quadruple " + str(quadruples[instruction_pointer][4]))
                instruction_pointer = quadruples[instruction_pointer][4] - 1
                continue
            else:
                instruction_pointer += 1

        #############
        # FUNCTIONS #
        #############
        elif quadruples[instruction_pointer][1] == "PARAMETER":
            # Obtain paramater index
            paramIndex = quadruples[instruction_pointer][2] - 1  ## ???
            # print(current_local_memory.return_val())
            origin_value = get_var_from_address(quadruples[instruction_pointer][2])
            destination_address_in_new_scope = quadruples[instruction_pointer][4]
            memory_stack.top().scope_memory[destination_address_in_new_scope] = origin_value
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "ERA":
            function_name = quadruples[instruction_pointer][4]  # Get the name of function to load
            function = function_directory.get_function(function_name)
            scope_memory = ExecutionMemory(function.id)  # Create Memory Segment
            for _, var in function.variable_table.items():
                # print(var.address, var.id)
                scope_memory.insert(var.address, None)
            # print(scope_memory.return_val())
            memory_stack.push(scope_memory)  # Load into memory_stack
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "GOSUB":
            global current_local_memory
            pending_jumps.append(instruction_pointer + 1)  # Add where we are to return after execution
            info("Function Invocation - moving execution to quadruple " + str(quadruples[instruction_pointer][4]))
            current_local_memory = memory_stack.top()
            instruction_pointer = quadruples[instruction_pointer][4] - 1  # Send IP to Function Start

        elif quadruples[instruction_pointer][1] == "RETURN":
            #  Guardar Valor de Retorno en Memoria global (hay que obtener direccion antes)
            instruction_pointer += 1

        elif quadruples[instruction_pointer][1] == "ENDFUNC":
            return_pointer = 0
            if not (memory_stack.size() <= 1):
                trashed_mem = memory_stack.pop()  # Offload memory
                # print("TRASHED MEM " + trashed_mem.id)
                # print(trashed_mem.return_val())
                new_memory = memory_stack.top()
                # print("NEW MEM " + new_memory.id)
                # print(new_memory.return_val())
                # print("GLOBAL MEM")
                # print(global_memory.return_val())
                current_local_memory = new_memory
                return_pointer = pending_jumps.pop()
                info("End of function - returning execution to quadruple " + str(return_pointer))
                instruction_pointer = return_pointer
                continue
            info("End of Program")
            instruction_pointer += 1

        ##########
        # ARRAYS #
        ##########
        elif quadruples[instruction_pointer][1] == "VERIFY":

            # Verificar out of bounds
            limit_i = quadruples[instruction_pointer][3]
            limit_s = quadruples[instruction_pointer][4]
            cell = get_var_from_address(quadruples[instruction_pointer][2]) 

            if cell >= limit_i and cell <= limit_s:
                instruction_pointer += 1
            else:
                error("Array access is out of bouds")

        #######
        # I/O #
        #######
        elif quadruples[instruction_pointer][1] == "OUTPUT":
            print(str(get_var_from_address(quadruples[instruction_pointer][4])))
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "INPUT":
            #  here theres an issue, because if it is a constant, the address is generic and doesnt specify a type,
            #  so we cant do a cast based on object type execpt if it comes with a specific address (we can do that later)
            #  TODO force type compatibility on non constants based on recieved address.
            res = input()
            if is_digit(res):
                res = int(res)
            elif is_float(res):
                res = float(res)
            save_to_memory(quadruples[instruction_pointer][4], res)
            instruction_pointer += 1


###########
# HELPERS #
###########
## TODO validate no trash in var

def get_var_from_address(address):
    global current_local_memory
    print("global", global_memory.return_val())
    print("local", current_local_memory.return_val())
    if is_global_variable(address):
        return global_memory.get_value_by_address(address)
    else:
        return current_local_memory.get_value_by_address(address)


def save_to_memory(address, val):
    global current_local_memory
    if is_global_variable(address):
        global_memory.insert(address, val)
        # print("SAVED " + str(val) + " to address " + str(address))
    else:
        current_local_memory.insert(address, val)
        # print("SAVED " + str(val) + " to address " + str(address))


def is_global_variable(address):
    if address >= (STARTING_ADDRESS + GLOBAL_OFFSET):
        return True
    return False


def is_float(check_input):
    if '.' in check_input:
        split_number = check_input.split('.')
        if len(split_number) == 2 and split_number[0].isdigit() and split_number[1].isdigit():
            return True
    return False


def is_digit(check_input):
    if check_input.isdigit():
        return True
    return False
