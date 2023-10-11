import string

from core.classes.errors import *

# consts

digits = "0123456789"
letters = string.ascii_letters
letters_digits = letters + digits
var_characters = "_"

keywords_list = [
    "var",
    "const",
    "and",
    "or",
    "xor",
    "not"
]

# position class

class Position:
    def __init__(self, index, line, column, filename, filetext):
        self.column = column
        self.line = line
        self.index = index
        self.filename = filename
        self.filetext = filetext

    def advance(self, current_char=None):
        self.index += 1
        self.column += 1

        if current_char == "\n":
            self.line += 1
            self.column = 0

    def __str__(self):
        return f"line {self.line + 1}, column {self.column + 1}"

    def copy(self):
        return Position(self.index, self.line, self.column, self.filename, self.filetext)


# token class

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return self.type

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def set_post(self, value=None, pos_start=None, pos_end=None):
        if value is None:
            value = self.value
        if pos_start is None:
            pos_start = self.pos_start
        if pos_end is None:
            try:
                pos_end = self.pos_end
            except:
                pos_end = pos_start.copy().advance()
        return Token(self.type, value, pos_start, pos_end)


token_list = {
    "plus": Token("plus"),
    "minus": Token("minus"),

    "div": Token("div"),
    "mul": Token("mul"),
    "pow": Token("pow"),

    "int": Token("int"),
    "float": Token("float"),

    "paren_l": Token("paren_l"),
    "paren_r": Token("paren_r"),

    "keyword": Token("keyword"),        # VAR, FUNC [eventually], stuff like that
    "identifier": Token("identifier"),
    "equals": Token("equals"),          # x = y

    "eq": Token("eq"),                  # x == y
    "neq": Token("neq"),                # x != y or x ~= y [lua compat]
    "lt": Token("lt"),                  # x <  y
    "gt": Token("gt"),                  # x >  y
    "lte": Token("lte"),                # x <= y
    "gte": Token("gte"),                # x >= y

    "eof": Token("eof"),
}


# lexer class itself

class Lexer:
    def __init__(self, filename, text):
        self.filename = filename
        self.tokens = None
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)
        self.current_char = None

    def __str__(self):
        return (f"""text:
{self.text}
pos: {self.pos}
char: {self.current_char}""")

    def advance(self):
        """
        Advance into the next character. Should only be used by parser
        :return:
        """
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def parse(self):
        """
        Turns `self.text` into a `list` of `Tokens`.
        :return: a list of Tokens
        """
        tokens = []
        self.advance()
        while self.current_char is not None:
            while self.current_char in " \t":
                self.advance()  # ignore
            match self.current_char:
                # simple tokens
                case "+":
                    tokens.append(token_list["plus"].set_post(pos_start=self.pos))
                    self.advance()
                case "-":
                    tokens.append(token_list["minus"].set_post(pos_start=self.pos))
                    self.advance()
                case "*":
                    tokens.append(token_list["mul"].set_post(pos_start=self.pos))
                    self.advance()
                case "/":
                    tokens.append(token_list["div"].set_post(pos_start=self.pos))
                    self.advance()
                case "^":
                    tokens.append(token_list["pow"].set_post(pos_start=self.pos))
                    self.advance()
                case "(":
                    tokens.append(token_list["paren_l"].set_post(pos_start=self.pos))
                    self.advance()
                case ")":
                    tokens.append(token_list["paren_r"].set_post(pos_start=self.pos))
                    self.advance()
                case "~", "!":
                    token, error = self.make_not_equals()
                    if error:
                        return [], error
                    tokens.append(token)
                case "=":
                    token, error = self.make_equals()
                    if error:
                        return [], error
                    tokens.append(token)
                case ">":
                    token, error = self.make_greater_than()
                    if error:
                        return [], error
                    tokens.append(token)
                case "<":
                    token, error = self.make_less_than()
                    if error:
                        return [], error
                    tokens.append(token)
                case _:
                    # complex tokens [numbers and such]
                    if self.current_char in letters + var_characters:
                        tokens.append(self.make_identifier())
                    elif self.current_char in digits:
                        tokens.append(self.make_numeric())
                    else:
                        pos_start = self.pos.copy()
                        err_char = self.current_char
                        self.advance()
                        return [], IllegalCharError(pos_start, pos_start, f"character not recognized: '{err_char}'")
        tokens.append(token_list["eof"].set_post(pos_start=self.pos))
        return tokens, []

    def make_numeric(self):
        num_string = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in digits + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break  # TODO: error
                dot_count += 1
                num_string += "."
            else:
                num_string += self.current_char
            self.advance()
        if dot_count == 0:
            return token_list["int"].set_post(value=int(num_string), pos_start=pos_start, pos_end=self.pos)
        else:
            return token_list["float"].set_post(value=float(num_string), pos_start=pos_start, pos_end=self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in letters_digits + var_characters:
            id_str += self.current_char
            self.advance()

        token_type = token_list["keyword"].type if id_str in keywords_list else token_list["identifier"].type
        return Token(token_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy() # char already a "~" or "!" so we're fine
        self.advance()

        if self.current_char == "=":
            self.advance()
            return token_list["neq"].set_post(pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "equals sign expected after '!' or '~'")

    def make_equals(self):
        pos_start = self.pos.copy()  # char already a "=" so we're fine
        self.advance()
        token = token_list["equals"]

        if self.current_char == '=':
            self.advance()
            token = token_list["eq"]

        return token.set_post(pos_start=pos_start, pos_end=self.pos), None

    def make_less_than(self):
        pos_start = self.pos.copy() # char already a "=" so we're fine
        self.advance()
        token = token_list["lt"]

        if self.current_char == '=':
            self.advance()
            token = token_list["lte"]

        return token.set_post(pos_start=pos_start, pos_end=self.pos), None

    def make_greater_than(self):
        pos_start = self.pos.copy() # char already a "=" so we're fine
        self.advance()
        token = token_list["gt"]

        if self.current_char == '=':
            self.advance()
            token = token_list["gte"]

        return token.set_post(pos_start=pos_start, pos_end=self.pos), None