import oracle
import unittest



def test_int_int_sum():
    """En el caso de la suma (0) entre un int (0) y un int (0)
        la suma debe resultar en un int (0)"""
    assert oracle.semantic_oracle[0][0][0] == 0


def test_int_float_sum():
    """En el caso de la suma (0) entre un int (0) y un float (1)
    la suma debe resultar en un int (0)"""
    assert oracle.semantic_oracle[0][1][0] == 0


def test_char_char_sum():
    """En el caso de la suma (0) entre un char (2) y un char (2)
    la suma debe resultar en un error (-1)"""
    assert oracle.semantic_oracle[2][2][0] == -1


def test_int_char_multiplication():
    """En el caso de la mutliplicacion (2) entre un int (0) y un char (2)
    la suma debe resultar en un error (-1)"""
    assert oracle.semantic_oracle[0][2][4] == -1


def test_string_operand_conversion():
    """Tests that we can convert operand strings into known Integers for use in our semantic cube."""
    assert oracle.convert_string_name_to_number_operand("+") == 0
    assert oracle.convert_string_name_to_number_operand("-") == 1
    assert oracle.convert_string_name_to_number_operand("*") == 2
    assert oracle.convert_string_name_to_number_operand("/") == 3
    assert oracle.convert_string_name_to_number_operand(">") == 4
    assert oracle.convert_string_name_to_number_operand("<") == 5
    assert oracle.convert_string_name_to_number_operand("!=") == 6
    assert oracle.convert_string_name_to_number_operand("AND") == 7
    assert oracle.convert_string_name_to_number_operand("OR") == 8


def test_string_type_conversion():
    """Tests that we can convert types into known Integers for use in our semantic cube."""
    assert oracle.convert_string_name_to_number_type("int") == 0
    assert oracle.convert_string_name_to_number_type("float") == 1
    assert oracle.convert_string_name_to_number_type("char") == 2

