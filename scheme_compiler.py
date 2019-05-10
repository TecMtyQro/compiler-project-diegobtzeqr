# Import required libraries
import ply.lex as lex
import ply.yacc as yacc
import sys

class Element:
    def __init__(self, name, category, value, scope):
        self.name = name
        self.category = category
        self.value = value
        self.scope = scope

    def __str__(self):
        return ("Element: " + str(self.name) + ", Category: " + str(self.category) + ", Value: " + str(self.value) + ", Scope: " + str(self.scope))

elements = [ ]

class Node(object):
    # Interface for a Node of AST

    def run(self):
        # Function to run the stms of the node.
        raise NotImplementedError("Subclass must implement abstract method")

class DefinitionList(Node):
    def __init__(self, definition, definition_list = None):
        self.type = 'DEFINITION_LIST'
        self.definition = definition
        self.definition_list = definition_list

    def run(self):
        self.definition.run()
        if self.definition_list:
            self.definition_list.run()

class Number(Node):
    def __init__(self, value):
        self.type = 'NUMBER'
        self.value = value

    def run(self):
        return self.value

class Boolean(Node):
    def __init__(self, value):
        self.type = 'BOOLEAN'
        self.value = value

    def run(self):
        return True if self.value == '#t' else False

class String(Node):
    def __init__(self, value):
        self.type = 'STRING'
        self.value = value

    def run(self):
        return self.value

class Cons_List(Node):
    def __init__(self, value, lst):
        self.value = value
        self.lst = lst

    def run(self):
        if isinstance(self.value, list):
            if isinstance(self.lst, list):
                return self.value + self.list
            elif isinstance(self.lst, Cons_List):
                if not isinstance(self.lst.run(), list):
                    return self.value + [self.lst.value.run()]
                else:
                    return self.value + self.lst.value
            else:
                return self.value + [self.list]
        elif isinstance(self.lst, list):
            if isinstance(self.value, Cons_List):
                if not isinstance(self.value.run(), list):
                    return [self.value.value.run()] + self.lst
                else:
                    return self.value.value + self.lst
            else:
                return [self.value] + self.lst
        elif isinstance(self.value, Cons_List):
            if isinstance(self.lst, Cons_List):
                if not isinstance(self.value.run(), list):
                    return [self.value.value.run()] + self.lst.value
                else:
                    return self.value.value + self.lst.value
            else:
                if not isinstance(self.value.run(), list):
                    return [self.value.value.run()] + [self.lst]
                else:
                    return self.value.value + [self.lst]
        elif isinstance(self.lst, Cons_List):
            if not isinstance(self.lst.run(), list):
                return [self.value.run()] + [self.lst.value.run()]
            else:
                return [self.value.run()] + self.lst.run()
        else:
            return [self.value.run()] + [self.lst.run()]

class Op_List(Node):
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def run(self):
        if self.op == "car":
            if self.value == None:
                return '\'()'
            return self.value.value.run()
        if self.op == "cdr" or self.op == "last":
            if self.value == None:
                return '\'()'
            if isinstance(self.value, Number):
                return [self.value]
            '''
            print(str(self.value.run()) + " type: " + str(type(self.value.run())))
            
            if isinstance(self.value.run(), list):
                return self.value.run()
            else:
                return self.value.lst.run()
                '''
            return self.value.lst.run()

class Definition(Node):
    def __init__(self, name, value):
        self.type = 'DEFINITION'
        self.name = name
        self.value = value        

    def run(self):
        temp = Element(self.name, self.type, self.value.run(), "GLOBAL")
        elements.append(temp)

class Definition_ID(Node):
    def __init__(self, name, value, scope):
        self.type = 'ID'
        self.name = name
        self.value = value
        self.scope = scope

    def run(self):
        temp = Element(self.name, self.type, self.value.run(), self.scope)
        elements.append(temp)
        
class ID(Node):
    def __init__(self, name):
        self.name = name
        self.type = 'ID'        

    def run(self):
        flag = 0
        for e in elements:
            if e.name == self.name:
                aux = e
                flag = 1
        
        if flag == 1:
            return aux.value
        else:
            print("Undefined name: " + self.name)
            sys.exit()

