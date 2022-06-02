"""
Lexer for the Mogavity Programming Language
Created by Clarissa V, and Hisao Y
March 2022
Usage for the Compiler´s Design Course
"""
from audioop import mul
from re import M
import ply.yacc as yacc
import ply.lex as lex
from function_directory import FunctionDirectory as fD, NodeArray
from quadruple import Quadruple
from temporal import Temporal
from Stack import Stack
import oracle
import virtual_machine as vm
from error_handling import info, error, warning
from pprint import pprint

# logging.basicConfig(level=logging.DEBUG)

fD = fD()
fD.function_table["global"].add_variable("global", "int")
quad = Quadruple(0, "", "", "", "")
temp = Temporal()


###################
##### STACKS ######
###################
poper = Stack()  # Operator Stack
stackO = Stack()  # Operand Stack
stack_type = Stack()  # Type Stack
stackJumps = Stack()  # Jump Stack
memory = Stack()  # Memory Stack ()?
stack_dim = Stack()  # Dimension Stack

quads = []

global current_scope
global num_params
global cont_temporals
global elif_num
global param_counter
global function_id
global last_scope
elif_num = 0
current_scope = 'global'
last_scope = ""
num_params = 0
cont_temporals = 0
param_counter = 0

vControl = ""
vFinal = ""
for_op = ""
for_updater = 0

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
    "UNDERSCORE",
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
# t_CTE_CHAR = r'[a-zA-Z0-9]'
t_CTE_CHAR = r'[a-zA]'
t_DOT = r'\.'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_UNDERSCORE = r'\_'

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
    """programa : PROGRAM new_program ID save_program SEMICOLON class vars instr MAIN np_main bloque np_end_func end_of_file
    | PROGRAM new_program ID save_program SEMICOLON class instr MAIN np_main bloque np_end_func end_of_file
    | PROGRAM new_program ID save_program SEMICOLON vars instr MAIN np_main bloque np_end_func end_of_file
    | PROGRAM new_program ID save_program SEMICOLON vars MAIN np_main bloque np_end_func end_of_file
    | PROGRAM new_program ID save_program SEMICOLON instr MAIN np_main bloque np_end_func end_of_file
    | PROGRAM new_program ID save_program SEMICOLON MAIN np_main bloque np_end_func end_of_file
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
    """vars :   VAR tipoCompuesto new_variable_set_type ID new_variable vars2 SEMICOLON
            |   VAR tipoSimple new_variable_set_type ID new_variable vars3 SEMICOLON
            | empty """


def p_vars2(p):
    '''vars2 :  COMMA ID new_variable vars2
             |  empty'''


def p_vars3(p):
    '''vars3 :  LEFTBRACKET set_array set_dim_and_r CTE_INT set_limits RIGHTBRACKET set_each_node set_virtual_address vars5
             |  LEFTBRACKET set_array set_dim_and_r CTE_INT set_limits RIGHTBRACKET set_each_node LEFTBRACKET CTE_INT set_limits RIGHTBRACKET set_each_node set_virtual_address vars5
             |  ID new_variable vars5
             |  vars5'''


def p_vars4(p):
    '''vars4 :  VAR tipoCompuesto ID new_variable vars2 SEMICOLON vars4
             |  VAR tipoSimple ID new_variable vars3 SEMICOLON vars4
             |  empty'''

def p_vars5(p):
    '''vars5 :  COMMA vars3
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
# <Instr>
def p_instr(p):
    """instr : INSTR VOID ID new_function LEFTPARENTHESIS params set_number_params RIGHTPARENTHESIS LEFTCURLYBRACKET vars set_local_vars save_curr_quad bloque2 RIGHTCURLYBRACKET np_end_func instr
              | INSTR tipoSimple ID new_function LEFTPARENTHESIS params set_number_params RIGHTPARENTHESIS LEFTCURLYBRACKET vars set_local_vars save_curr_quad bloque2 RIGHTCURLYBRACKET np_end_func instr
              | empty
    """
##  TODO INSTR modificado para soportar la declaracion de multiples funciones

# <Params>
def p_params(p):
    """params : tipoSimple new_variable_set_type set_params ID new_variable_param params
    | COMMA tipoSimple new_variable_set_type set_params ID new_variable_param params
    | empty
    """
    pass


# <Bloque>
def p_bloque(p):
    """bloque : LEFTCURLYBRACKET bloque2 RIGHTCURLYBRACKET"""
    # print('here bloque')


def p_bloque2(p):
    '''bloque2  :   estatuto bloque2
                |   empty'''
    print('here')


# <Estatuto>
def p_estatuto(p):
    """estatuto :   asignacion
                |   llamada
                |   condicion
                |   escritura
                |   lectura
                |   cicloW
                |   cicloFor
                |   return
    """

#TODO: Check how to see if we are using assingment with a temporal pointer, idea: check stackO.size like in generate_write_quad
# <Asignación>
def p_asignacion(p):
    '''asignacion   :   variable ASSIGNMENT exp SEMICOLON'''
    # print(p[1])
    print(stackO.size())
    exp = stackO.pop()
    is_array = fD.function_table[current_scope].variable_table[p[1]].has_dimensions
    # exp_type = stack_type.pop()
    _ = stack_type.pop()
    address = 0
    if fD.get_var_type(p[1], current_scope) and (is_array == False):
        address = fD.get_variable_address(current_scope, p[1])
        #print("ADDRESS FOR ", p[1], "in scope", current_scope, "is", address)
    elif is_array and int(stackO.top()) >= 100000:
        address = stackO.top()
    else:
        print("no addr?")

    new_quad = quad.generate_quad('=', exp, None, address)
    #print("ASIGN QUAD")
    #new_quad.print_quad()
    # new_quad.print_quad()
    quads.append(new_quad)


# <Variable>
def p_variable(p):
    """variable :   ID
                |   ID DOT ID
                |   ID add_array_id LEFTBRACKET verify_dims exp array_quads RIGHTBRACKET end_array_call"""
    p[0] = p[1]

def p_variable2(p):
    """variable2 :  LEFTBRACKET verify_dims exp RIGHTBRACKET array_quads update_dim LEFTBRACKET exp array_quads RIGHTBRACKET end_array_call
                 |  empty"""


# <Condicion>
def p_condicion(p):
    """condicion    :   IF LEFTPARENTHESIS exp RIGHTPARENTHESIS np_if_1 bloque np_if_2
                    |   IF LEFTPARENTHESIS exp RIGHTPARENTHESIS np_if_1 bloque condicion2"""
    print('here?2342423')


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
    address = fD.get_variable_address(current_scope, p[3])
    ## TODO VALIDATE VARIABLE EXISTANCE
    new_quad = quad.generate_quad('INPUT', None, None, address)
    quads.append(new_quad)


# <Llamada>
def p_llamada(p):
    """llamada  :   UNDERSCORE ID function_detection LEFTPARENTHESIS llamada2 verify_coherence_of_params RIGHTPARENTHESIS function_gosub SEMICOLON"""


def p_llamada2(p):
    """llamada2 :   add_to_param_counter exp verify_param llamada2
                |   COMMA add_to_param_counter exp verify_param llamada2
                |   empty"""


# <CicloW>
def p_cicloW(p):
    """cicloW   :   WHILE np_while_1 LEFTPARENTHESIS exp RIGHTPARENTHESIS np_while_2 bloque np_while_3"""


# <CicloFor>
def p_cicloFor(p):
    """cicloFor :   FOR LEFTPARENTHESIS assign_for SEMICOLON exp for_exp_comp SEMICOLON update np_for_3 RIGHTPARENTHESIS bloque np_for_4"""
    # print('f')

"""
# <CicloFor>
def p_cicloFor(p):
    cicloFor :   
    FOR LEFTPARENTHESIS assign_for SEMICOLON exp SEMICOLON update np_for_3 RIGHTPARENTHESIS bloque np_for_4
    # print('f')
