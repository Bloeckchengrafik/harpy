from harpy import create_error_message


class CompileError(Exception):
    def __init__(self, message, filename, lineno, column, src):
        self.message = message
        self.filename = filename
        self.lineno = lineno
        self.column = column
        self.src = src.splitlines()[lineno - 1]

    def __str__(self):
        return create_error_message(self.message, self.filename, self.lineno, self.column, self.src)
