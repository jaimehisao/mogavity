"""
virtual_machine.py - Virtual Machine for the Mogavity Compiler
The VM for the Mogavity compiler is an efficient machine that helps us run the intermediate code
generated during compilation.
"""
from function_directory import FunctionDirectory
from quadruple import Quadruple

class ExecutionMemory:
    """This way we can handle memory in scopes rather than having a ton of variables."""

    ## TODO check if overflow validation should be done here or is it fine with the one we already do
    def __init__(self):
        self.scope_memory = {}

    def insert(self, address, value):
        self.scope_memory[address] = value

    def get_value_by_address(self, address):
        return self.scope_memory[address]


def start_virtual_machine(function_directory: FunctionDirectory, quadruples: [Quadruple]):
    print("")
    print("")
    print("")
    print("")
    print("")
    print("START VM")
    ## Initial VM Declarations
    global_memory = ExecutionMemory()

    instruction_pointer = 1

    #  Load Global Memory
    global_scope = function_directory.function_table["global"]

    #  Constants are stored in a table only inside the global scope, so we load them from here
    #print(global_scope.constants_table)
    for constant, addr in global_scope.constants_table.items():
        ## TODO make sure compatibility is validated.
        global_memory.insert(addr, constant)

    #print(global_memory.scope_memory)

    while quadruples[instruction_pointer][1] != "EOF":
        #print("Quad", quadruples[instruction_pointer][0])
        #print(global_memory.scope_memory)
        #quadruples[instruction_pointer].print_quad()

        if quadruples[instruction_pointer][1] == "=":
            value = global_memory.get_value_by_address(quadruples[instruction_pointer][2])
            print("VALUE TYPE", type(value))
            addr = quadruples[instruction_pointer][4]
            global_memory.insert(addr, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "+":
            left = global_memory.get_value_by_address(quadruples[instruction_pointer][2])
            right = global_memory.get_value_by_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left + right
            print(left, right, value)
            global_memory.insert(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "-":
            left = global_memory.get_value_by_address(quadruples[instruction_pointer][2])
            right = global_memory.get_value_by_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left - right
            global_memory.insert(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "/":
            left = global_memory.get_value_by_address(quadruples[instruction_pointer][2])
            right = global_memory.get_value_by_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left / right
            global_memory.insert(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "*":
            left = global_memory.get_value_by_address(quadruples[instruction_pointer][2])
            right = global_memory.get_value_by_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = left * right
            global_memory.insert(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "<":
            left = global_memory.get_value_by_address(quadruples[instruction_pointer][2])
            right = global_memory.get_value_by_address(quadruples[instruction_pointer][3])
            res = quadruples[instruction_pointer][4]
            value = bool(left < right)
            print(res,"Value", value, type(value))
            global_memory.insert(res, value)
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "GOTO":
            print("Changing IP based on GOTO to Q", quadruples[instruction_pointer][4])
            instruction_pointer = quadruples[instruction_pointer][4]
        elif quadruples[instruction_pointer][1] == "GOTOF":
            #print("GOTOF",quadruples[instruction_pointer][2])
            if not quadruples[instruction_pointer][2]:
                print("Changing IP to ", quadruples[instruction_pointer][4], quadruples[instruction_pointer][2])
                instruction_pointer = quadruples[instruction_pointer][4]
            else:
                instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "ENDFUNC":
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "OUTPUT":
            print(str(global_memory.get_value_by_address(quadruples[instruction_pointer][4])))
            instruction_pointer += 1
        elif quadruples[instruction_pointer][1] == "input":
            ## res = input()
            ## assign to memory
            instruction_pointer += 1