"""


# TODO: update assign diagram
# <Assign>
def p_assign_for(p):
    """assign_for   :   ID for_declaration ASSIGNMENT exp"""


"""assign_for   :   ID np_for_1 ASSIGNMENT exp np_for_2"""


# <Update>
def p_update(p):
    """update   :   ID PLUSEQUAL CTE_INT 
                |   ID MINUSEQUAL CTE_INT
                |   ID TIMESEQUAL CTE_INT
                |   ID DIVIDEEQUAL CTE_INT"""
    global for_op
    global for_updater
    if p[2] == "+=":
        for_op = "+"
    elif p[2] == "-=":
        for_op = "-"
    elif p[2] == "*=":
        for_op = "*"
    else:
        for_op = "/"
    for_updater = p[3]


# <Return>
def p_return(p):
    """return   :   RETURN exp end_func_return SEMICOLON"""


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
                |   CTE_INT save_pvar_int save_constant_int
                |   CTE_FLOAT save_pvar_float save_constant_float
                |   CTE_CHAR save_pvar_int save_constant_int
                |   llamada
                |   variable save_pvar_var save_id
                '''
    pass


def p_error(p):
    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])
    if p == None:
        token = "end of file"
    else:
        token = f"({p.value}) on line {p.lineno}"
    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))
    error("Syntax error on " + token)



########################################################
################ PUNTOS NEURALGICOS ####################
########################################################

def p_new_program(p):
    """new_program : """
    # Generar el quad del main
    new_quad = quad.generate_quad("GOTO", None, None, None)
    quads.append(new_quad)
    stackJumps.push(new_quad.id)


def p_save_program(p):
    """save_program :"""
    print()
    # func_table.add_elements(p[-1], "program")


# Generar el quad del main
def p_np_main(p):
    """np_main : """
    global current_scope, last_scope
    last_scope = current_scope
    current_scope = "global"
    num_quad = stackJumps.pop() #it should always be 1
    tmp_quad = quads[num_quad-1]
    tmp_quad.fill_quad(len(quads) + 1)


# Agregar Variable en Tabla
def p_new_variable(p):
    """new_variable : """
    #print("TMP TYPE", tmp_type, "VAR", p[-1])
    print("Adding new variable", "CURRENT SCOPE", current_scope, "VAR", p[-1])
    address = fD.function_table[current_scope].add_variable(p[-1], tmp_type)
    print("New variable address", address)
    #fD.function_table.print_all_variable_tables()


def p_new_param_variable(p):
    """new_variable_param : """
    name = p[-1]
    address = fD.function_table[current_scope].add_variable(name, tmp_type)
    fD.function_table[current_scope].parameter_table.append(address)


def p_new_variable_set_type(p):
    """new_variable_set_type : """
    global tmp_type
    if p[-1] is not None:
        tmp_type = p[-1]


def p_save_id(p):
    """save_id :"""
    global pvar
    # if stackO.is_Empty() == False:
    #     return
    address = fD.get_variable_address(pvar, current_scope)
    stackO.push(address)
    var_type = fD.get_var_type(pvar, current_scope)
    stack_type.push(var_type)


def p_save_constant_int(p):
    """save_constant_int : """
    global pvar
    tmp_int = int(pvar)
    address = fD.get_constant(tmp_int)
    stackO.push(address)
    stack_type.push("int")


def p_save_constant_float(p):
    """save_constant_float : """
    global pvar
    tmp_float = float(pvar)
    address = fD.get_constant(tmp_float)
    stackO.push(address)
    stack_type.push("float")  ## Maybe we can change this to our int operator codes.


def p_save_op(p):
    """save_op :"""
    if p[-1] is not None:
        poper.push(p[-1])


# Save type of param into our ParamList
def p_set_params(p):
    """set_params : """
    global num_params
    #global tmp_id
    fD.function_table[current_scope].add_param(tmp_type)
    num_params += 1


# Save the amount of params in DirFunc
def p_set_number_params(p):
    """set_number_params : """
    fD.function_table[current_scope].set_params(num_params)
    ## TODO a mi se me hace que esto es extra y podemos calcular el numero de params con len()


# Save the initial address of the function with its quad
def p_save_curr_quad(p):
    """save_curr_quad : """
    fD.function_table[current_scope].set_quadruple(quads[-1].id + 1)


# Save the amount of local variables in DirFunc
def p_set_local_vars(p):
    """set_local_vars : """
    fD.function_table[current_scope].set_vars()


def p_add_operator_plusminus(p):
    """add_operator_plusminus : """
    global cont_temporals
    if poper.top() == '+' or poper.top() == '-':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            # tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(result_type)
            if current_scope != "global":
                cont_temporals += 1
            temporal = fD.function_table[current_scope].memory_manager.assign_new_temp()
            new_quad = quad.generate_quad(op, left_op, right_op, temporal)
            # new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(temporal)
            stack_type.push(res[1])
        else:
            error("Type mismatch at " + str(p.lexer.lineno))


def p_add_operator_multiplydivide(p):
    """add_operator_multiplydivide : """
    # print('poper md', p[-1])
    # poper.size()
    global cont_temporals
    if poper.top() == '*' or poper.top() == '/':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        #  print(right_op, right_type, left_op, left_type, op)
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            # tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(tmp_type)
            if current_scope != "global":
                cont_temporals += 1
            temporal = fD.function_table[current_scope].memory_manager.assign_new_temp()
            new_quad = quad.generate_quad(op, left_op, right_op, temporal)
            #new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Type Mismatched")


def p_add_operator_loop(p):
    """add_operator_loop :"""
    global cont_temporals
    if poper.top() == '<=' or poper.top() == '<' or poper.top() == '>' or poper.top() == '>=' \
            or poper.top() == '==' or poper.top() == '!=':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            # tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(result_type)
            if current_scope != "global":
                cont_temporals += 1
            temporal = fD.function_table[current_scope].memory_manager.assign_new_temp()
            new_quad = quad.generate_quad(op, left_op, right_op, temporal)
            #new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(temporal)
            stack_type.push(res[1])
        else:
            error("Type Mismatched")


def p_add_operator_and(p):
    """add_operator_and :"""
    global cont_temporals
    if poper.top() == 'AND':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            # tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(tmp_type)
            if current_scope != "global":
                cont_temporals += 1
            temporal = fD.function_table[current_scope].memory_manager.assign_new_temp()
            new_quad = quad.generate_quad(op, left_op, right_op, temporal)
            new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Type Mismatched")


def p_add_operator_or(p):
    """add_operator_or :"""
    global cont_temporals
    if poper.top() == 'OR':
        right_op = stackO.pop()
        right_type = stack_type.pop()
        left_op = stackO.pop()
        left_type = stack_type.pop()
        op = poper.pop()
        result_type = oracle.use_oracle(left_type, right_type, op)
        if result_type != -1:
            # tmp_type = oracle.convert_number_type_to_string_name(result_type)
            res = temp.get_temp(tmp_type)
            if current_scope != "global":
                cont_temporals += 1
            temporal = fD.function_table[current_scope].memory_manager.assign_new_temp()
            new_quad = quad.generate_quad(op, left_op, right_op, temporal)
            # new_quad.print_quad()
            quads.append(new_quad)
            stackO.push(res[0])
            stack_type.push(res[1])
        else:
            error("Operator type mismatched at line: " + str(p.lineno()))    


def p_generate_write_quad(p):
    """generate_write_quad :"""
    # When it is a string we can directly generate the quadm still we need to assign an address to the constant
    if isinstance(p[-1], str):
        address = fD.get_constant(p[-1])  # CTE address generated for value.
        new_quad = quad.generate_quad("OUTPUT", None, None, address)  # Quad is generated using CTE address.
        quads.append(new_quad)
    else:
        res = stackO.pop()
        stack_type.pop()
        new_quad = quad.generate_quad("OUTPUT", None, None, res)  # Quad is generated based on operand stack.
        quads.append(new_quad)


def p_np_print(p):
    """np_print :"""
    print("sos aqui")


def p_change_scope(p):
    """change_scope : """
    global current_scope, last_scope
    last_scope = current_scope
    current_scope = p[-1]


# Verificar el tipo de la variable


####################################
######### PUNTOS DEL IF ############
####################################
def p_np_if_1(p):
    """np_if_1 : """
    stackJumps.show_all()
    cond = stackO.pop()
    print("cond", cond)
    type_cond = stack_type.pop()
    # if type_cond then it is a malformed if
    if type_cond != "bool":
        error("Expected type bool")
    else:
        new_quad = quad.generate_quad("GOTOF", cond, None, None)
        stackJumps.push(new_quad.id - 1)
        quads.append(new_quad)


def p_np_if_elif(p):
    """np_if_elif : """
    stackJumps.show_all()

    global elif_num
    cond = stackO.pop()
    print("cond", cond)
    type_cond = stack_type.pop()
    # if type_cond then it is a malformed if
    if type_cond != "bool":
        error("Expected type bool")
    else:
        new_quad = quad.generate_quad("GOTOF", cond, None, None)
        stackJumps.push(new_quad.id - 1)
        quads.append(new_quad)
        new_quad = quad.generate_quad("GOTO", None, None, None)
        stackJumps.push(new_quad.id - 1)
        quads.append(new_quad)
    elif_num += 1


def p_np_if_2(p):
    """np_if_2 : """
    stackJumps.show_all()

    # num_quad = stackJumps.pop()
    # fill_quad
    """
    global elif_num
    if elif_num != 0:
        for x in range(0, elif_num):
            num_quad = stackJumps.pop()
            tmp_quad = quads[num_quad]
            tmp_quad.fill_quad(len(quads) + 1)
    """

    num_quad = stackJumps.pop()
    tmp_quad = quads[num_quad]
    tmp_quad.fill_quad(len(quads) + 1)
    # tmp_quad.print_quad()
    elif_num = 0
    # TODO solo jala para un elif


def p_np_else(p):
    """np_else : """
    stackJumps.show_all()

    false = stackJumps.pop()
    new_quad = quad.generate_quad("GOTO", None, None, None)
    stackJumps.push(new_quad.id - 1)
    quads.append(new_quad)
    tmp_quad = quads[false]
    tmp_quad.fill_quad(len(quads) + 1)
    # tmp_quad.print_quad()


####################################
######### PUNTOS DEL FOR NUEVOS ###########
####################################

def p_for_declaration_control(p):
    """for_declaration : """

    control_var = p[-1]

    # Check if control var exists in either the local or global scope
    print("CURR SCOPE", current_scope, control_var)
    address = fD.get_variable_address(control_var, current_scope)
    _type = fD.get_var_type(control_var, current_scope)

    if _type != "int":
        error("Type mismatch on for statement in line " + str(p.lexer.lineno))

    stackO.push(address)
    stack_type.push(_type)


def p_for_exp_assign(p):
    """for_exp_assign : """
    _type = stack_type.pop()
    op_addr = stackO.pop()
    if _type != "int":
        error("1 Type mismatch on for statement in line " + str(p.lexer.lineno))

    v_control = stackO.top()
    v_control_type = stack_type.top()

    _ = oracle.use_oracle(v_control_type, _type, "=")

    _quad = quad.generate_quad("=", op_addr, "EXP FOR ASSIGN", v_control) #TODO REMOVE
    quads.append(_quad)

    control_var = p[-4]

    # Check if control var exists in either the local or global scope
    address = fD.get_variable_address(control_var, current_scope)
    _type = fD.get_var_type(control_var, current_scope)

    if _type != "int":
        error("2 Type mismatch on FOR statement in line " + str(p.lexer.lineno))

    stackO.push(address)
    stack_type.push(_type)


def p_for_exp_comp(p):
    """for_exp_comp : """
    op = stackO.pop()
    _type = stack_type.pop()
    print("TYPE", _type, op)
    """
        if _type != "int":
        error("3 Type mismatch on FOR statement in line " + str(p.lexer.lineno))
    """

    v_final = fD.function_table[current_scope].memory_manager.assign_new_temp()
    _quad = quad.generate_quad("=", op, None, v_final)
    quads.append(_quad)

    v_control = stackO.top()
    addr = fD.function_table[current_scope].memory_manager.assign_new_temp()
    _quad_2 = quad.generate_quad("<", v_control, v_final, addr)
    quads.append(_quad_2)
    stackJumps.push(_quad_2.id - 1)
    _quad_3 = quad.generate_quad("GOTOF", None, None, addr)
    quads.append(_quad_3)
    stackJumps.push(_quad_3.id-1)






####################################
######### PUNTOS DEL FOR ###########
####################################
def p_np_for_1(p):
    """np_for_1 : """
    address = fD.get_variable_address(current_scope, p[-1])
    stackO.push(address)
    id_type = fD.get_var_type(p[-1], current_scope)
    # vailidate that tit is numeric, if not break (var we mean)
    print(id_type)
    stack_type.show_all()
    if id_type == "int":
        stack_type.push(id_type)
    else:
        error("Expected type int")


def p_np_for_2(p):
    """np_for_2 : """
    global vControl
    exp_type = stack_type.pop()
    if exp_type != "int":
        error("Type mismatch in linex " + str(p.lexer.lineno))
    else:
        exp = stackO.pop()
        vControl = stackO.top()
        control_type = stack_type.top()
        _ = oracle.use_oracle(control_type, exp_type, "=")  # Cubo semantico se encarga de errores aqui
        new_quad = quad.generate_quad("=", exp, None, vControl)  ## Ahi va en none?
        print("NP FOR 2 - Generated Quad")
        new_quad.print_quad()
        quads.append(new_quad)


def p_np_for_3(p):
    """np_for_3 : """
    global cont_temporals
    stack_type.show_all()
    stackO.show_all()
    stack_type.pop() ## TODO PARCHE
    exp_type = stack_type.pop()
    if exp_type != "int":
        error("Type mismatch in linez " + str(p.lexer.lineno))
    else:
        exp = stackO.pop()
        vFinal = fD.function_table[current_scope].memory_manager.assign_new_temp()
        if current_scope != "global":
            cont_temporals += 1
        new_quad = quad.generate_quad("=", exp, "vFinal", vFinal)
        quads.append(new_quad)
        tmp_x = fD.function_table[current_scope].memory_manager.assign_new_temp()  ## replaced temp.get_temp("bool")
        if current_scope != "global":
            cont_temporals += 1
        new_quad = quad.generate_quad("<", vControl, vFinal, tmp_x)
        quads.append(new_quad)
        stackJumps.push(len(quads))
        new_quad = quad.generate_quad("GOTOF", tmp_x, None, None)
        quads.append(new_quad)
        stackJumps.push(len(quads) - 1)


def p_np_for_4(p):
    """np_for_4 : """
    global cont_temporals
    tmp_y = fD.function_table[current_scope].memory_manager.assign_new_temp()  ## replaced temp.get_temp("int")
    if current_scope != "global":
        cont_temporals += 1

    for_updater_constant = fD.get_constant(for_updater)
    new_quad = quad.generate_quad(for_op, vControl, for_updater_constant, tmp_y)


    quads.append(new_quad)
    # TODO: we have a duplicate quad but it's based on the FOR of the teacher ---> ASK WHAT'S WITH VC 
    new_quad = quad.generate_quad("=", tmp_y, "VCONTROL", vControl) ## TODO REMOVE 3 rd val
    quads.append(new_quad)
    new_quad = quad.generate_quad("=", tmp_y, "STACK 0. pop", stackO.pop())  # stackO.pop() has to be the original ID
    quads.append(new_quad)
    final = stackJumps.pop()
    ret = stackJumps.pop()
    new_quad = quad.generate_quad("GOTO", None, None, ret)
    quads.append(new_quad)
    tmp_quad = quads[final]
    tmp_quad.fill_quad(len(quads) + 1)
    stack_type.pop()


###############################
######## FAKE BOTTOM ##########
###############################
def p_create_fake_bottom(p):
    """create_fake_bottom :"""
    poper.push(p[-1])


def p_add_fake_bottom(p):
    """erase_fake_bottom :"""
    poper.pop()


####################################
######## ARRAYS ##########
####################################
def p_new_array(p):
    """new_array : """
    #  WE need to reserve the memory space for all the size of the array.
    size = p[-1]  # suponiendo, prob es diferente
    for i in range(0, size):
        fD.function_table[current_scope].memory_manager.assign_new_int_address()


####################################
######## PUNTOS DEL WHILE ##########
####################################
def p_np_while_1(p):
    """np_while_1 : """
    """
    exp_type = stack_type.pop()
    if (exp_type != bool):
        error("Type Mismatch")
    else:
        result = stackO.pop()
        new_quad = quad.generate_quad("GOTOF", result, None, None) #Pending to fill last
        # GENERAR GOTO EN FALSO
        stackJumps.push(new_quad.id - 1)
    """
    # print("WHHHHHIIILLLEEEE")
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
    # print(false)
    new_quad = quad.generate_quad("GOTO", None, None, ret)
    # new_quad.print_quad()
    quads.append(new_quad)
    tmp_quad = quads[false]
    tmp_quad.fill_quad(len(quads) + 1)
    # tmp_quad.print_quad()


#############################
######## FUNCTIONS ##########
#############################
def p_new_function(p):
    """new_function :"""
    global current_scope, num_params, cont_temporals, last_scope
    num_params = 0
    cont_temporals = 0
    last_scope = current_scope
    current_scope = p[-1]
    fD.add_function(p[-1], tmp_type)
    if tmp_type != "void":
        fD.function_table["global"].add_variable(p[-1], tmp_type)


#  Neuralgic Point for function detection
def p_function_detection(p):
    """function_detection :"""
    global param_counter, function_id
    function_id = p[-1]
    fD.check_if_exists(function_id)
    # Verify function exists
    # Start handling execution
    new_quad = quad.generate_quad("ERA", None, None, function_id)
    quads.append(new_quad)
    param_counter = 0


def p_verify_param(p):
    """verify_param : """
    global param_counter, function_id
    original_address = stackO.pop()
    arg_type = stack_type.pop()
    if fD.function_table[function_id].parameter_table_types[param_counter-1] == arg_type:
        param_addr = fD.function_table[function_id].parameter_table[param_counter-1]
        new_quad = quad.generate_quad("PARAMETER", original_address, None, param_addr)
        quads.append(new_quad)
    else:
        error("Type mismatched in parameters in scope " + current_scope)

def p_add_to_param_counter(p):
    """add_to_param_counter : """
    global param_counter
    param_counter += 1


def p_verify_coherence_of_params(p):
    """verify_coherence_of_params : """
    global param_counter
    #print("param count", param_counter, "len", len(fD.function_table[function_id].parameter_table))
    if param_counter == len(fD.function_table[function_id].parameter_table):
        pass
    else:
        error("Amount of parameters is incorrect for scope " + current_scope)


def p_function_gosub(p):
    """function_gosub : """
    gosub_quad = quad.generate_quad("GOSUB", function_id, None, fD.function_table[function_id].starting_quadruple)
    quads.append(gosub_quad)
    new_temp = fD.function_table[current_scope].memory_manager.assign_new_temp()
    function_global_address = fD.get_variable_address(function_id, "global")
    print("ID", function_id)
    guadalupano_quad = quad.generate_quad("=", function_global_address, "PARCHE GUADALUPANO", new_temp)  # TODO REMOVE
    quads.append(guadalupano_quad)
    stackO.push(new_temp)
    stack_type.push(fD.function_table[function_id].return_type)


def p_np_end_func(p):
    """np_end_func : """
    global cont_temporals
    new_quad = quad.generate_quad("ENDFUNC", None, None, None)
    quads.append(new_quad)
    fD.function_table[current_scope].set_temporals(cont_temporals)
    #fD.function_table[current_scope].release_var_table() lo hacemos en maq virtual
    cont_temporals = 0


## TODO VALIDAR RETORNO Y TIPO DE RETORNO
def p_end_func_return(p):
    """end_func_return : """

    # Obtain the function's return type
    return_type = fD.function_table[current_scope].return_type

    # Caso Void
    if return_type == "void":
        new_quad = quad.generate_quad("RETURN", None, None, None)
        quads.append(new_quad)

    # Caso valor de Retorno
    else:
        actual_return_type = type(pvar)
        if isinstance(pvar, int) or isinstance(pvar, float):
            item_to_return = fD.get_constant(pvar)
            if isinstance(item_to_return, int):
                actual_return_type = "int"
            elif isinstance(item_to_return, float):
                actual_return_type = "float"
        else:
            actual_return_type = fD.get_var_type(pvar, current_scope)
            item_to_return = fD.get_variable_address(pvar, current_scope)
        _ = oracle.use_oracle(return_type, actual_return_type, "=")  # Validate if the girl dances with the old guy

        function_global_address = fD.get_variable_address(current_scope, "global")
        equal_global_quad = quad.generate_quad("=", item_to_return, "RETURN QUAD TO EQUAL TO GLOBAL ADDR", function_global_address)  # TODO REMOVE 3rd VAL
        quads.append(equal_global_quad)
        temporal_quad = quad.generate_quad("RETURN", None, None, function_global_address)
        quads.append(temporal_quad)


        # Parche Guadalupano Milagroso




    """
    global pvar, function_calls
    return_type = fD.function_table[current_scope].return_type   # Ver el tipo de retorno de la funcion
    if return_type == "void":
        new_quad = quad.generate_quad("RETURN", None, None, None)
        quads.append(new_quad)
    else:
        if type(pvar) == int:
            item_to_return = fD.get_constant(pvar)
        elif type(pvar) == float:
            item_to_return = fD.get_constant(pvar)
        else:
            item_to_return = fD.get_variable_address(current_scope, pvar)
        global_address = fD.function_table["global"].add_variable("RET" + str(len(quads)), return_type) ## caso void? Generar direccion en momoria global donde guardaremos resultado
        new_quad = quad.generate_quad("=", item_to_return, None, global_address)
        quads.append(new_quad)
        print("QUAD ADDED FOR RETURN ")
        new_quad.print_quad()
        print("GLOBAL ADDR ", str(global_address))
        stackO.push(global_address)
        print("O STACK")
        stackO.show_all()
        stack_type.push("int")  ## TODO forzado a int
        new_quad = quad.generate_quad("RETURN", None, None, global_address)
        quads.append(new_quad)
    """




    """
    return_type = fD.function_table[current_scope].return_type   # Ver el tipo de retorno de la funcion
    if return_type == "void":
        new_quad = quad.generate_quad("RETURN", None, None, None)
        quads.append(new_quad)
    else:
        if type(pvar) == int:
            item_to_return = fD.get_constant(pvar)
        elif type(pvar) == float:
            item_to_return = fD.get_constant(pvar)
        else:
            item_to_return = fD.get_variable_address(current_scope, pvar)
        print("CURRENT SCOPE ", return_type)
        address = fD.function_table[current_scope].add_variable(current_scope, return_type) ## caso void? Generar direccion en momoria global donde guardaremos resultado
        print("Will return from scopee " + current_scope + " to scope " + last_scope + " with addr " + str(address))
        if address != "":
            # Case of no return (mostly for main)
            new_quad = quad.generate_quad("RETURN", item_to_return, None, address)
            stackO.push(address)
            print(str(address) + str(" aaaaaa"))
            stack_type.push(address)
        else:
            new_quad = quad.generate_quad("RETURN", item_to_return, None, None)
        quads.append(new_quad)
    """



def p_save_pvar_int(p):
    """save_pvar_int : """
    global pvar
    pvar = int(p[-1])


def p_save_pvar_float(p):
    """save_pvar_float : """
    global pvar
    pvar = float(p[-1])


def p_save_pvar_var(p):
    """save_pvar_var : """
    global pvar
    pvar = p[-1]
    #print("AAAAA",p[-3])


#############################
########## ARRAYS ###########
#############################
def p_set_array(p):
    """set_array : """
    global id_array
    if p[-3] is None:
        return
    id_array = p[-3]
    fD.function_table[current_scope].set_array(id_array)

def p_set_dim_and_r(p):
    """set_dim_and_r : """
    global dim, r
    dim = 1
    r = 1

def p_set_limits(p):
    """set_limits : """
    global r, id_array
    node = NodeArray()
    node.lim_inf = 0
    node.lim_sup = int(p[-1]) - 1
    r = (node.lim_sup - node.lim_inf + 1) * r
    fD.function_table[current_scope].add_node(id_array, node)

def p_add_dim(p):
    """add_dim : """
    global dim, id_array
    dim += 1
    next_node = NodeArray()
    last_node = fD.function_table[current_scope].get_last_node(id_array)
    last_node.next_node = next_node
    
def p_set_each_node(p):
    """set_each_node : """
    global dim, id_array, r, offset, size, k
    last_node = fD.function_table[current_scope].get_last_node(id_array)
    last_node.next_node = None
    node = fD.function_table[current_scope].get_first_node(id_array)
    dim = 1
    offset = 0
    size = r
    while(node.next_node is not None) :
        node.m = r / (node.lim_sup - node.lim_inf + 1)
        r = node.m
        offset = offset + node.lim_inf * node.m
        dim += 1
        node = node.next_node
    k = offset
    node.k = k

def p_set_virtual_address(p):
    """set_virtual_address : """
    global next_virtual_address, id_array, size
    next_virtual_address = fD.get_variable_address(id_array, current_scope) + size
    var_type = fD.get_var_type(id_array, current_scope)
    fD.function_table[current_scope].memory_manager.set_new_virtual_address(var_type, next_virtual_address)

def p_add_array_id(p):
    """add_array_id : """
    if fD.function_table["global"].variable_table[p[-1]].has_dimensions:
        stackO.push(p[-1])
        var_type = fD.get_var_type(p[-1], current_scope)
        stack_type.push(var_type)

def p_verify_dims(p):
    """verify_dims : """
    global dim, array_id, array_var
    array_id = stackO.pop()
    array_type = stack_type.pop()
    array_var = fD.function_table[current_scope].variable_table[array_id]
    if array_var.has_dimensions:
        dim = 1
        stack_dim.push((array_id, dim))
        poper.push("(") # FakeBottom

def p_array_quads(p):
    """array_quads : """
    global array_id, dim, node, array_var
    node = fD.function_table[current_scope].get_first_node(array_id)
    verify_quad = quad.generate_quad("VER", stackO.top(), node.lim_inf, node.lim_sup) 
    quads.append(verify_quad)

    if node.next_node is not None:
        aux = stackO.pop()
        new_temp = temp.get_temp(array_var.type)
        temporal = fD.function_table[current_scope].memory_manager.assign_new_temp()
        multiply_m_quad = quad.generate_quad("*", aux, node.m, temporal) # Sn * mn
        quads.append(multiply_m_quad)
        stackO.push(new_temp[0])

    if dim > 1:
        aux2 = stackO.pop()
        aux1 = stackO.pop()
        new_temp = temp.get_temp(array_var.type)
        temporal = fD.function_table[current_scope].memory_manager.assign_new_temp()
        add_dims_quad = quad.generate_quad("+", aux1, aux2, temporal)   # Sn * mn + Sx
        quads.append(add_dims_quad)
        stackO.push(new_temp[0])

def p_update_dim(p):
    """update_dim : """
    global dim, array_id, node
    dim += 1
    stack_dim.push((array_id, dim))
    node = node.next_node

def p_end_array_call(p):
    """end_array_call : """
    global array_var, node
    aux1 = stackO.pop()
    new_temp = temp.get_temp(array_var.type)
    temporal1 = fD.function_table[current_scope].memory_manager.assign_new_temp()
    add_offset_quad = quad.generate_quad("+", aux1, node.k, temporal1)
    quads.append(add_offset_quad)
    address_temp = temp.get_temp(array_var.type)
    temporal2 = fD.function_table[current_scope].memory_manager.assign_new_temp()
    add_base_address_quad = quad.generate_quad("+", temporal1, fD.get_variable_address(array_id, current_scope), temporal2)
    quads.append(add_base_address_quad)
    stackO.push(temporal2)
    poper.pop()

###########################
######## CLASSES ##########
###########################

def p_declare_class(p):
    """declare_class :"""
    pass


def p_declare_class_attribute(p):
    """declare_class_attribute :"""
    pass


def p_declare_class_method(p):
    """declare_class_method :"""
    pass

#######################
######## EOF ##########
#######################

def p_end_of_file(p):
    """end_of_file :"""
    quads.append(quad.generate_quad("EOF", None, None, None))


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


parser = yacc.yacc()
#parser = yacc.yacc(debug=True)

r = None
try:
    f = open("test15.mog", 'r')
    r = f.read()
    f.close()
except FileNotFoundError:
    error("No hay archivo para probar")

parser.parse(r, debug=False)
#parser.parse(r)
print("")
print("")
print("")
print("")
print("Código Aceptado")

print("====================================")
for quad in quads:
    quad.print_quad()
print("====================================")
#  Prepare to pass code to virtual machine

#vm.start_virtual_machine(fD, quads)

#print(vars(fD.function_table["global"].variable_table["A"]))

#  TODO implement warning when a variable is unused.
#  TODO implement warning when function is unused.


"""
NOTAS

A) El problewma pasa al retornar y asignar variable a llamada el de ;;
B) No podemos hacer operaciones como a = _local() + 1;;

instr void local2()
{
    var int a, b, c;
    a = 3;
    output -> "Should output 3";
    output -> a;
    return 0;
}
"""
