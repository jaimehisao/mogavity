"""
Lexer for the Mogavity Programming Language
Created by Clarissa V, and Hisao Y
March 2022
Usage for the Compiler´s Design Course
"""
import ply.yacc as yacc
import ply.lex as lex

tokens = [
    "ID",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LESSTHAN",
    "GREATERTHAN",
    "EQUALS",
    "NOTEQUAL",
    "ASSIGNMENT",
    "EQUALGREATERTHAN",
    "EQUALLESSTHAN",
    "MINUSEQUAL",
    "PLUSEQUAL",
    "TIMESEQUAL",
    "DIVIDEEQUAL",
    "LEFTARROW",
    "RIGHTARROW",
    "LEFTPARENTHESIS",
    "RIGHTPARENTHESIS",
    "LEFTCURLYBRACKET",
    "RIGHTCURLYBRACKET",
    "CTE_STRING",
    "CTE_FLOAT",
    "CTE_INT",
    "CTE_CHAR",
    "DOT",
    "SEMICOLON",
    "COLON",
]

# Reserved Keywords
reserved = {
    "program": "PROGRAM",
    "class": "CLASS",
    "instr": "INSTR",
    "int": "INT",
    "float": "FLOAT",
    "char": "CHAR",
    "void": "VOID",
    "output": "OUTPUT",
    "input": "INPUT",
    "or": "OR",
    "and": "AND",
    "if": "IF",
    "elif": "ELIF",
    "for": "FOR",
    "while": "WHILE",
    "main": "MAIN",
    "inherits": "INHERITS",
    "attr": "ATTR",
    "methods": "METHODS",
    "var": "VAR",
    "otherwise": "OTHERWISE"
}

tokens = tokens + list(reserved.values())

def t_ID(t):
    r"[a-zA-Z]+(_?[a-zA-Z0-9]+)*"
    t.type = reserved.get(t.value, "ID")
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



"""PARSER"""

# GRAMMARS

# <PROGRAMA>
def p_programa(p):
    """programa : PROGRAM ID SEMICOLON class vars instr bloque
    | PROGRAM ID SEMICOLON vars instr bloque
    | PROGRAM ID SEMICOLON instr bloque
    | PROGRAM ID SEMICOLON bloque
    """

# <CLASS>
def p_class(p):
    """
    class: CLASS ID INHERITS ID LEFTCURLYBRACKET ATTR COLON vars constructor colon constructor method colon INSTR RIGHTCURLYBRACKET
    | CLASS ID INHERITS ID LEFTCURLYBRACKET ATTR COLON vars constructor colon constructor method colon INSTR RIGHTCURLYBRACKET
    | CLASS ID LEFTCURLYBRACKET ATTR COLON vars constructor colon constructor method colon INSTR RIGHTCURLYBRACKET
    | CLASS ID LEFTCURLYBRACKET ATTR COLON vars method colon INSTR RIGHTCURLYBRACKET
    | CLASS ID LEFTCURLYBRACKET ATTR COLON vars constructor colon constructor RIGHTCURLYBRACKET
    | CLASS ID INHERITS ID LEFTCURLYBRACKET ATTR COLON vars constructor colon constructor method colon INSTR RIGHTCURLYBRACKET


    programa : PROGRAM ID SEMICOLON class vars instr bloque
    | PROGRAM ID SEMICOLON vars instr bloque
    | PROGRAM ID SEMICOLON instr bloque
    | PROGRAM ID SEMICOLON bloque
    """

# <CONSTRUCTOR>
def p_constructor(p):
    """constructor : ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | ID LEFTPARENTHESIS RIGHTPARENTHESIS bloque
    """


    """VARS"""


# <TipoCompuesto>
def p_tipoCompuesto(p):
    """tipoCompuesto : ID
    """

# <Tiposimple>
def p_tipoSimple(p):
    """tipoSimple : int
    | float
    | char
    """

# <Instr>
def p_tipoSimple(p):
    """instr : instr void ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | instr tipoSimple ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    """

# <Params>
def p_params(p):
    """params : tipoSimple ID
    | tipoSimple ID COMMA params1
    |
    """

# <Params1>
def p_params1(p):
    """params1 : tipoSimple ID ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | instr tipoSimple ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | empty
    """

    """PARAMS2"""

# <Bloque>
def p_bloque(p): #TODO falta el caso de muchos estatutos
    """bloque : LEFTCURLYBRACE estatuto RIGHTCURLYBRACE
    | LEFTCURLYBRACE RIGHTCURLYBRACE
    """

# <Estatuto>
def p_estatuto(p):
    """estatuto :
    """


def p_error(p):
    """
    If there is an error, the parser will resort to this instruction to inform of it.
    :param p:
    :return:
    """
    if p == None:
        token = "end of file"
    else:
        token = f"({p.value}) on line {p.lineno}"

    print(f"Syntax error: {token}")
    exit()

lexer = lex.lex()
parser = yacc.yacc()


def parse(r):
    parser.parse(r)
