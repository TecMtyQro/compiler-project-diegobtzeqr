import unittest

from scheme_lexer import lexer as scheme_lexer

class LexerTest(unittest.TestCase):

    def test_one_word_comment(self):
        f = open("tests/OneWordComment.rkt", "r")
        e = open("tests/result/OneWordComment.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_one_line_comment(self):
        f = open("tests/OneLineComment.rkt", "r")
        e = open("tests/result/OneLineComment.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_constant_definition(self):
        f = open("tests/ConstantDefinition.rkt", "r")
        e = open("tests/result/ConstantDefinition.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_strings(self):
        f = open("tests/Strings.rkt", "r")
        e = open("tests/result/Strings.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_data_type(self):
        f = open("tests/DataType.rkt", "r")
        e = open("tests/result/DataType.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_loop_and_conditional(self):
        f = open("tests/LoopAndCond.rkt", "r")
        e = open("tests/result/LoopAndCond.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_input_output(self):
        f = open("tests/InputOutput.rkt", "r")
        e = open("tests/result/InputOutput.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_instruction(self):
        f = open("tests/Instruction.rkt", "r")
        e = open("tests/result/Instruction.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_error_definition(self):
        f = open("tests/ErrorDefinition.rkt", "r")
        e = open("tests/result/ErrorDefinition.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_instruction_not_allow(self):
        f = open("tests/InstructionNotAllow.rkt", "r")
        e = open("tests/result/InstructionNotAllow.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

    def test_wrong_loop(self):
        f = open("tests/WrongLoop.rkt", "r")
        e = open("tests/result/WrongLoop.txt", "w+")
        t = f.read()
        scheme_lexer.input(t)
        while True:
            tok = scheme_lexer.token()
            if not tok:
                break
            e.write(str(tok)+"\n")
            self.assertTrue(tok.type != "ERROR")
        f.close()
        e.close()

if __name__ == '__main__':
    unittest.main()
