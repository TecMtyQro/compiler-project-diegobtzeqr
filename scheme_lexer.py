# Import required libraries
import ply.lex as lex
import sys

# Create a list of reserved words.
reserved = {
    'if' : 'IF',
    'cond' : 'COND',
    'else' : 'ELSE',
    'case' : 'CASE',
    'lambda' : 'LAMBDA',
    'define' : 'DEFINE',
    'and' : 'AND',
    'or' : 'OR',
    'do' : 'DO',
    'cons' : 'CONS',
    'cdr' : 'CDR',
    'car' : 'CAR',
    'last' : 'LAST',
    'list' : 'LIST',
    'remainder' : 'REMAINDER',
    'log' : 'LOG',
    }

# Define tokens and add the reserved words as a list.
tokens = [
    'ID',
    'ADD',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'GREATER',
    'LESS',
    'GREATER_EQUAL',
    'LESS_EQUAL',
    'OPEN_PAR',
    'CLOSE_PAR',
    'OPEN_BRA',
    'CLOSE_BRA',
    'OPEN_KEY',
    'CLOSE_KEY',
    'COMMA',
    'TRUE',
    'FALSE',
    'SPACE',
    'NEW_LINE',
    'COMMENT',
    'COM_BLOCK',
    'INT',
    'FLOAT',
    'EQQUES',
    'NEQQUES',
    'CHARACTER',
    'STRING',
    ] + list(reserved.values())

# Define all the token specifications in order of importance (usually the length of the token).
t_ignore_COM_BLOCK = r'\#\|(.|\n|\t)*\|\#'

t_ADD = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_GREATER_EQUAL = r'\>\='
t_GREATER = r'\>'
t_LESS_EQUAL = r'\<\='
t_LESS = r'\<'
t_OPEN_PAR = r'\('
t_CLOSE_PAR = r'\)'
t_OPEN_BRA = r'\['
t_CLOSE_BRA = r'\]'
t_OPEN_KEY = r'\{'
t_CLOSE_KEY = r'\}'
t_COMMA = r'\,'
t_TRUE = r'\#t'
t_FALSE = r'\#f'
t_NEQQUES = r'NEQ\?'
t_EQQUES = r'EQ\?'
t_CHARACTER = r'\'[a-zA-Z]\''
#t_STRING = r'\".*\"'
t_STRING = r'\"[^"]*\"'

# Ignore elements that are goint to be in the code but aren't required.
t_ignore_SPACE = r'\ '
t_ignore_TAB = '\\t'
t_ignore_ENTER = '\\n'
t_ignore_COMMENT = r'\;.*'

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
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

# Create lexer.
lexer = lex.lex()

lexer.input("'a' \"b\" cond \"Simple \tsentence with issues\" if\tIF cond else case lambda\ndefine and or do cons cdr car#|Bloque de comentarios\nIgnorame pls\tsi eres tan amable\n|#last list remainder log id id1 id2 id_ id_2_3_4 id_test_3 iDF id_Fg4_5f +-/*;Comentario, ignorame pls\n>=><=<()[]{},#t #f EQ? NEQ?")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
