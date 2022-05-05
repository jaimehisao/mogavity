"""
WE ARE GOING TO SET UP AN ARBITRARY LIMIT OF 10K VARIABLES PER TYPE

SO 10000 LOCALS 10000 TEMPS 10000 CONSTANTS 10000

"""

MAX_INTS = 10000
MAX_FLOATS = 10000
MAX_CHARS = 10000


sleeping_memory = []



class MemoryManager:
    assigned_ints: int
    assigned_float: int
    assigned_chars: int

    def __init__(self):
        self.assigned_ints = 0
        self.assigned_float = 0
        self.assigned_chars = 0

    def assign_new_int(self, scope):
        if scope is not 'global':
            if self.assigned_ints < MAX_INTS:
                pass
        else:
            pass


    def assign_new_float(self):
        pass


    def assign_new_char(self):
        pass


    def clear_memory(self):
        pass


    def chloroform(self):
        pass


    def wake_up_sleeping_beauty(self):
        pass


