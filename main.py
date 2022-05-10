"""
Lexer for the Mogavity Programming Language
Created by Clarissa V, and Hisao Y
March 2022
Usage for the Compiler´s Design Course
"""
from xmlrpc.client import Boolean
import ply.yacc as yacc
import ply.lex as lex
import logging
from function_directory import FunctionDirectory
import quadruples_generator
from quadruple import Quadruple
from temporal import Temporal
from Stack import Stack
import oracle

from error_handling import info, error, warning

from pprint import pprint

logging.basicConfig(level=logging.DEBUG)

# class_table = class_directory.ClassTable()
func_table = FunctionDirectory()
quad = Quadruple(0, "", "", "", "")
temp = Temporal()

poper = Stack()
stackO = Stack()
stack_type = Stack()
stackJumps = Stack()

quads = []

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
    # print('here xd')


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
    # print("here tipo simple")


# TODO: Actualizar el diagrama instr
# TODO: Volver a agregar instr2 cuando resolvamos el bug
# <Instr>
def p_instr(p):
    """instr : INSTR VOID ID new_function LEFTPARENTHESIS params RIGHTPARENTHESIS instr2 bloque
    | INSTR tipoSimple ID new_function LEFTPARENTHESIS params RIGHTPARENTHESIS instr2 bloque
    """


def p_instr2(p):
    """instr2 : vars
              | empty"""
    pass


# <Params>
def p_params(p):
    """params : tipoSimple ID
    | tipoSimple ID COMMA params1
    | empty
    """
    pass


# <Params1>
def p_params1(p):
    """params1 : tipoSimple ID ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | instr tipoSimple ID LEFTPARENTHESIS params RIGHTPARENTHESIS bloque
    | empty
    """
    # print('here222')


# <Bloque>
def p_bloque(p):
    """bloque : LEFTCURLYBRACKET bloque2 RIGHTCURLYBRACKET"""
    # print('here bloque')


def p_bloque2(p):
    '''bloque2  :   estatuto bloque2
                |   empty'''
    # print('here')


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
    # print(p[1])
    # print(stackO.top())
    exp = stackO.pop()
    # exp_type = stack_type.pop()
    _ = stack_type.pop()
    new_quad = quad.generate_quad('=', exp, None, p[1])
    new_quad.print_quad()
    quads.append(new_quad)


# <Variable>
def p_variable(p):
    """variable :   ID
                |   ID DOT ID
                |   ID LEFTBRACKET exp RIGHTBRACKET
                |   ID LEFTBRACKET exp RIGHTBRACKET LEFTBRACKET exp RIGHTBRACKET"""
    p[0] = p[1]


# <Condicion>
def p_condicion(p):
    """condicion    :   IF LEFTPARENTHESIS exp RIGHTPARENTHESIS np_if_1 bloque np_if_2
                    |   IF LEFTPARENTHESIS exp RIGHTPARENTHESIS np_if_1 bloque condicion2"""
    # print('here?2342423')


def p_condicion2(p):
    """condicion2   :   OTHERWISE np_else bloque np_if_2
                    |   np_if_2 ELIF LEFTPARENTHESIS exp RIGHTPARENTHESIS np_if_1 bloque condicion2"""
    # print('here again')


# <Escritura>
def p_escritura(p):
    """escritura    :   OUTPUT RIGHTARROW exp generate_write_quad escritura2 SEMICOLON
                    |   OUTPUT RIGHTARROW CTE_STRING generate_write_quad escritura2 SEMICOLON"""


def p_escritura2(p):
    """escritura2   :   COMMA exp generate_write_quad escritura2
                    |   COMMA CTE_STRING generate_write_quad escritura2
                    |   empty"""


# <Lectura>
def p_lectura(p):
    """lectura  :   INPUT LEFTARROW variable SEMICOLON"""
    new_quad = quad.generate_quad('INPUT', None, None, p[3])
    quads.append(new_quad)


# <Llamada>
def p_llamada(p):
    """llamada  :   ID function_detection LEFTPARENTHESIS llamada2 RIGHTPARENTHESIS SEMICOLON"""


def p_llamada2(p):
    """llamada2 :   exp llamada2
                |   COMMA exp llamada2
                |   empty"""


# <CicloW>
def p_cicloW(p):
    """cicloW   :   WHILE np_while_1 LEFTPARENTHESIS exp RIGHTPARENTHESIS np_while_2 bloque np_while_3"""
    # print('w')


# <CicloFor>
def p_cicloFor(p):
    """cicloFor :   FOR LEFTPARENTHESIS assign SEMICOLON exp SEMICOLON update RIGHTPARENTHESIS bloque"""
    # print('f')


# <Assign>
def p_assign(p):
    """assign   :   ID ASSIGNMENT CTE_INT"""


# <Update>
def p_update(p):
    """update   :   ID PLUSEQUAL CTE_INT
                |   ID MINUSEQUAL CTE_INT
                |   ID TIMESEQUAL CTE_INT
                |   ID DIVIDEEQUAL CTE_INT"""


# <Return>
def p_return(p):
    """return   :   RETURN exp SEMICOLON"""


