from core.lexer import Lexer
from core.parser import Parser


def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.parse()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error
