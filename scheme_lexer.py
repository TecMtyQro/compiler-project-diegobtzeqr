import ply.lex as lex
import sys

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
    ] + list(reserved.values())

t_ignore_COM_BLOCK = r'\#\|.*\|\#'

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
t_COMMA = r'\,'
t_TRUE = r'\#\t'
t_FALSE = r'\#\f'
t_SPACE = r'\ '
t_EQQUES = r'EQ\?'
t_NEQQUES = r'NEQ\?'

t_ignore_TAB = '\\t'
t_ignore_SPACE = '\\n'
t_ignore_COMMENT = r'\;.*'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
     r'\d+'
     t.value = int(t.value)
     return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')
     return t

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lexer = lex.lex()

lexer.input("(+ 9.54 8)")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
