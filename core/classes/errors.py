from core.utils import string_with_arrows


class Error:
    def __init__(self, pos_start, pos_end, key, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.key = key
        self.details = details

    def __repr__(self):
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


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "ExpectedCharError", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "InvalidSyntaxError", details)


class FuseRuntimeError(Error):
    def __init__(self, pos_start, pos_end, details, context, key="FuseRuntimeError"):
        super().__init__(pos_start, pos_end, key, details)
        self.context = context

    def __repr__(self):
        result = self.generate_traceback()
        result += f"\n{self.key}: {self.details}"
        result += '\n\n' + string_with_arrows(self.pos_start.filetext, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        context = self.context

        while context:
            result = f"\nat {self.pos_start.filename}, line {self.pos_start.line + 1}, in {context.display_name}" + result
            pos = context.parent_entry_pos
            context = context.parent

        return "Traceback: [most recent call last]:" + result


class VariableUndefinedError(FuseRuntimeError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context, key="VariableUndefinedError")
        self.context = context


class ConstantAssignmentError(FuseRuntimeError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context, key="ConstantAssignmentError")
        self.context = context
