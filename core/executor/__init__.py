from core.interpreter import Interpreter
from core.lexer import Lexer
from core.parser import Parser


def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.parse()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result.value, result.error
