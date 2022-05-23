"""
virtual_machine.py - Virtual Machine for the Mogavity Compiler
The VM for the Mogavity compiler is an efficient machine that helps us run the intermediate code
generated during compilation.
"""
from function_directory import FunctionDirectory
from quadruple import Quadruple
from constants import STARTING_ADDRESS, GLOBAL_OFFSET
from error_handling import info


class ExecutionMemory:
    """This way we can handle memory in scopes rather than having a ton of variables."""
    ## TODO check if overflow validation should be done here or is it fine with the one we already do
    def __init__(self):
        self.scope_memory = {}

    def insert(self, address, value):
        self.scope_memory[address] = value

    def get_value_by_address(self, address):
        return self.scope_memory[address]


global_memory = ExecutionMemory()
local_memory = ExecutionMemory()


def start_virtual_machine(function_directory: FunctionDirectory, quadruples: [Quadruple]):
    print("")
    print("")
    print("")
    print("")
    print("")
    print("Starting the Mogavity Virtual Machine")
    ## Initial VM Declarations

    instruction_pointer = 1

    #  Load Global Memory
    global_scope = function_directory.function_table["global"]

    #  Constants are stored in a table only inside the global scope, so we load them from here
    # print(global_scope.constants_table)
    for constant, addr in global_scope.constants_table.items():
        ## TODO make sure compatibility is validated.
        save_to_memory(addr, constant)

    # print(global_memory.scope_memory)

    while quadruples[instruction_pointer][1] != "EOF":
        print("Quad", quadruples[instruction_pointer][0])
        #print(global_memory.scope_memory)
        # quadruples[instruction_pointer].print_quad()

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
            print("Hey im hewre")
            value = bool(left < right)
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == ">":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left > right)
            print("resval",res, value)
            save_to_memory(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "!=":
            left = get_var_from_address(quadruples[instruction_pointer][2])
            right = get_var_from_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left != right)
            save_to_memory(res, value)
            instruction_pointer += 1
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
            info("GOTO detected, changing IP to quadruple " + str(quadruples[instruction_pointer][4]))
            instruction_pointer = quadruples[instruction_pointer][4]
        elif quadruples[instruction_pointer][1] == "GOTOF":
            # print("GOTOF",quadruples[instruction_pointer][2])
            #print("GOTOF VAL", get_var_from_address(quadruples[instruction_pointer][2]))
            if not get_var_from_address(quadruples[instruction_pointer][2]):
                info("GOTOF detected, changing IP to quadruple " + str(quadruples[instruction_pointer][4]))
                instruction_pointer = quadruples[instruction_pointer][4] - 1
                continue
            else:
                instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "ENDFUNC":
            instruction_pointer += 1

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

def get_var_from_address(address):
    if is_global_variable(address):
        return global_memory.get_value_by_address(address)
    else:
        return local_memory.get_value_by_address(address)


def save_to_memory(address, val):
    if is_global_variable(address):
        global_memory.insert(address, val)
    else:
        local_memory.insert(address, val)


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