class Operation(Node):
    def __init__(self, op, left, right):
        self.type = 'OPERATION'
        self.op = op
        self.left = left
        self.right = right

    def run(self):
        tempL = self.left
        tempR = self.right
        
        if isinstance(self.left,str):
            aux = 0
            for e in elements:
                if e.name == self.left:
                    self.left = Number(e.value)
                    aux = 1
                    break

            if aux == 0:
                print("Error: " + self.left + " not previously defined.")
                sys.exit()

        if isinstance(self.right,str):
            aux = 0
            for e in elements:
                if e.name == self.right:
                    self.right = Number(e.value)
                    aux = 1
                    break

            if aux == 0:
                print("Error: " + self.right + " not previously defined.")
                sys.exit()
            
        if  ((isinstance(self.left, Number)  or (isinstance(self.left, ID)  and (isinstance(self.left.run(), int)  or isinstance(self.left.run(), float))))
        and  (isinstance(self.right, Number) or (isinstance(self.right, ID) and (isinstance(self.right.run(), int) or isinstance(self.right.run(), float))))):
            if self.op == '+':
                temp = self.left.run() + self.right.run()
                self.left = tempL
                self.right = tempR
                return temp
            elif self.op == '-':
                temp = self.left.run() - self.right.run()
                self.left = tempL
                self.right = tempR
                return temp
            elif self.op == '*':
                temp = self.left.run() * self.right.run()
                self.left = tempL
                self.right = tempR
                return temp
            elif self.op == '/':
                temp = self.left.run() / self.right.run()
                self.left = tempL
                self.right = tempR
                return temp
            elif self.op == '/':
                temp = self.left.run() / self.right.run()
                self.left = tempL
                self.right = tempR
                return temp
            elif self.op == 'remainder':
                temp = self.left.run() % self.right.run()
                self.left = tempL
                self.right = tempR
                return temp
            else:
                print("Operand error")
                sys.exit()
        else:
            print("Error: Type Mismatch")
            sys.exit()

class Comparison(Node):
    def __init__(self, op, left, right):
        self.type = 'COMPARISON'
        self.op = op
        self.left = left
        self.right = right

    def run(self):
        tempL = self.left
        tempR = self.right

        if isinstance(self.left,str):
            aux = 0
            for e in elements:
                if e.name == self.left:
                    self.left = Number(e.value)
                    aux = 1
                    break

            if aux == 0:
                print("Error: " + self.left + " not previously defined.")
                sys.exit()

        if isinstance(self.right,str):
            aux = 0
            for e in elements:
                if e.name == self.right:
                    self.right = Number(e.value)
                    aux = 1
                    break
                
            if aux == 0:
                print("Error: " + self.right + " not previously defined.")
                sys.exit()
        if  ((isinstance(self.left, Number)  or (isinstance(self.left, ID)  and (isinstance(self.left.run(), int)  or isinstance(self.left.run(), float))))
        and  (isinstance(self.right, Number) or (isinstance(self.right, ID) and (isinstance(self.right.run(), int) or isinstance(self.right.run(), float))))):
            if self.op == '<':
                if self.left.run() < self.right.run():
                    self.left = tempL
                    self.right = tempR
                    return '#t'
                else:
                    self.left = tempL
                    self.right = tempR
                    return '#f'
            elif self.op == '>':
                if self.left.run() > self.right.run():
                    self.left = tempL
                    self.right = tempR
                    return '#t'
                else:
                    self.left = tempL
                    self.right = tempR
                    return '#f'
            elif self.op == '<=':
                if self.left.run() <= self.right.run():
                    self.left = tempL
                    self.right = tempR
                    return '#t'
                else:
                    self.left = tempL
                    self.right = tempR
                    return '#f'
            elif self.op == '>=':
                if self.left.run() >= self.right.run():
                    self.left = tempL
                    self.right = tempR
                    return '#t'
                else:
                    self.left = tempL
                    self.right = tempR
                    return '#f'
            elif self.op == 'eq?':
                if self.left.run() == self.right.run():
                    self.left = tempL
                    self.right = tempR
                    return '#t'
                else:
                    self.left = tempL
                    self.right = tempR
                    return '#f'
            elif self.op == 'neq?':
                if self.left.run() != self.right.run():
                    self.left = tempL
                    self.right = tempR
                    return '#t'
                else:
                    self.left = tempL
                    self.right = tempR
                    return '#f'
            else:
                print("Comparison Error")
                sys.exit()
        else:
            print("Error: Type Mismatch")
            sys.exit()

