"""
Lexer for the Mogavity Programming Language
Created by Clarissa V, and Hisao Y
March 2022
Usage for the Compiler´s Design Course
"""
import ply.yacc as yacc
import ply.lex as lex
import sys, logging
from function_directory import FunctionDirectory

# class_table = class_directory.ClassTable()
func_table = FunctionDirectory()

global current_scope
current_scope = 'global'

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
    "LEFTBRACKET",
    "RIGHTBRACKET",
    "CTE_STRING",
    "CTE_FLOAT",
    "CTE_INT",
    "CTE_CHAR",
    "DOT",
    "SEMICOLON",
    "COLON",
    "COMMA",
]
# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_EQUALS = r'=='
t_NOTEQUAL = r'!='
t_ASSIGNMENT = r'\='
t_EQUALGREATERTHAN = r'>='
t_EQUALLESSTHAN = r'<='
t_MINUSEQUAL = r'-='
t_PLUSEQUAL = r'\+='
t_TIMESEQUAL = r'\*='
t_DIVIDEEQUAL = r'/='
t_LEFTARROW = r'<-'
t_RIGHTARROW = r'->'
t_LEFTPARENTHESIS = r'\('
t_RIGHTPARENTHESIS = r'\)'
t_LEFTCURLYBRACKET = r'\{'
t_RIGHTCURLYBRACKET = r'\}'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_CTE_STRING = r'"([^\\"\n]+|\\.)*"'
t_CTE_FLOAT = r'[+-]?[0-9]+\.[0-9]+([Ee][+-]?[0-9]*)?'
t_CTE_INT = r'[0-9]+'
t_CTE_CHAR = r'[a-zA-Z0-9]'
t_DOT = r'\.'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','

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
    "return": "RETURN",
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


# GRAMMARS
lexer = lex.lex()


# <PROGRAMA>
def p_programa(p):
    """programa : PROGRAM new_program ID save_program SEMICOLON class vars instr MAIN bloque
    | PROGRAM new_program ID save_program SEMICOLON class instr MAIN bloque
    | PROGRAM new_program ID save_program SEMICOLON vars instr MAIN bloque
    | PROGRAM new_program ID save_program SEMICOLON vars MAIN bloque
    | PROGRAM new_program ID save_program SEMICOLON instr MAIN bloque
    | PROGRAM new_program ID save_program SEMICOLON MAIN bloque
    """


# epsilon
def p_empty(p):
    '''empty :'''
    pass


# <CLASS>
def p_class(p):
    """class : CLASS ID INHERITS ID LEFTCURLYBRACKET ATTR COLON vars constructor COLON constructor METHODS COLON instr RIGHTCURLYBRACKET
    | CLASS ID LEFTCURLYBRACKET ATTR COLON vars constructor COLON constructor METHODS COLON instr RIGHTCURLYBRACKET
    | CLASS ID LEFTCURLYBRACKET ATTR COLON vars METHODS COLON instr RIGHTCURLYBRACKET
    | CLASS ID LEFTCURLYBRACKET ATTR COLON vars constructor COLON constructor RIGHTCURLYBRACKET
    """


# <CONSTRUCTOR>
def p_constructor(p):
    """constructor : ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | ID LEFTPARENTHESIS RIGHTPARENTHESIS bloque
    """


# <VARS>
def p_vars(p):
    """vars :   VAR tipoCompuesto new_variable_set_type ID new_variable vars2 SEMICOLON vars4
            |   VAR tipoSimple new_variable_set_type ID new_variable vars3 SEMICOLON vars4"""


def p_vars2(p):
    '''vars2 :  COMMA ID new_variable vars2
             |  empty'''


def p_vars3(p):
    '''vars3 :  LEFTBRACKET CTE_INT RIGHTBRACKET vars3
             |  COMMA ID new_variable vars3
             |  empty'''


def p_vars4(p):
    '''vars4 :  tipoCompuesto ID new_variable vars2 SEMICOLON vars4
             |  tipoSimple ID new_variable vars3 SEMICOLON vars4
             |  empty'''


# <TipoCompuesto>
def p_tipoCompuesto(p):
    """tipoCompuesto : ID new_variable_set_type
    """


# <Tiposimple>
def p_tipoSimple(p):
    """tipoSimple : INT new_variable_set_type
    | FLOAT new_variable_set_type
    | CHAR new_variable_set_type
    """

# TODO: Actualizar el diagrama instr
# <Instr>
def p_instr(p):
    """instr : INSTR VOID ID new_function LEFTPARENTHESIS params RIGHTPARENTHESIS instr2 bloque
    | INSTR tipoSimple ID new_function LEFTPARENTHESIS params RIGHTPARENTHESIS instr2 bloque
    """
    global current_scope
    current_scope = p[3]

def p_instr2(p):
    """instr2 : vars
              | empty"""

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
def p_bloque(p):
    """bloque : LEFTCURLYBRACKET bloque2 RIGHTCURLYBRACKET"""


def p_bloque2(p):
    '''bloque2  :   estatuto bloque2
                |   empty'''


# <Estatuto>
def p_estatuto(p):
    """estatuto :   asignacion
                |   condicion
                |   escritura
                |   lectura
                |   llamada
                |   cicloW
                |   cicloFor
                |   return
    """