# <Exp>
def p_exp(p):
    """exp  :   expA add_operator_or expOR"""


def p_expOR(p):
    """expOR    :   OR save_op expA expOR
                |   empty"""


# <ExpA>
def p_expA(p):
    """expA :   expB add_operator_and expAND"""


def p_expAND(p):
    """expAND   :   AND save_op expB expAND
                |   empty"""


# <ExpB>
def p_expB(p):
    """expB :   expC add_operator_loop expLOOP"""


def p_expLOOP(p):
    """expLOOP  :   LESSTHAN save_op expB
                |   GREATERTHAN save_op expB
                |   EQUALLESSTHAN save_op expB
                |   EQUALGREATERTHAN save_op expB
                |   EQUALS save_op expB
                |   NOTEQUAL save_op expB
                |   empty"""


# <ExpC>
def p_expC(p):
    '''expC :   termino add_operator_plusminus expPM'''


# TODO: Agregué un punto neuralgico justo despues de operador PLUS para ver si esa es la lógica para poder generar correctamente los cuadruplos aritmeticos
# al parecer sí funciona pero tenemos el bug del oraculo SOS que no me deja ver si es correcta la implementación
def p_expPM(p):
    """expPM    :   PLUS save_op expC
                |   MINUS save_op expC
                |   empty"""
    # if p[1] is not None:
    #     poper.push(p[1])
    #     print('xd not none' + poper.top())
    # print("xd2")
    # print(poper)


### LLEGA A TERMINO, ENTRA A FACTOR Y LUEGO EJECUTA EL PUNTO NEURALGICO, Y PUFFF (RESOLVED)
# <Termino>
def p_termino(p):
    '''termino  :   factor add_operator_multiplydivide expMD'''
    # print('xd'+ p[-1])


def p_expMD(p):
    '''expMD    :   TIMES save_op termino
                |   DIVIDE save_op termino
                |   empty'''

    # print('here')


# TODO: Update factor diagram
# <Factor>
def p_factor(p):
    '''factor   :   LEFTPARENTHESIS exp RIGHTPARENTHESIS
                |   CTE_INT save_id
                |   CTE_FLOAT save_id
                |   CTE_CHAR save_id
                |   variable save_id
                |   llamada'''
    pass


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
    error("Syntax error on " + token)
    exit()


########################################################
################ PUNTOS NEURALGICOS ####################
########################################################

def p_new_program(p):
    """new_program : """
    global func_table


def p_save_program(p):
    """save_program :"""
    print()
    # func_table.add_elements(p[-1], "program")


# Agregar Variable en Tabla
def p_new_variable(p):
    """new_variable : """
    func_table.add_variable(p[-1], current_scope, tmp_type)
    func_table.print_all_variable_tables()


def p_new_variable_set_type(p):
    """new_variable_set_type : """
    global tmp_type
    if p[-1] is not None:
        tmp_type = p[-1]


def p_new_function(p):
    """new_function :"""
    global current_scope
    current_scope = p[-1]
    func_table.add_function(p[-1], tmp_type)


def p_save_id(p):
    """save_id :"""
    stackO.push(p[-1])
    if p[-1].isdigit():
        stack_type.push("int")
    else:
        var_type = func_table.get_var_type(p[-1], current_scope)
        stack_type.push(var_type)
    # TODO: check for float


def p_save_op(p):
    """save_op :"""
    if p[-1] is not None:
        poper.push(p[-1])


def p_add_operator_plusminus(p):
    """add_operator_plusminus : """
    """if poper.top() is not None:
        print("ADD")"""
    if poper.top() == '+' or poper.top() == '-':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        print(result_type)
        if result_type != -1:
            print("si baila mija con en senor")
           # tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(result_type)
            new_quad = quad.generate_quad(op, left_op, right_op, res[0])
            new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Type mismatch at " + str(p.lineno))


def p_add_operator_multiplydivide(p):
    """add_operator_multiplydivide : """
    # print('poper md', p[-1])
    # poper.size()

    if poper.top() == '*' or poper.top() == '/':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        #  print(right_op, right_type, left_op, left_type, op)
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            print("si baila mija con en senor")
            tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(tmp_type)
            new_quad = quad.generate_quad(op, left_op, right_op, res[0])
            new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Type Mismatched")


def p_add_operator_loop(p):
    """add_operator_loop :"""
    # print('poper ' + poper)

    if poper.top() == '<=' or poper.top() == '<' or poper.top() == '>' or poper.top() == '>=' or poper.top() == '==' or poper.top() == '!=':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            print("si baila mija con en senor")
            #tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(result_type)
            new_quad = quad.generate_quad(op, left_op, right_op, res[0])
            new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Type Mismatched")


def p_add_operator_and(p):
    """add_operator_and :"""
    # print('poper ' + poper)

    if poper.top() == 'AND':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            print("si baila mija con en senor")
            tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(tmp_type)
            new_quad = quad.generate_quad(op, left_op, right_op, res[0])
            new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Type Mismatched")


