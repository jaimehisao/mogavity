import memory_manager

memory_manager = memory_manager.MemoryManager()


def test_assign_new_int_address_in_interval():
    assigned_address = memory_manager.assign_new_int_address()
    assert assigned_address >= 10000
    assert assigned_address <= 19999


def test_assign_new_float():
    assigned_address = memory_manager.assign_new_float()
    assert assigned_address >= 20000
    assert assigned_address <= 29999


def test_assign_new_char():
    assigned_address = memory_manager.assign_new_char()
    assert assigned_address >= 30000
    assert assigned_address <= 39000


def test_assign_new_temp():
    assigned_address = memory_manager.assign_new_temp()
    assert assigned_address >= 40000
    assert assigned_address <= 59000


def test_get_variable_from_address():
    assert memory_manager.get_variable_from_address(10000) == "int"
    assert memory_manager.get_variable_from_address(20000) == "float"
    assert memory_manager.get_variable_from_address(30000) == "char"
    assert memory_manager.get_variable_from_address(40000) == "temp"


def test_get_variable_size_from_scope():
    assert memory_manager.get_variable_size_for_scope() == (1, 1, 1)
