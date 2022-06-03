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
ASSIGN = 9
Equal = 10

Results 
-1 = Error
"""
import sys
from error_handling import error, info

n = 9  # Probolema con ineficiencia de espacio utilizado
semantic_oracle = distance = [[[0 for k in range(11)] for j in range(5)] for i in range(5)]
semantic_oracle[0][0][0] = 0    # Int y Int (Sum)
semantic_oracle[0][0][1] = 0    # Int y Int (Subtract)
semantic_oracle[0][0][2] = 0    # Int y Int (Multiply)
semantic_oracle[0][0][3] = 0    # Int y Int (Divide)
semantic_oracle[0][0][4] = 4    # Int y Int (Greater Than)
semantic_oracle[0][0][5] = 4    # Int y Int (Less Than)
semantic_oracle[0][0][6] = 4    # Int y Int (Not Equal)
semantic_oracle[0][0][7] = -1   # Int y Int (AND)
semantic_oracle[0][0][8] = -1   # Int y Int (OR)
semantic_oracle[0][0][9] = 0    # Int y Int (ASSIGN)
semantic_oracle[0][0][10] = 4   # Int y Int (EQUAL)
semantic_oracle[1][1][0] = 1    # Float y Float (Sum)
semantic_oracle[1][1][1] = 1    # Float y Float (Subtract)
semantic_oracle[1][1][2] = 1    # Float y Float (Multiply)
semantic_oracle[1][1][3] = 1    # Float y Float (Divide)
semantic_oracle[1][1][4] = 4    # Float y Float (Greater Than)
semantic_oracle[1][1][5] = 4    # Float y Float (Less Than)
semantic_oracle[1][1][6] = 4    # Float y Float (Not Equal)
semantic_oracle[1][1][7] = -1   # Float y Float (AND)
semantic_oracle[1][1][8] = -1   # Float y Float (OR)
semantic_oracle[1][1][9] = 1    # Float y Float (ASSIGN)
semantic_oracle[1][1][10] = 4   # Float y Float (EQUAL)
semantic_oracle[0][1][0] = 0    # Int y Float (Sum)
semantic_oracle[0][1][1] = 0    # Int y Float (Subtract)
semantic_oracle[0][1][2] = 1    # Int y Float (Multiply)
semantic_oracle[0][1][3] = 0    # Int y Float (Divide)
semantic_oracle[0][1][4] = 4    # Int y Float (Greater Than)
semantic_oracle[0][1][5] = 4    # Int y Float (Less Than)
semantic_oracle[0][1][6] = 4    # Int y Float (Not Equal)
semantic_oracle[0][1][7] = -1   # Int y Float (AND)
semantic_oracle[0][1][8] = -1   # Int y Float (OR)
semantic_oracle[0][1][9] = -1   # Int y Float (ASSIGN)
semantic_oracle[0][1][10] = 4   # Int y Float (EQUAL)
semantic_oracle[1][0][0] = 0    # Float y Int (Sum)
semantic_oracle[1][0][1] = 0    # Float y Int (Subtract)
semantic_oracle[1][0][2] = 1    # Float y Int (Multiply)
semantic_oracle[1][0][3] = 0    # Float y Int (Divide)
semantic_oracle[1][0][4] = 4    # Float y Int (Greater Than)
semantic_oracle[1][0][5] = 4    # Float y Int (Less Than)
semantic_oracle[1][0][6] = 4    # Float y Int (Not Equal)
semantic_oracle[1][0][7] = -1   # Float y Int (AND)
semantic_oracle[1][0][8] = -1   # Float y Int (OR)
semantic_oracle[1][0][9] = -1   # Float y Int (ASSIGN)
semantic_oracle[1][0][10] = 4   # Float y Int (EQUAL)
semantic_oracle[2][2][0] = -1   # Char y Char (Sum)
semantic_oracle[2][2][1] = -1   # Char y Char (Subtract)
semantic_oracle[2][2][2] = -1   # Char y Char (Multiply)
semantic_oracle[2][2][3] = -1   # Char y Char (Divide)
semantic_oracle[2][2][4] = -1   # Char y Char (Greater Than)
semantic_oracle[2][2][5] = -1   # Char y Char (Less Than)
semantic_oracle[2][2][6] = 4    # Char y Char (Not Equal)
semantic_oracle[2][2][7] = -1   # Char y Char (AND)
semantic_oracle[2][2][8] = -1   # Char y Char (OR)
semantic_oracle[2][2][9] = 2    # Char y Char (ASSIGN)
semantic_oracle[2][2][10] = 4   # Char y Char (EQUAL)
semantic_oracle[2][0][0] = -1   # Char y Int (Sum)
semantic_oracle[2][0][1] = -1   # Char y Int (Subtract)
semantic_oracle[2][0][2] = -1   # Char y Int (Multiply)
semantic_oracle[2][0][3] = -1   # Char y Int (Divide)
semantic_oracle[2][0][4] = -1   # Char y Int (Greater Than)
semantic_oracle[2][0][5] = -1   # Char y Int (Less Than)
semantic_oracle[2][0][6] = -1   # Char y Int (Not Equal)
semantic_oracle[2][0][7] = -1   # Char y Int (AND)
semantic_oracle[2][0][8] = -1   # Char y Int (OR)
semantic_oracle[2][0][9] = -1   # Char y Int (ASSIGN)
semantic_oracle[2][0][10] = -1  # Char y Int (EQUAL)
semantic_oracle[2][1][0] = -1   # Char y Float (Sum)
semantic_oracle[2][1][1] = -1   # Char y Float (Subtract)
semantic_oracle[2][1][2] = -1   # Char y Float (Multiply)
semantic_oracle[2][1][3] = -1   # Char y Float (Divide)
semantic_oracle[2][1][4] = -1   # Char y Float (Greater Than)
semantic_oracle[2][1][5] = -1   # Char y Float (Less Than)
semantic_oracle[2][1][6] = -1   # Char y Float (Not Equal)
semantic_oracle[2][2][7] = -1   # Char y Float (AND)
semantic_oracle[2][1][8] = -1   # Char y Float (OR)
semantic_oracle[2][1][9] = -1   # Char y Float (ASSIGN)
semantic_oracle[2][1][10] = -1  # Char y Float (EQUAL)
semantic_oracle[0][2][0] = -1   # Int y Char (Sum)
semantic_oracle[0][2][1] = -1   # Int y Char (Subtract)
semantic_oracle[0][2][2] = -1   # Int y Char (Multiply)
semantic_oracle[0][2][3] = -1   # Int y Char (Divide)
semantic_oracle[0][2][4] = -1   # Int y Char (Greater Than)
semantic_oracle[0][2][5] = -1   # Int y Char (Less Than)
semantic_oracle[0][2][6] = -1   # Int y Char (Not Equal)
semantic_oracle[0][2][7] = -1   # Int y Char (AND)
semantic_oracle[0][2][8] = -1   # Int y Char (OR)
semantic_oracle[0][2][9] = -1   # Int y Char (ASSIGN)
semantic_oracle[0][2][10] = -1  # Int y Char (EQUAL)
semantic_oracle[1][2][0] = -1   # Float y Char (Sum)
semantic_oracle[1][2][1] = -1   # Float y Char (Subtract)
semantic_oracle[1][2][2] = -1   # Float y Char (Multiply)
semantic_oracle[1][2][3] = -1   # Float y Char (Divide)
semantic_oracle[1][2][4] = -1   # Float y Char (Greater Than)
semantic_oracle[1][2][5] = -1   # Float y Char (Less Than)
semantic_oracle[1][2][6] = -1   # Float y Char (Not Equal)
semantic_oracle[1][2][7] = -1   # Float y Char (AND)
semantic_oracle[1][1][8] = -1   # Float y Char (OR)
semantic_oracle[1][1][9] = -1   # Float y Char (ASSIGN)
semantic_oracle[1][2][10] = -1  # Float y Char (EQUAL)
semantic_oracle[4][4][0] = -1   # Bool y Bool (Sum)
semantic_oracle[4][4][1] = -1   # Bool y Bool (Subtract)
semantic_oracle[4][4][2] = -1   # Bool y Bool (Multiply)
semantic_oracle[4][4][3] = -1   # Bool y Bool (Divide)
semantic_oracle[4][4][4] = -1   # Bool y Bool (Greater Than)
semantic_oracle[4][4][5] = -1   # Bool y Bool (Less Than)
semantic_oracle[4][4][6] = -1   # Bool y Bool (Not Equal)
semantic_oracle[4][4][7] = 4    # Bool y Bool (AND)
semantic_oracle[4][4][8] = 4    # Bool y Bool (OR)
semantic_oracle[4][4][9] = -1   # Bool y Bool (ASSIGN)
semantic_oracle[4][4][10] = -1  # Bool y Bool (EQUAL)
semantic_oracle[4][0][0] = -1   # Bool y Int (Sum)
semantic_oracle[4][0][1] = -1   # Bool y Int (Subtract)
semantic_oracle[4][0][2] = -1   # Bool y Int (Multiply)
semantic_oracle[4][0][3] = -1   # Bool y Int (Divide)
semantic_oracle[4][0][4] = -1   # Bool y Int (Greater Than)
semantic_oracle[4][0][5] = -1   # Bool y Int (Less Than)
semantic_oracle[4][0][6] = -1   # Bool y Int (Not Equal)
semantic_oracle[4][0][7] = -1   # Bool y Int (AND)
semantic_oracle[4][0][8] = -1   # Bool y Int (OR)
semantic_oracle[4][0][9] = -1   # Bool y Int (ASSIGN)
semantic_oracle[4][0][10] = -1  # Bool y Int (EQUAL)
semantic_oracle[4][1][0] = -1   # Bool y Float (Sum)
semantic_oracle[4][1][1] = -1   # Bool y Float (Subtract)
semantic_oracle[4][1][2] = -1   # Bool y Float (Multiply)
semantic_oracle[4][1][3] = -1   # Bool y Float (Divide)
semantic_oracle[4][1][4] = -1   # Bool y Float (Greater Than)
semantic_oracle[4][1][5] = -1   # Bool y Float (Less Than)
semantic_oracle[4][1][6] = -1   # Bool y Float (Not Equal)
semantic_oracle[4][1][7] = .1   # Bool y Float (AND)
semantic_oracle[4][1][8] = -1   # Bool y Float (OR)
semantic_oracle[4][1][9] = -1   # Bool y Float (ASSIGN)
semantic_oracle[4][1][10] = -1  # Bool y Float (EQUAL)
semantic_oracle[4][2][0] = -1   # Bool y Char (Sum)
semantic_oracle[4][2][1] = -1   # Bool y Char (Subtract)
semantic_oracle[4][2][2] = -1   # Bool y Char (Multiply)
semantic_oracle[4][2][3] = -1   # Bool y Char (Divide)
semantic_oracle[4][2][4] = -1   # Bool y Char (Greater Than)
semantic_oracle[4][2][5] = -1   # Bool y Char (Less Than)
semantic_oracle[4][2][6] = -1   # Bool y Char (Not Equal)
semantic_oracle[4][2][7] = -1   # Bool y Char (AND)
semantic_oracle[4][2][8] = -1   # Bool y Char (OR)
semantic_oracle[4][2][9] = -1   # Bool y Char (ASSIGN)
semantic_oracle[4][2][10] = -1  # Bool y Char (EQUAL)
semantic_oracle[0][4][0] = -1   # Int y Bool (Sum)
semantic_oracle[0][4][1] = -1   # Int y Bool (Subtract)
semantic_oracle[0][4][2] = -1   # Int y Bool (Multiply)
semantic_oracle[0][4][3] = -1   # Int y Bool (Divide)
semantic_oracle[0][4][4] = -1   # Int y Bool (Greater Than)
semantic_oracle[0][4][5] = -1   # Int y Bool (Less Than)
semantic_oracle[0][4][6] = -1   # Int y Bool (Not Equal)
semantic_oracle[0][4][7] = -1   # Int y Bool (AND)
semantic_oracle[0][4][8] = -1   # Int y Bool (OR)
semantic_oracle[0][4][9] = -1   # Int y Bool (ASSIGN)
semantic_oracle[0][4][10] = -1  # Int y Bool (EQUAL)
semantic_oracle[1][4][0] = -1   # Float y Bool (Sum)
semantic_oracle[1][4][1] = -1   # Float y Bool (Subtract)
semantic_oracle[1][4][2] = -1   # Float y Bool (Multiply)
semantic_oracle[1][4][3] = -1   # Float y Bool (Divide)
semantic_oracle[1][4][4] = -1   # Float y Bool (Greater Than)
semantic_oracle[1][4][5] = -1   # Float y Bool (Less Than)
semantic_oracle[1][4][6] = -1   # Float y Bool (Not Equal)
semantic_oracle[1][4][7] = -1   # Float y Bool (AND)
semantic_oracle[1][4][8] = -1   # Float y Bool (OR)
semantic_oracle[1][4][9] = -1   # Float y Bool (ASSIGN)
semantic_oracle[1][4][10] = -1  # Float y Bool (EQUAL)
semantic_oracle[2][4][0] = -1   # Char y Bool (Sum)
semantic_oracle[2][4][1] = -1   # Char y Bool (Subtract)
semantic_oracle[2][4][2] = -1   # Char y Bool (Multiply)
semantic_oracle[2][4][3] = -1   # Char y Bool (Divide)
semantic_oracle[2][4][4] = -1   # Char y Bool (Greater Than)
semantic_oracle[2][4][5] = -1   # Char y Bool (Less Than)
semantic_oracle[2][4][6] = -1   # Char y Bool (Not Equal)
semantic_oracle[2][4][7] = -1   # Char y Bool (AND)
semantic_oracle[2][4][8] = -1   # Char y Bool (OR)
semantic_oracle[2][4][9] = -1   # Char y Bool (ASSIGN)
semantic_oracle[2][4][10] = -1  # Char y Bool (EQUAL)




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
        elif name == "bool":
            return 4


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
        elif name == "and":
            return 7
        elif name == "or":
            return 8
        elif name == "=":
            return 9
        elif name == "==":
            return 10
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