def p_add_operator_or(p):
    """add_operator_or :"""
    # print('poper ' + poper)

    if poper.top() == 'OR':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            print("si baila mija con en senor")
            tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(tmp_type)
            new_quad = quad.generate_quad(op, left_op, right_op, res[0])
            new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Operator type mismatched at line: " + str(p.lineno()))


#  Neuralgic Point for function detection
def p_function_detection(p):
    """function_detection :"""
    func_table.get_function(p[-1], "0")  # str(p.lineno())
    # Verify function exists
    # Start handling execution
    pass


def p_generate_write_quad(p):
    """generate_write_quad :"""
    print("WRTIE ESCRIBIRRRR FASFDSAD")
    print(p[-1])
    # When it is a string we can directly generate the quad
    if isinstance(p[-1], str):
        print("ENTER STRING")
        new_quad = quad.generate_quad("OUTPUT", None, None, p[-1])
        new_quad.print_quad()
        quads.append(new_quad)
    # If it is not a string, then it is an exp and we should already have it in stackO, remebering that it is a temporal
    else:
        print("ENTER EXPPPP")
        res = stackO.pop()
        # We don't really need the type, do we?
        stack_type.pop()
        # We generate the quad
        new_quad = quad.generate_quad("OUTPUT", None, None, res)
        new_quad.print_quad()
        quads.append(new_quad)


"""
One to start and one to end the program? Maybe this simplifies our execution flow when converting
instructions in the virtual machine?

Should we maybe add one when we call a function inside a function? 
"""


def p_np_print(p):
    """np_print :"""
    print("sos aqui")


def p_change_scope(p):
    """change_scope : """
    global current_scope
    current_scope = p[-1]


# Verificar el tipo de la variable


####################################
######### PUNTOS DEL IF ############
####################################
def p_np_if_1(p):
    """np_if_1 : """
    print("IFIIFIFIFIF")
    cond = stackO.pop()
    type_cond = stack_type.pop()
    # if type_cond then it is a malformed if
    print(type_cond)
    if type_cond != "bool":
        error("Expected type bool")
    else:
        new_quad = quad.generate_quad("GOTOF", cond, None, None)
        stackJumps.push(new_quad.id - 1)
        quads.append(new_quad)


def p_np_if_2(p):
    """np_if_2 : """
    num_quad = stackJumps.pop()
    # fill_quad
    tmp_quad = quads[num_quad]
    tmp_quad.fill_quad(len(quads) + 1)
    tmp_quad.print_quad()

def p_np_else(p):
    """np_else : """
    false = stackJumps.pop()
    new_quad = quad.generate_quad("GOTO", None, None, None)
    stackJumps.push(new_quad.id - 1)
    quads.append(new_quad)
    tmp_quad = quads[false]
    tmp_quad.fill_quad(len(quads) + 1)
    tmp_quad.print_quad()


####################################
######### PUNTOS DEL FOR ###########
####################################
# def p_np_for_1(p):
#     """np_for_1 : """
#     stackO.push(id) ####
#     stack_type.push(type) #####
#     # vailidate that tit is numeric, if not break (var we mean)


#     print("FORRRRRRRRR")

# def p_np_for_2(p):
#     """np_for_2 : """
#     print("FORRRRRRRRR")
#     exp_type = stack_type.pop()
#     if(exp_type != numeric tyoe):
#         error("Type mismatch")
#     else:
#         exp = stackO.pop()
#         vControl = stackO.top()
#         control_type = stack_type.top()
#         result_type = oracle.use_oracle(control_type, exp_type, "=")
#         #  Cubo semantico se encarga de errores aqui
#         quad.generate_quad("=", exp, vControl, None) ## Ahi va en none?


# def p_np_for_3(p):
#     """np_for_3 : """
#     print("FORRRRRRRRR")

# def p_np_for_4(p):
#     """np_for_4 : """
#     print("FORRRRRRRRR")


####################################
######## PUNTOS DEL WHILE ##########
####################################
def p_np_while_1(p):
    """np_while_1 : """
    print("WHHHHHIIILLLEEEE")
    stackJumps.push(len(quads) + 1)  # cont


def p_np_while_2(p):
    """np_while_2 : """
    cond = stackO.pop()
    type_cond = stack_type.pop()
    if type_cond != "bool":
        error("Expected type bool")
    else:
        new_quad = quad.generate_quad("GOTOF", cond, None, None)
        stackJumps.push(new_quad.id - 1)
        quads.append(new_quad)


def p_np_while_3(p):
    """np_while_3 : """
    false = stackJumps.pop()
    ret = stackJumps.pop()
    print(false)
    new_quad = quad.generate_quad("GOTO", None, None, ret)
    new_quad.print_quad()
    quads.append(new_quad)
    tmp_quad = quads[false]
    tmp_quad.fill_quad(len(quads) + 1)
    tmp_quad.print_quad()


parser = yacc.yacc()
r = None
try:
    f = open("test4.txt", 'r')
    r = f.read()
    f.close()
except FileNotFoundError:
    error("No hay archivo para probar")

parser.parse(r)
# parser.parse(r, debug=1)
print("Código Aceptado")
#print(func_table.function_table)

#  TODO implement warning when a variable is unused.
#  TODO implement warning when function is unused.
