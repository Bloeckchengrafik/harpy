import ast

from harpy import create_error_message


class ASTWalkerAndTypeChecker(ast.NodeVisitor):
    def __init__(self, filename: str, source: str):
        self.errors = []
        self.warnings = []
        self.filename = filename
        self.source = source

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.returns is None:
            self.warnings.append(create_error_message(
                f"Function {node.name} does not have a return type annotation, assuming it returns None",
                self.filename,
                node.lineno,
                node.col_offset,
                node.end_col_offset,
                self.source.splitlines()[node.lineno - 1]
            ))

            node.returns = ast.Name(id="None", ctx=ast.Load())

        for arg in node.args.args:
            if arg.annotation is None:
                self.errors.append(create_error_message(
                    f"Argument {arg.arg} does not have a type annotation",
                    self.filename,
                    arg.lineno,
                    arg.col_offset,
                    node.end_col_offset,
                    self.source.splitlines()[arg.lineno - 1]
                ))

        self.generic_visit(node)

    def visit_Assign(self, node):
        # Infer type of variable
        if isinstance(node.value, ast.Num):
            node.type = "int"
            self.warnings.append(create_error_message(
                f"Variable {node.targets[0].id} is inferred to be of type {node.type}",
                self.filename,
                node.lineno,
                node.col_offset,
                node.end_col_offset,
                self.source.splitlines()[node.lineno - 1]
            ))
        elif isinstance(node.value, ast.Str):
            node.type = "str"
            self.warnings.append(create_error_message(
                f"Variable {node.targets[0].id} is inferred to be of type {node.type}",
                self.filename,
                node.lineno,
                node.col_offset,
                node.end_col_offset,
                self.source.splitlines()[node.lineno - 1]
            ))
        elif isinstance(node.value, ast.BinOp):
            node.type = "int"
            self.warnings.append(create_error_message(
                f"Variable {node.targets[0].id} is inferred to be of type {node.type}",
                self.filename,
                node.lineno,
                node.col_offset,
                node.end_col_offset,
                self.source.splitlines()[node.lineno - 1]
            ))
        else:
            self.errors.append(create_error_message(
                f"Cannot infer type of variable {node.targets[0].id}",
                self.filename,
                node.lineno,
                node.col_offset,
                node.end_col_offset,
                self.source.splitlines()[node.lineno - 1]
            ))

        self.generic_visit(node)
