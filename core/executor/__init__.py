from core.interpreter import Interpreter, Context, SymbolTable
from core.lexer import Lexer
from core.parser import Parser


global_symbol_table = SymbolTable()

def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.parse()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    context = Context("<shell>")
    context.symbol_table = global_symbol_table
    interpreter = Interpreter()
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
