"""
oracle.py - Serves as the only authority for semantics in the Mogavity language
Created on: 25/04/22 by Jaime Hisao Yesaki Hinojosa
1 y 2
Int = 0
Float = 1
Char = 2
Bool = 4

3
Sum = 0
Subtract = 1
Multiply = 2
Divide = 3
Greater Than = 4
Less Than = 5
Not Equal = 6
AND = 7
OR = 8

Results 
-1 = Error
"""
import sys
from error_handling import error, info

n = 9  # Probolema con ineficiencia de espacio utilizado
semantic_oracle = distance = [[[0 for k in range(9)] for j in range(3)] for i in range(3)]
semantic_oracle[0][0][0] = 0  # Int y Int (Sum)
semantic_oracle[0][0][1] = 0  # Int y Int (Subtract)
semantic_oracle[0][0][2] = 0  # Int y Int (Multiply)
semantic_oracle[0][0][3] = 0  # Int y Int (Divide)
semantic_oracle[0][0][4] = 4  # Int y Int (Greater Than)
semantic_oracle[0][0][5] = 4  # Int y Int (Less Than)
semantic_oracle[0][0][6] = 4  # Int y Int (Not Equal)
semantic_oracle[0][0][7] = -1  # Int y Int (AND)
semantic_oracle[0][0][8] = -1  # Int y Int (OR)
semantic_oracle[1][1][0] = 1  # Float y Float (Sum)
semantic_oracle[1][1][1] = 1  # Float y Float (Subtract)
semantic_oracle[1][1][2] = 1  # Float y Float (Multiply)
semantic_oracle[1][1][3] = 1  # Float y Float (Divide)
semantic_oracle[1][1][4] = 4  # Float y Float (Greater Than)
semantic_oracle[1][1][5] = 4  # Float y Float (Less Than)
semantic_oracle[1][1][6] = 4  # Float y Float (Not Equal)
semantic_oracle[1][1][7] = -1  # Float y Float (AND)
semantic_oracle[1][1][8] = -1  # Float y Float (OR)
semantic_oracle[0][1][0] = 0  # Int y Float (Sum)
semantic_oracle[0][1][1] = 0  # Int y Float (Subtract)
semantic_oracle[0][1][2] = 1  # Int y Float (Multiply)
semantic_oracle[0][1][3] = 0  # Int y Float (Divide)
semantic_oracle[0][1][4] = 4  # Int y Float (Greater Than)
semantic_oracle[0][1][5] = 4  # Int y Float (Less Than)
semantic_oracle[0][1][6] = 4  # Int y Float (Not Equal)
semantic_oracle[0][1][7] = -1  # Int y Float (AND)
semantic_oracle[0][1][8] = -1  # Int y Float (OR)
semantic_oracle[1][0][0] = 0  # Float y Int (Sum)
semantic_oracle[1][0][1] = 0  # Float y Int (Subtract)
semantic_oracle[1][0][2] = 1  # Float y Int (Multiply)
semantic_oracle[1][0][3] = 0  # Float y Int (Divide)
semantic_oracle[1][0][4] = 4  # Float y Int (Greater Than)
semantic_oracle[1][0][5] = 4  # Float y Int (Less Than)
semantic_oracle[1][0][6] = 4  # Float y Int (Not Equal)
semantic_oracle[1][0][7] = -1  # Float y Int (AND)
semantic_oracle[1][0][8] = -1  # Float y Int (OR)
semantic_oracle[2][2][0] = -1  # Char y Char (Sum)
semantic_oracle[2][2][1] = -1  # Char y Char (Subtract)
semantic_oracle[2][2][2] = -1  # Char y Char (Multiply)
semantic_oracle[2][2][3] = -1  # Char y Char (Divide)
semantic_oracle[2][2][4] = -1  # Char y Char (Greater Than)
semantic_oracle[2][2][5] = -1  # Char y Char (Less Than)
semantic_oracle[2][2][6] = 4  # Char y Char (Not Equal)
semantic_oracle[2][2][7] = -1  # Char y Char (AND)
semantic_oracle[2][2][8] = -1  # Char y Char (OR)
semantic_oracle[2][0][0] = -1  # Char y Int (Sum)
semantic_oracle[2][0][1] = -1  # Char y Int (Subtract)
semantic_oracle[2][0][2] = -1  # Char y Int (Multiply)
semantic_oracle[2][0][3] = -1  # Char y Int (Divide)
semantic_oracle[2][0][4] = -1  # Char y Int (Greater Than)
semantic_oracle[2][0][5] = -1  # Char y Int (Less Than)
semantic_oracle[2][0][6] = -1  # Char y Int (Not Equal)
semantic_oracle[2][0][7] = -1  # Char y Int (AND)
semantic_oracle[2][0][8] = -1  # Char y Int (OR)
semantic_oracle[2][1][0] = -1  # Char y Float (Sum)
semantic_oracle[2][1][1] = -1  # Char y Float (Subtract)
semantic_oracle[2][1][2] = -1  # Char y Float (Multiply)
semantic_oracle[2][1][3] = -1  # Char y Float (Divide)
semantic_oracle[2][1][4] = -1  # Char y Float (Greater Than)
semantic_oracle[2][1][5] = -1  # Char y Float (Less Than)
semantic_oracle[2][1][6] = -1  # Char y Float (Not Equal)
semantic_oracle[2][2][7] = -1  # Char y Float (AND)
semantic_oracle[2][1][8] = -1  # Char y Float (OR)
semantic_oracle[0][2][0] = -1  # Int y Char (Sum)
semantic_oracle[0][2][1] = -1  # Int y Char (Subtract)
semantic_oracle[0][2][2] = -1  # Int y Char (Multiply)
semantic_oracle[0][2][3] = -1  # Int y Char (Divide)
semantic_oracle[0][2][4] = -1  # Int y Char (Greater Than)
semantic_oracle[0][2][5] = -1  # Int y Char (Less Than)
semantic_oracle[0][2][6] = -1  # Int y Char (Not Equal)
semantic_oracle[0][2][7] = -1  # Int y Char (AND)
semantic_oracle[0][2][8] = -1  # Int y Char (OR)
semantic_oracle[1][2][0] = -1  # Float y Char (Sum)
semantic_oracle[1][2][1] = -1  # Float y Char (Subtract)
semantic_oracle[1][2][2] = -1  # Float y Char (Multiply)
semantic_oracle[1][2][3] = -1  # Float y Char (Divide)
semantic_oracle[1][2][4] = -1  # Float y Char (Greater Than)
semantic_oracle[1][2][5] = -1  # Float y Char (Less Than)
semantic_oracle[1][2][6] = -1  # Float y Char (Not Equal)
semantic_oracle[1][2][7] = -1  # Float y Char (AND)
semantic_oracle[1][1][8] = -1  # Float y Char (OR)


