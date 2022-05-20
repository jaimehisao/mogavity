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

    ## Initial VM Declarations
    global_memory = ExecutionMemory()

    instruction_pointer = 1

    #  Load Global Memory
    global_scope = function_directory.function_table["global"]

    #  Constants are stored in a table only inside the global scope, so we load them from here
    print(global_scope.constants_table)
    for constant, addr in global_scope.constants_table.items():
        ## TODO make sure compatibility is validated.
        global_memory.insert(addr, constant)

    print(global_memory.scope_memory)

    while quadruples[instruction_pointer][1] != "EOF":

        if quadruples[instruction_pointer][1] == "=":
            pass
        elif quadruples[instruction_pointer][1] == "+":
            pass
        elif quadruples[instruction_pointer][1] == "-":
            pass
        elif quadruples[instruction_pointer][1] == "/":
            pass
        elif quadruples[instruction_pointer][1] == "*":
            pass
        elif quadruples[instruction_pointer][1] == "output":
            pass
        elif quadruples[instruction_pointer][1] == "input":
            pass











