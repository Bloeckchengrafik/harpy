from .ASTWalker import ASTWalkerAndTypeChecker

from .. import print_error, print_warning


class TypeChecker:
    def __init__(self, ast, env):
        self.ast = ast
        self.env = env
        self.walker = ASTWalkerAndTypeChecker(env["filename"], env["code"])
        self.errors = []
        self.warnings = []

    def check(self):
        self.walker.visit(self.ast)

        self.errors = self.walker.errors
        self.warnings = self.walker.warnings

        self.walker.errors = []
        self.walker.warnings = []

        return self.errors, self.warnings

    def print_errors_and_warnings(self):
        for error in self.errors:
            print_error(error)
        for warning in self.warnings:
            print_warning(warning)
