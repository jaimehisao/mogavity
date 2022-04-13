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
t_PLUS          =   r'\+' 
t_MINUS         =   r'-'
t_TIMES         =   r'\*'
t_DIVIDE        =   r'/'
t_LESSTHAN      =   r'<'
t_GREATERTHAN   =   r'>'
t_EQUALS        =   r'=='
t_NOTEQUAL      =   r'!='
t_ASSIGNMENT    =   r'\='
t_EQUALGREATERTHAN  =   r'>='
t_EQUALLESSTHAN     =   r'<='
t_MINUSEQUAL        =   r'-='
t_PLUSEQUAL         =   r'\+='
t_TIMESEQUAL        =   r'\*='
t_DIVIDEEQUAL       =   r'/='
t_LEFTARROW         =   r'<-'
t_RIGHTARROW        =   r'->'
t_LEFTPARENTHESIS   =   r'\('
t_RIGHTPARENTHESIS  =   r'\)'
t_LEFTCURLYBRACKET  =   r'\{'
t_RIGHTCURLYBRACKET =   r'\}'
t_LEFTBRACKET       =   r'\['
t_RIGHTBRACKET      =   r'\]'
t_CTE_STRING        =   r'"([^\\"\n]+|\\.)*"'
t_CTE_FLOAT         =   r'[+-]?[0-9]+\.[0-9]+([Ee][+-]?[0-9]*)?'
t_CTE_INT           =   r'[0-9]+'
t_CTE_CHAR          =   r'[a-zA-Z0-9]'
t_DOT               =   r'\.'
t_SEMICOLON         =   r';'
t_COLON             =   r':'
t_COMMA             =   r','

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
# epsilon
def p_empty(p):
    '''empty :'''
    pass

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
# <VARS>
def p_vars(p):
    """vars :   VAR tipoCompuesto ID vars2 SEMICOLON vars4
            |   VAR tipoSimple ID vars3 SEMICOLON vars4"""

def p_vars2(p):
    '''vars2 :  COMMA ID vars2
             |  empty'''

def p_vars3(p):
    '''vars3 :  LEFTBRACKET CTE_INT RIGHTBRACKET vars3
             |  COMMA ID vars3
             |  empty'''

def p_vars4(p):
    '''vars4 :  tipoCompuesto ID vars2 SEMICOLON vars4
             |  tipoSimple ID vars3 SEMICOLON vars4
             |  empty'''


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
def p_instr(p):
    """instr : INSTR VOID ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | INSTR tipoSimple ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
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
def p_bloque(p):
    """bloque : LEFTCURLYBRACE bloque2 RIGHTCURLYBRACE"""

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
    '''variable :   ID DOT ID
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
    '''lectura  :   INPUT LEFTARROW variable semicolon'''

# <Llamada>
def p_llamada(p):
    '''llamada  :   ID LEFTPARENTHESIS exp llamada2 RIGHTPARENTHESIS SEMICOLON'''

def p_llamada2(p):
    '''llamada2 :   COMMA exp
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

lexer = lex.lex()
parser = yacc.yacc()

try:
    f = open("mogavity/test.txt", 'r')
    r = f.read()
    f.close()
except FileNotFoundError:
    print("No hay archivo para probar")

parser.parse(r)
print("Código correcto")
