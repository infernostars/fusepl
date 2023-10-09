import resource

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

    def __repr__(self):
        return f"({self.op_token}, {self.node})"


# parse result


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, result):
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node

        return result

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
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
        if not res.error and self.current_token.type != token_list["eof"].type:            return res.failure(
            InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected an operation"
            ))
        return res

    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (token_list["plus"].type, token_list["minus"].type):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOpNode(token, factor))

        elif token.type in (token_list["int"].type, token_list["float"].type):
            result.register(self.advance())
            return result.success(NumberNode(token))

        elif token.type == token_list["paren_l"].type:  # parenthesis check like 1*(2+5)
            result.register(self.advance())
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type == token_list["paren_r"].type:
                result.register(self.advance())
                return result.success(expression)
            else:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected closing parenthesis"
                ))

        return result.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected an integer or a float"
        ))

    def term(self):
        return self.bin_op(self.factor, (token_list["mul"].type, token_list["div"].type))

    def expression(self):
        return self.bin_op(self.term, (token_list["plus"].type, token_list["minus"].type))

    def bin_op(self, func, ops):
        result = ParseResult()
        left = result.register(func())
        if result.error:
            return result

        while self.current_token.type in ops:
            op_token = self.current_token
            result.register(self.advance())
            right = result.register(func())
            if result.error: return result
            left = BinaryOpNode(left, op_token, right)

        return result.success(left)
