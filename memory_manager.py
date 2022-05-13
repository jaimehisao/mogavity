"""
memory_manager.py - Mogavity's Memory Manager
Hisao Yesaki and Clarissa Velasquez

WE ARE GOING TO SET UP AN ARBITRARY LIMIT OF 10K VARIABLES PER TYPE
-----------------------------
-- INTS -- FLOATS -- CHARS --
-----------------------------

"""
import sys
import logging
from error_handling import error, info, warning
logging.basicConfig(level=logging.DEBUG)

STARTING_ADDRESS = 10000
MAX_PER_VAR = 10000

#  Stack that holds all the states that went to sleep, this way we make sure we escape the contexts in order.
# TODO: adapt to our own Stack implementation.
sleeping_memory = []


class MemoryManager:
    assigned_ints: int
    assigned_floats: int
    assigned_chars: int
    assigned_temps: int
    MAX_INTS: int
    MAX_FLOATS: int
    MAX_CHARS: int
    MAX_TEMPS: int

    def __init__(self):
        self.assigned_ints = STARTING_ADDRESS
        self.MAX_INTS = self.assigned_ints + MAX_PER_VAR - 1
        self.assigned_floats = self.MAX_INTS + 1
        self.MAX_FLOATS = self.assigned_floats + MAX_PER_VAR - 1
        self.assigned_chars = self.MAX_FLOATS + 1
        self.MAX_CHARS = self.assigned_chars + MAX_PER_VAR - 1
        self.assigned_temps = self.MAX_CHARS + 1
        self.MAX_TEMPS = self.assigned_temps + MAX_PER_VAR - 1

        """
        print("int", str(self.assigned_ints), str(self.MAX_INTS))
        print("float", str(self.assigned_float), str(self.MAX_FLOATS))
        print("char", str(self.assigned_chars), str(self.MAX_CHARS))
        print("tmp", str(self.assigned_temps), str(self.MAX_TEMPS))
        """

    def assign_new_int_address(self):
        if self.assigned_ints < self.MAX_INTS:
            assigned = self.assigned_ints
            self.assigned_ints += 1
            return assigned
        error("Too much Integer variables, please optimize!")

    def assign_new_float(self):
        if self.assigned_floats < self.MAX_FLOATS:
            assigned = self.assigned_floats
            self.assigned_floats += 1
            return assigned
        error("Too much Float variables, please optimize!")

    def assign_new_char(self):
        if self.assigned_chars < self.MAX_CHARS:
            assigned = self.assigned_chars
            self.assigned_chars += 1
            return assigned
        error("Too much Char variables, please optimize!")

    def assign_new_temp(self):
        if self.assigned_temps < self.MAX_TEMPS:
            assigned = self.assigned_temps
            self.assigned_temps += 1
            return assigned
        error("Too much Temporary variables, please optimize your operations!")

    def get_variable_from_address(self, address):
        print(address)
        if STARTING_ADDRESS <= address <= self.MAX_INTS:
            return "int"
        elif self.MAX_INTS + 1 <= address <= self.MAX_FLOATS:
            return "float"
        elif self.MAX_FLOATS + 1 <= address <= self.MAX_CHARS:
            return "char"
        elif self.MAX_CHARS + 1 <= address <= self.MAX_TEMPS:
            return "temp"
        else:
            error("Given address does not match any address type interval.")

    def get_variable_size_for_scope(self):
        """
        Our intermediate code generator needs the number of variables to calculate storage requirements.
        :return: Number of Integer, Float and Char Variables for the current scope.
        """
        number_of_int_variables = self.assigned_ints - STARTING_ADDRESS
        number_of_float_variables = self.assigned_floats - (self.MAX_INTS + 1)
        number_of_char_variables = self.assigned_chars - (self.MAX_FLOATS + 1)
        return number_of_int_variables, number_of_float_variables, number_of_char_variables

