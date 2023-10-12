import unittest
from core.interpreter import Interpreter, Context, SymbolTable, FuseNumber
from core.lexer import Lexer, Token, Position
from core.parser import Parser, NumberNode, BinaryOpNode, VarAssignNode
from core.executor import run

global_symbol_table = SymbolTable()


class Tests(unittest.TestCase):
    def test_math_lex(self):
        lexer = Lexer("<test>", "1+1")
        self.assertEqual("[int:1, plus, int:1, eof]", str(lexer.parse()[0]))
    def test_math_lexp(self):
        lexer = Lexer("<test>", "1+1")
        parser = Parser(lexer.parse()[0])
        self.assertEqual("((int:1), plus, (int:1))", str(parser.parse().node))
    def test_math_lpi(self):
        lexer = Lexer("<test>", "1+1")
        parser = Parser(lexer.parse()[0])
        context = Context("<shell>")
        context.symbol_table = global_symbol_table
        out = Interpreter().visit(parser.parse().node, context)
        self.assertEqual(2, out.value.value)

    def test_assign_lex(self):
        lexer = Lexer("<test>", "var a = 1+(3*2)^3")
        self.assertEqual("[keyword:var, identifier:a, equals, int:1, plus, paren_l, int:3, mul, int:2, paren_r, pow, int:3, eof]", str(lexer.parse()[0]))
    def test_assign_lexp(self):
        lexer = Lexer("<test>", "var a = 1+(3*2)^3")
        parser = Parser(lexer.parse()[0])
        self.assertEqual("(identifier:a, ((int:1), plus, (((int:3), mul, (int:2)), pow, (int:3))))", str(parser.parse().node))
    def test_assign_lpi(self):
        lexer = Lexer("<test>", "var a = 1+(3*2)^3")
        parser = Parser(lexer.parse()[0])
        context = Context("<shell>")
        context.symbol_table = global_symbol_table
        out = Interpreter().visit(parser.parse().node, context)
        self.assertEqual(217, out.value.value)
    def test_if_statement(self):
        context = Context("<shell>")
        context.symbol_table = global_symbol_table
        out = run(context, "if true or false then 1000 else 2000")
        self.assertEqual(1000, out[0].value)

if __name__ == '__main__':
    unittest.main()