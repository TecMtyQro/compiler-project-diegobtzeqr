# Import required libraries
import ply.lex as lex
import ply.yacc as yacc
import sys

# Create a list of reserved words.
reserved = {
    'if' : 'IF',
    'cond' : 'COND',
    'else' : 'ELSE',
    'define' : 'DEFINE',
    'do' : 'DO',
    'cons' : 'CONS',
    'cdr' : 'CDR',
    'car' : 'CAR',
    'last' : 'LAST',
    'remainder' : 'REMAINDER',
    'read' : 'READ',
    'display' : 'DISPLAY',
    }

# Define tokens and add the reserved words as a list.
tokens = [
    'EQQUES',
    'NEQQUES',
    'ID',
    'ADD',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQUALS',
    'GREATER',
    'LESS',
    'GREATER_EQUAL',
    'LESS_EQUAL',
    'OPEN_PAR',
    'CLOSE_PAR',
    'OPEN_BRA',
    'CLOSE_BRA',
    'TRUE',
    'FALSE',
    'SPACE',
    'NEW_LINE',
    'COMMENT',
    'COM_BLOCK',
    'INT',
    'FLOAT',
    'CHARACTER',
    'STRING',
    'EMPTY',
    ] + list(reserved.values())

# Define all the token specifications in order of importance (usually the length of the token).
t_ignore_COM_BLOCK = r'\#\|(.|\n|\t)*\|\#'

t_ADD = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_GREATER_EQUAL = r'\>\='
t_GREATER = r'\>'
t_LESS_EQUAL = r'\<\='
t_LESS = r'\<'
t_OPEN_PAR = r'\('
t_CLOSE_PAR = r'\)'
t_OPEN_BRA = r'\['
t_CLOSE_BRA = r'\]'
t_TRUE = r'\#t'
t_FALSE = r'\#f'
t_CHARACTER = r'\'[^\']+\''
t_STRING = r'\"[^"]*\"'
#t_EMPTY = r'\'\(\)'

# Ignore elements that are goint to be in the code but aren't required.
t_ignore_SPACE = r'\ '
t_ignore_TAB = '\\t'
t_ignore_ENTER = '\\n'
t_ignore_COMMENT = r'\;.*'

def t_EMPTY(t):
    r'\'\(\)'
    return t

def t_EQQUES(t):
    r'eq\?'
    return t

def t_NEQQUES(t):
    r'neq\?'
    return t

# Define a regular expression to detect float numbers, located above the integer identifier to prioritize it.
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Define a regular expression to detect itneger numbers.
def t_INT(t):
     r'\d+'
     t.value = int(t.value)
     return t

# Define a regular expression to detect identifiers.
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')
     return t

# Define the error method for invalid characters.
def t_error(t):
    t.type = "ERROR"
    print("ERROR: Illegal character '%s'" % t.value[0])
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

# Create lexer.
lexer = lex.lex()

precedence = (
    )

def p_program(p):
    'program : form'
    #return p
    print(p[1])

def p_form_a(p):
    '''
    form : definition
         | expression
    '''
    p[0] = p[1]

def p_form_b(p):
    'form : definition definition'
    p[0] = (p[1], p[2])

# Se acumulan los aprentesis? Creo que si, pero a ver que pasa
def p_definition(p):
    'definition : OPEN_PAR DEFINE ID body CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_body_exp(p):
    '''
    body : expression
         | definition
    '''
    p[0] = p[1]

def p_expression(p):
    '''
    expression : constant
               | if_expression
               | do_expression
               | cond_expression
               | operation
               | ID
               | read
               | display
               | cons
               | list_manip
    '''
    p[0] = p[1]

def p_if_expression_a(p):
    'if_expression : OPEN_PAR IF comparison_expression expression CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_if_expression_b(p):
    'if_expression : OPEN_PAR IF comparison_expression expression expression CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_cond_expression_a(p):
    'cond_expression : OPEN_PAR COND OPEN_BRA comparison_expression expression CLOSE_BRA CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_cond_expression_b(p):
    'cond_expression : OPEN_PAR COND OPEN_BRA comparison_expression expression CLOSE_BRA OPEN_BRA ELSE expression CLOSE_BRA CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])

def p_do_expression(p):
    'do_expression : OPEN_PAR DO do_condition comparison_expression expression CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_do_condition(p):
    'do_condition : OPEN_PAR ID constant operation CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_operation(p):
    'operation : OPEN_PAR symbol expression expression CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_comparison_expression(p):
    'comparison_expression : OPEN_PAR comparison expression expression CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_read(p):
    'read : OPEN_PAR READ CLOSE_PAR'
    p[0] = (p[1], p[2], p[3])

def p_display(p):
    'display : OPEN_PAR DISPLAY expression CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4])

def p_cons(p):
    'cons : OPEN_PAR CONS constant list_expression CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_list_manip(p):
    'list_manip : OPEN_PAR list_op list CLOSE_PAR'
    p[0] = (p[1], p[2], p[3], p[4])

def p_list_expression(p):
    '''
    list_expression : list
                    | constant
    '''
    p[0] = p[1]

def p_list_op(p):
    '''
    list_op : CDR
            | CAR
            | LAST
    '''
    p[0] = p[1]

def p_list(p):
    '''
    list : cons
         | EMPTY
         | ID
    '''
    p[0] = p[1]

def p_symbol(p):
    '''
    symbol : comparison
           | boolean
           | ADD
           | MINUS
           | DIVIDE
           | MULTIPLY
           | REMAINDER
    '''
    p[0] = p[1]

def p_boolean(p):
    '''
    boolean : TRUE
            | FALSE
    '''
    p[0] = p[1]

def p_comparison(p):
    '''
    comparison : EQQUES
               | NEQQUES
               | EQUALS
               | GREATER
               | LESS
               | GREATER_EQUAL
               | LESS_EQUAL
    '''
    p[0] = p[1]

def p_constant(p):
    '''
    constant : INT
             | FLOAT
             | CHARACTER
             | STRING
    '''
    p[0] = p[1]

def p_error(t):
    print("Sintax error")
    sys.exit()
    '''
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error")
    #sys.exit()
    '''

parser = yacc.yacc(method="SLR")
while True:
    try:
        s = input('>>')
    except EOFError:
        break
    parser.parse(s)