class Input(Node):
    def __init__(self):
        self.type = 'INPUT'

    def run(self):
        return input()

class Print(Node):
    def __init__(self, item):
        self.type = 'PRINT'
        self.item = item

    def run(self):
        for e in elements:
            if e.name == self.item:
                print(str(e.value))
                return None
        
        if isinstance(self.item, int) or isinstance(self.item, float) or isinstance(self.item, Number) or isinstance(self.item, String) or isinstance(self.item, Operation):
            print(self.item.run())
        else:
            print(String(self.item).run())

class If(Node):
    def __init__(self, condition, stmt, else_stmt = None):
        self.type = 'IF'
        self.condition = condition
        self.stmt = stmt
        self.else_stmt = else_stmt

    def run(self):
        if self.condition.run() == '#t':
            self.stmt.run()
        else:
            self.else_stmt.run()

class Do(Node):
    def __init__(self, ID, op, comp, stmt):
        self.type = 'DO'
        self.ID = ID
        self.op = op
        self.comp = comp
        self.stmt = stmt

    def run(self):
        for e in elements:
            if e.name == self.ID.name:
                break
        
        while self.comp.run() == '#t':
            res = self.stmt.run()
            for e in elements:
                if e.name == self.ID.name:
                    e.value = self.op.run()
        
        elements.remove(e)
        return res

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
    if p[1].run() != None:
        print(p[1].run())

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
    p[0] = Definition(p[3], p[4])

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
               | comparison_expression
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
    p[0] = If(p[3], p[4])

def p_if_expression_b(p):
    'if_expression : OPEN_PAR IF comparison_expression expression expression CLOSE_PAR'
    p[0] = If(p[3], p[4], p[5])

def p_cond_expression_a(p):
    'cond_expression : OPEN_PAR COND OPEN_BRA comparison_expression expression CLOSE_BRA CLOSE_PAR'
    p[0] = If(p[4], p[5])

def p_cond_expression_b(p):
    'cond_expression : OPEN_PAR COND OPEN_BRA comparison_expression expression CLOSE_BRA OPEN_BRA ELSE expression CLOSE_BRA CLOSE_PAR'
    p[0] = If(p[4], p[5], p[9])
                
def p_do_expression(p):
    'do_expression : OPEN_PAR DO id_set operation comparison_expression expression CLOSE_PAR'
    p[0] = Do(p[3], p[4], p[5], p[6])

def p_id_set(p):
    'id_set : OPEN_PAR ID constant CLOSE_PAR'
    temp = Definition_ID(p[2], p[3], "DO")
    temp.run()
    p[0] = ID(p[2])

def p_operation(p):
    'operation : OPEN_PAR symbol expression expression CLOSE_PAR'
    p[0] = Operation(p[2], p[3], p[4])

def p_comparison_expression(p):
    'comparison_expression : OPEN_PAR comparison expression expression CLOSE_PAR'
    p[0] = Comparison(p[2], p[3], p[4])

def p_read_a(p):
    'read : READ'
    p[0] = Input()

def p_read_b(p):
    'read : OPEN_PAR READ CLOSE_PAR'
    p[0] = Input()

def p_display(p):
    'display : OPEN_PAR DISPLAY expression CLOSE_PAR'
    p[0] = Print(p[3])

def p_cons(p):
    'cons : OPEN_PAR CONS constant list_expression CLOSE_PAR'
    p[0] = Cons_List(p[3], p[4])

def p_list_manip(p):
    'list_manip : OPEN_PAR list_op list CLOSE_PAR'
    p[0] = Op_List(p[2], p[3])

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
         | list_manip
         | EMPTY
         | ID
    '''
    p[0] = p[1]

def p_symbol(p):
    '''
    symbol : ADD
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
    if p[1] == '#t':
        p[0] = Boolean('#t')
    else:
        p[0] = Boolean('#f')

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
             | boolean
    '''
    if p[1] == '#t' and p[1] == '#f':
        p[0] = p[1]
    elif isinstance(p[1], int) or isinstance(p[1], float):
        p[0] = Number(p[1])
    else:
        p[0] = String(p[1])

def p_error(t):
    print("Sintax error.")
    sys.exit()

parser = yacc.yacc(method="SLR")
while True:
    try:
        s = input('>>')
    except EOFError:
        break
    parser.parse(s)
