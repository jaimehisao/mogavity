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
