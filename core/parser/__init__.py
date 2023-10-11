from core.lexer import token_list
from core.classes.errors import *


class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'


class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

        self.pos_start = self.op_token.pos_start
        self.pos_end = self.node.pos_end


class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end


class VarAssignNode:
    def __init__(self, var_name_token, value_node, const=False):
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.const = const

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f"({self.op_token}, {self.node})"


# parse result


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, result):
        self.advance_count += result.advance_count
        if result.error:
            self.error = result.error
        return result.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


# parser

class Parser:
    def __init__(self, tokens):
        self.current_token = None
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != token_list["eof"].type:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected an operation"
                ))
        return res

    def atom(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (token_list["int"].type, token_list["float"].type):
            result.register_advancement()
            self.advance()
            return result.success(NumberNode(token))

        if token.type == token_list["identifier"].type:
            result.register_advancement()
            self.advance()
            return result.success(VarAccessNode(token))

        elif token.type == token_list["paren_l"].type:  # parenthesis check like 1*(2+5)
            result.register_advancement()
            self.advance()
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type == token_list["paren_r"].type:
                result.register_advancement()
                self.advance()
                return result.success(expression)
            else:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected closing parenthesis"
                ))

        return result.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected an integer, float, identifier, '-', or parenthesis"
        ))

    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (token_list["plus"].type, token_list["minus"].type):
            result.register_advancement()
            self.advance()
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOpNode(token, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.atom, (token_list["pow"].type,), self.factor)

    def term(self):
        return self.bin_op(self.factor, (token_list["mul"].type, token_list["div"].type))

    def arith_expr(self):
        return self.bin_op(self.term, (token_list["plus"].type, token_list["minus"].type))

    def comp_expr(self):
        result = ParseResult()

        if self.current_token.matches(token_list["keyword"].type, "not"):
            op_token = self.current_token
            result.register_advancement()
            self.advance()

            node = result.register(self.comp_expr())
            if result.error:
                return result
            return result.success(UnaryOpNode(op_token, node))

        node = result.register(self.bin_op(self.arith_expr, ("eq", "neq", "lt", "gt", "lte", "gte")))

        if result.error:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected an integer, float, identifier, '-', parenthesis, or 'not'"
            ))

        return result.success(node)

    def expression(self):
        result = ParseResult()
        if self.current_token.matches(token_list["keyword"].type, "var") or self.current_token.matches(token_list["keyword"].type, "const"):
            definition_token = self.current_token
            result.register_advancement()
            self.advance()

            if self.current_token.type != token_list["identifier"].type:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "Expected identifier"
                    )
                )

            var_name = self.current_token
            result.register_advancement()
            self.advance()

            if self.current_token.type != token_list["equals"].type:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "Expected '='"
                    )
                )

            result.register_advancement()
            self.advance()
            expr = result.register(self.expression())
            if result.error:
                return result
            if definition_token.matches(token_list["keyword"].type, "var"):
                return result.success(VarAssignNode(var_name, expr, const=False))
            else:
                return result.success(VarAssignNode(var_name, expr, const=True))

        node = result.register(self.bin_op(self.comp_expr, ((token_list["keyword"].type, "and"),
                                                            (token_list["keyword"].type, "or"))))

        if result.error:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected an integer, float, identifier, '-', parenthesis, 'var', or 'not'"
                )
            )

        return result.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        result = ParseResult()
        left = result.register(func_a())
        if result.error:
            return result

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op_token = self.current_token
            result.register_advancement()
            self.advance()
            right = result.register(func_b())
            if result.error:
                return result
            left = BinaryOpNode(left, op_token, right)

        return result.success(left)
