from core.classes.number import FuseNumber
from core.lexer import token_list
from core.classes.errors import *

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

class RuntimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        # should be like "visit_BinaryOpNode"
        method = getattr(self, method_name, self.no_visit_method)  # is this cursed? yes. however, fuck you.
        return method(node, context)

    def no_visit_method(self, node, context):  # default if there isn't a special method
        raise Exception(f"no visit method for {type(node).__name__}")

    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
           FuseNumber(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinaryOpNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        right = res.register(self.visit(node.right_node, context))

        if node.op_token.type == token_list["plus"].type:
            result, error = left.add(right)
        if node.op_token.type == token_list["minus"].type:
            result, error = left.sub(right)
        if node.op_token.type == token_list["div"].type:
            result, error = left.divide(right)
        if node.op_token.type == token_list["mul"].type:
            result, error = left.multiply(right)
        if node.op_token.type == token_list["pow"].type:
            result, error = left.power(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        result = RuntimeResult()
        number = result.register(self.visit(node.node, context))  # this is the child node of the unary op [i.e. the 4 in -4]

        if node.op_token.type == token_list["minus"].type:
            number, error = number.multiply(FuseNumber(-1))

        if error:
            return result.failure(error)
        else:
            return result.success(number.set_pos(node.pos_start, node.pos_end))
