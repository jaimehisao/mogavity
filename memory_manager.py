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
from constants import STARTING_ADDRESS, MAX_PER_VAR, GLOBAL_OFFSET
from error_handling import error, info, warning

logging.basicConfig(level=logging.DEBUG)


class MemoryManager:
    is_global: bool
    assigned_ints: int
    assigned_floats: int
    assigned_temps: int
    assigned_constants: int
    assigned_poiners: int
    MAX_INTS: int
    MAX_FLOATS: int
    MAX_TEMPS: int
    MAX_CONSTANTS: int
    MAX_POINTERS: int

    def __init__(self, is_global: bool):
        self.is_global = is_global
        if self.is_global:
            self.assigned_ints = STARTING_ADDRESS + GLOBAL_OFFSET
        else:
            self.assigned_ints = STARTING_ADDRESS
        self.MAX_INTS = self.assigned_ints + MAX_PER_VAR - 1
        self.assigned_floats = self.MAX_INTS + 1
        self.MAX_FLOATS = self.assigned_floats + MAX_PER_VAR - 1
        self.assigned_temps = self.MAX_FLOATS + 1
        self.MAX_TEMPS = self.assigned_temps + MAX_PER_VAR - 1
        self.assigned_constants = self.MAX_TEMPS + 1
        self.MAX_CONSTANTS = self.assigned_constants + MAX_PER_VAR - 1
        self.assigned_poiners = self.MAX_CONSTANTS + 1
        self.MAX_POINTERS = self.assigned_poiners + MAX_PER_VAR - 1

    def assign_new_int_address(self):
        if self.assigned_ints < self.MAX_INTS:
            assigned = self.assigned_ints
            self.assigned_ints += 1
            return assigned
        error("Too many Integer variables, please optimize!")

    def assign_new_float(self):
        if self.assigned_floats < self.MAX_FLOATS:
            assigned = self.assigned_floats
            self.assigned_floats += 1
            return assigned
        error("Too many Float variables, please optimize!")

    def assign_new_temp(self):
        if self.assigned_temps < self.MAX_TEMPS:
            assigned = self.assigned_temps
            self.assigned_temps += 1
            return assigned
        error("Too many Temporary variables, please optimize your operations!")

    def assign_new_constant(self):
        if self.assigned_constants < self.MAX_CONSTANTS:
            assigned = self.assigned_constants
            self.assigned_constants += 1
            return assigned
        error("Too many Constants, please optimize your operations!")

    def assign_new_pointer(self):
        if self.assigned_poiners < self.MAX_POINTERS:
            assigned = self.assigned_poiners
            self.assigned_poiners += 1
            return assigned
        error("Too many Pointers!")

    """
        def set_new_virtual_address(self, _type, new_address):
        if _type == "int":
            if self.assigned_ints < self.MAX_INTS:
                self.assigned_ints = new_address
        elif _type == "float":
            if self.assigned_floats < self.MAX_FLOATS:
                self.assigned_floats = new_address
        else:
            if self.assigned_chars < self.MAX_CHARS:
                self.assigned_chars = new_address
    """

    def get_variable_type_from_address(self, address):
        """
        Returns the type of a variable, in string, depending on the address given.
        :param address: virtual address of the variable needed.
        :return: type of the requested variable.
        """
        if STARTING_ADDRESS <= address <= self.MAX_INTS:
            return "int"
        elif self.MAX_INTS + 1 <= address <= self.MAX_FLOATS:
            return "float"
        elif self.MAX_FLOATS + 1 <= address <= self.MAX_TEMPS:
            return "char"
        elif self.MAX_TEMPS + 1 <= address <= self.MAX_CONSTANTS:
            return "CTE"
        elif self.MAX_CONSTANTS + 1 <= address <= self.MAX_POINTERS:
            return "POINTER"
        else:
            error("Given address does not match any address type interval.")

    def get_variable_size_for_scope(self):
        """
        Our intermediate code generator needs the number of variables to calculate storage requirements.
        :return: Number of Integer, Float and Char Variables for the current scope.
        """
        number_of_int_variables = self.assigned_ints - STARTING_ADDRESS
        number_of_float_variables = self.assigned_floats - (self.MAX_INTS + 1)
        number_of_tmp_variables = self.assigned_temps - (self.MAX_FLOATS + 1)
        number_of_constants = self.assigned_constants - (self.MAX_TEMPS + 1)
        return number_of_int_variables, number_of_float_variables, number_of_tmp_variables, number_of_constants

    def is_address_global(self, address):
        if address < STARTING_ADDRESS + GLOBAL_OFFSET:
            return True
        else:
            return False
