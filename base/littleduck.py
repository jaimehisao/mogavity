# Lexer and Parser for Little Duck Programming Languaje
# Clarissa Andrea Velásquez Magaña A01281743

# List of token names
tokens = [
    'ID',
    'CTEINT',
    'CTEFLOAT',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'GTHAN',
    'LTHAN',
    'DIFF',
    'LPAREN',
    'RPAREN',
    'DOTCOM',
    'COMMA',
    'TWODOT',
    'LBRACE',
    'RBRACE',
]

# Tokens
t_CTEINT    = r'[0-9]+'
t_CTEFLOAT  = r'[+-]?[0-9]+\.[0-9]+([Ee][+-]?[0-9]*)?'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'\='
t_GTHAN     = r'>'
t_LTHAN     = r'<'
t_DIFF      = r'<>'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_DOTCOM    = r';'
t_COMMA     = r','
t_TWODOT    = r':'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_STRING    = r'"([^\\"\n]+|\\.)*"'

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'var' : 'VAR',
    'program' : 'PROGRAM',
    'int' : 'INT',
    'float' : 'FLOAT',
    'print' : 'PRINT',
}

tokens = tokens + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z]+(_?[a-zA-Z0-9]+)*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Gramáticas
# <PROGRAMA>
def p_programa(p):
    '''programa : PROGRAM ID DOTCOM vars bloque
                | PROGRAM ID DOTCOM bloque'''
# epsilon
def p_empty(p):
    '''empty :'''
    pass

# <TIPO>
def p_tipo(p):
    '''tipo : INT
            | FLOAT'''

# <VARCTE>
def p_varcte(p):
    '''varcte : ID
              | CTEINT
              | CTEFLOAT'''

# <CONDICION>
def p_condicion(p):
    '''condicion : IF LPAREN expresion RPAREN bloque DOTCOM
                 | IF LPAREN expresion RPAREN bloque ELSE bloque DOTCOM'''

# <ASIGNACION>
def p_asignacion(p):
    '''asignacion : ID EQUALS expresion DOTCOM'''

# <ESCRITURA>
def p_escritura(p):
    '''escritura : PRINT LPAREN esc1 RPAREN DOTCOM'''

def p_esc1(p):
    '''esc1 : expresion esc2
            | STRING esc2'''

def p_esc2(p):
    '''esc2 : COMMA esc1
            | empty'''

# <ESTATUTO>
def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura'''

# <VARS>
def p_vars(p):
    '''vars : VAR var1'''

def p_var1(p):
    '''var1 : ID COMMA var1
            | ID var2'''

def p_var2(p):
    '''var2 : TWODOT tipo DOTCOM var1
            | TWODOT tipo DOTCOM'''

# <BLOQUE>
def p_bloque(p):
    '''bloque : LBRACE bloque1 RBRACE'''

def p_bloque1(p):
    '''bloque1 : estatuto bloque1
               | empty'''

# <EXPRESION>
def p_expresion(p):
    '''expresion : exp
                 | exp GTHAN exp
                 | exp LTHAN exp
                 | exp DIFF exp'''

# <EXP>
def p_exp(p):
    '''exp : termino exp1'''

def p_exp1(p):
    '''exp1 : PLUS exp
            | MINUS exp
            | empty'''

# <TERMINO>
def p_termino(p):
    '''termino : factor ter1'''

def p_ter1(p):
    '''ter1 : TIMES termino
            | DIVIDE termino
            | empty'''

# <FACTOR>
def p_factor(p):
    '''factor : LPAREN expresion RPAREN
              | PLUS varcte
              | MINUS varcte
              | varcte'''


def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"({p.value}) on line {p.lineno}"
            
    print(f"Syntax error: {token}")
    exit()

import ply.yacc as yacc
parser = yacc.yacc()

try:
    f = open("3.2ply/test.txt", 'r')
    r = f.read()
    f.close()
except FileNotFoundError:
    print("No hay archivo para probar")

parser.parse(r)
print("Código correcto")