# TODO: functions to check semantics with oracle


def convert_string_name_to_number_type(name):
    """
    If you need the Oracle type equivalent for a type, eg. Int, Float. You can use this
    function to obtain the int "pointer" to the oracle table. Eg. Int = 0
    :param name: the type in string you wish to convert.
    :return: the given type converted to Integer.
    """
    if name is not None:
        if name == "int":
            return 0
        elif name == "float":
            return 1
        elif name == "char":
            return 2


def convert_string_name_to_number_operand(name):
    """
    If you need the Oracle operand equivalent for an operand, eg. +, -. You can use this
    function to obtain the int "pointer" to the oracle table. Eg. + = 0
    :param name: the operand in string you wish to convert. (symbol)
    :return: the given operand converted to Integer.
    """
    if name is not None:
        if name == "+":
            return 0
        elif name == "-":
            return 1
        elif name == "*":
            return 2
        elif name == "/":
            return 3
        elif name == ">":
            return 4
        elif name == "<":
            return 5
        elif name == "!=":
            return 6
        elif name == "AND":
            return 7
        elif name == "OR":
            return 8
        else:
            error("Operator" + name + " not supported.")


def convert_number_type_to_string_name(num):
    if num is not None:
        if num == 0:
            return "int"
        elif num == 1:
            return "float"
        elif num == 2:
            return "char"
        elif num == 4:
            return "bool"
        else:
            error("Resulting type " + str(num) + " not supported!")


def use_oracle(left_type, right_type, operand):
    return convert_number_type_to_string_name(semantic_oracle[convert_string_name_to_number_type(left_type)][convert_string_name_to_number_type(right_type)][
            convert_string_name_to_number_operand(operand)])

