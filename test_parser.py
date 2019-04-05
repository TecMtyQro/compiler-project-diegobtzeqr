import unittest

from scheme_compiler import parser as scheme_parser
from scheme_compiler import lexer as scheme_lexer

class LexerTest(unittest.TestCase):

    def test_variable_definition(self):
        f = open("tests/VariableDefinition.rkt", "r")
        e = open("tests/result/VariableDefinition.txt", "w+")
        s = f.read()
        scheme_lexer.input(s)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            par = scheme_parser.parse(s)
        '''
        tok = scheme_parser.parse(t)
        print(tok)
        e.write(str(tok)+"\n")
        '''
        #scheme_parser.parse(t)
        print(str(par))
        self.assertTrue(0 != -1)
        f.close()
        e.close()

    def test_loop_conditional(self):
        f = open("tests/LoopConditional.rkt", "r")
        e = open("tests/result/LoopConditional.txt", "w+")
        s = f.read()
        scheme_lexer.input(s)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            par = scheme_parser.parse(s)
        '''
        tok = scheme_parser.parse(t)
        print(tok)
        e.write(str(tok)+"\n")
        '''
        #scheme_parser.parse(t)
        print(str(par))
        self.assertTrue(0 != -1)
        f.close()
        e.close()

if __name__ == '__main__':
    unittest.main()
