import unittest
from core.interpreter import Interpreter, Context, SymbolTable, FuseNumber
from core.lexer import Lexer, Token, Position
from core.parser import Parser, NumberNode, BinaryOpNode, VarAssignNode

global_symbol_table = SymbolTable()


class Tests(unittest.TestCase):
    def test_math_lex(self):
        lexer = Lexer("<test>", "1+1")
        self.assertEqual("[int:1, plus, int:1, eof]", str(lexer.parse()[0]))
    def test_math_parse(self):
        parser = Parser([Token("int",value=1,pos_start=Position(1,1,1,1,1)),Token("plus",pos_start=Position(1,1,1,1,1)),Token("int",value=1,pos_start=Position(1,1,1,1,1))])
        self.assertEqual("((int:1), plus, (int:1))", str(parser.parse().node))
    def test_math_int(self):
        context = Context("<shell>")
        context.symbol_table = global_symbol_table
        out = Interpreter().visit(BinaryOpNode(NumberNode(Token("int",value=1,pos_start=Position(1,1,1,1,1))),Token("plus",pos_start=Position(1,1,1,1,1)),NumberNode(Token("int",value=1,pos_start=Position(1,1,1,1,1)))), context)
        self.assertEqual(2, out.value.value)
    def test_assign_lex(self):
        lexer = Lexer("<test>", "var a = 1+(3*2)^3")
        self.assertEqual("[keyword:var, identifier:a, equals, int:1, plus, paren_l, int:3, mul, int:2, paren_r, pow, int:3, eof]", str(lexer.parse()[0]))
    def test_assign_parse(self):
        parser = Parser([Token("keyword",value="var",pos_start=Position(1,1,1,1,1)),Token("identifier",value="a",pos_start=Position(1,1,1,1,1)),
                         Token("equals",pos_start=Position(1,1,1,1,1)),Token("int",value=1,pos_start=Position(1,1,1,1,1)),Token("plus",pos_start=Position(1,1,1,1,1)),
                         Token("paren_l",pos_start=Position(1,1,1,1,1)),Token("int",value=3,pos_start=Position(1,1,1,1,1)),Token("mul",pos_start=Position(1,1,1,1,1)),
                         Token("int",value=2,pos_start=Position(1,1,1,1,1)),Token("paren_r",pos_start=Position(1,1,1,1,1)),Token("pow",pos_start=Position(1,1,1,1,1)),
                         Token("int",value=3,pos_start=Position(1,1,1,1,1)),Token("eof",pos_start=Position(1,1,1,1,1))])
        self.assertEqual("(identifier:a, ((int:1), plus, (((int:3), mul, (int:2)), pow, (int:3))))", str(parser.parse().node))
    def test_assign_int(self):
        context = Context("<shell>")
        context.symbol_table = global_symbol_table
        out = Interpreter().visit(VarAssignNode(Token("a",pos_start=Position(1,1,1,1,1)), BinaryOpNode(NumberNode(Token("int",value=1,pos_start=Position(1,1,1,1,1))),Token("plus",pos_start=Position(1,1,1,1,1)),
                                           BinaryOpNode(BinaryOpNode(NumberNode(Token("int",value=3,pos_start=Position(1,1,1,1,1))),Token("mul",pos_start=Position(1,1,1,1,1)),NumberNode(Token("int",value=2,pos_start=Position(1,1,1,1,1)))),
                                           Token("pow",pos_start=Position(1,1,1,1,1)),NumberNode(Token("int",value=3,pos_start=Position(1,1,1,1,1)))))), context)
        self.assertEqual(217, out.value.value)

if __name__ == '__main__':
    unittest.main()