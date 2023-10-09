from core.utils import string_with_arrows


class Error:
    def __init__(self, pos_start, pos_end, key, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.key = key
        self.details = details

    def __str__(self):
        result = f"{self.key}: {self.details}"
        if self.pos_start == self.pos_end:
            result += f"\n... at {self.pos_start.filename}, {str(self.pos_start)}"
        else:
            result += f"\n... at {self.pos_start.filename}, ({str(self.pos_start)}) to ({str(self.pos_end)})"
        result += '\n\n' + string_with_arrows(self.pos_start.filetext, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "IllegalCharError", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "InvalidSyntaxError", details)


class RuntimeError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "RuntimeError", details)