# <Asignación>
def p_asignacion(p):
    '''asignacion   :   variable ASSIGNMENT exp SEMICOLON'''


# <Variable>
def p_variable(p):
    '''variable :   ID
                |   ID DOT ID
                |   ID LEFTBRACKET exp RIGHTBRACKET
                |   ID LEFTBRACKET exp RIGHTBRACKET LEFTBRACKET exp RIGHTBRACKET'''


# <Condicion>
def p_condicion(p):
    '''condicion    :   IF LEFTPARENTHESIS exp RIGHTPARENTHESIS bloque
                    |   IF LEFTPARENTHESIS exp RIGHTPARENTHESIS bloque condicion2'''


def p_condicion2(p):
    '''condicion2   :   OTHERWISE bloque
                    |   ELIF LEFTPARENTHESIS exp RIGHTPARENTHESIS bloque condicion2'''


# <Escritura>
def p_escritura(p):
    '''escritura    :   OUTPUT RIGHTARROW exp escritura2 SEMICOLON
                    |   OUTPUT RIGHTARROW CTE_STRING escritura2 SEMICOLON'''


def p_escritura2(p):
    '''escritura2   :   COMMA exp escritura2
                    |   COMMA CTE_STRING escritura2
                    |   empty'''


# <Lectura>
def p_lectura(p):
    '''lectura  :   INPUT LEFTARROW variable SEMICOLON'''


# <Llamada>
def p_llamada(p):
    '''llamada  :   ID LEFTPARENTHESIS llamada2 RIGHTPARENTHESIS SEMICOLON'''


def p_llamada2(p):
    '''llamada2 :   exp llamada2
                |   COMMA exp llamada2
                |   empty'''


# <CicloW>
def p_cicloW(p):
    '''cicloW   :   WHILE LEFTPARENTHESIS exp RIGHTPARENTHESIS bloque'''


# <CicloFor>
def p_cicloFor(p):
    '''cicloFor :   FOR LEFTPARENTHESIS assign SEMICOLON exp SEMICOLON update RIGHTPARENTHESIS bloque'''


# <Assign>
def p_assign(p):
    '''assign   :   ID ASSIGNMENT CTE_INT'''


# <Update>
def p_update(p):
    '''update   :   ID PLUSEQUAL CTE_INT
                |   ID MINUSEQUAL CTE_INT
                |   ID TIMESEQUAL CTE_INT
                |   ID DIVIDEEQUAL CTE_INT'''


# <Return>
def p_return(p):
    '''return   :   RETURN exp SEMICOLON'''


# <Exp>
def p_exp(p):
    '''exp  :   expA expOR'''


def p_expOR(p):
    '''expOR    :   OR expA expOR
                |   empty'''


# <ExpA>
def p_expA(p):
    '''expA :   expB expAND'''


def p_expAND(p):
    '''expAND   :   AND expB expAND
                |   empty'''


# <ExpB>
def p_expB(p):
    '''expB :   expC expLOOP'''


def p_expLOOP(p):
    '''expLOOP  :   LESSTHAN expB
                |   GREATERTHAN expB
                |   EQUALLESSTHAN expB
                |   EQUALGREATERTHAN expB
                |   EQUALS expB
                |   NOTEQUAL expB
                |   empty'''


# <ExpC>
def p_expC(p):
    '''expC :   termino expPM'''


def p_expPM(p):
    '''expPM    :   PLUS expC
                |   MINUS expC
                |   empty'''


# <Termino>
def p_termino(p):
    '''termino  :   factor expMD'''


def p_expMD(p):
    '''expMD    :   TIMES termino
                |   DIVIDE termino
                |   empty'''


# <Factor>
def p_factor(p):
    '''factor   :   LEFTPARENTHESIS exp RIGHTPARENTHESIS
                |   CTE_INT
                |   CTE_FLOAT
                |   CTE_CHAR
                |   variable
                |   llamada'''


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


########################################################
################ PUNTOS NEURALGICOS ####################
########################################################

def p_new_program(p):
    'new_program : '
    global func_table


def p_save_program(p):
    'save_program :'
    print()
    #func_table.add_elements(p[-1], "program")


# Agregar Variable en Tabla
def p_new_variable(p):
    'new_variable : '
    func_table.add_variable(p[-1], current_scope, func_table.tmp_type)


def p_new_variable_set_type(p):
    'new_variable_set_type : '
    global tmp_type
    tmp_type = p[-1]
    # TODO we have a situation here pending to resolve
    """As the variable type comes BEFORE the name, we have no way of knowing if we will actually
     need it when the ID comes, so we store it temporarily for future use and just overwrite it when the time comes."""


def p_new_function(p):
    'new_function :'
    func_table.add_function(p[-1], tmp_type)


"""
def p_new_constructor(p):
    'new_constructor :'

def p_new_array(p):
    'new_array : '

def p_new_function(p):
    'new_function : '

def p_new_param_get_type(p):
    'new_param_get_type : '
"""


def error(message: str):
    print(message)  # use raise?
    sys.exit()


# Verificar el tipo de la variable


parser = yacc.yacc()
r = None
try:
    f = open("test.txt", 'r')
    r = f.read()
    f.close()
except FileNotFoundError:
    print("No hay archivo para probar")

parser.parse(r)
#parser.parse(r, debug=1)
print("Código Aceptado")
print(func_table.function_table)
