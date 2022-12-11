import ast
from rich import print

from harpy import create_error_message, print_error


class TypeTransformer(ast.NodeTransformer):
    def __init__(self, code, filename="<unknown>"):
        self.code = code
        self.filename = filename

    def visit_Name(self, node):
        return node

    def visit_FunctionDef(self, node):
        # Infer type of return value if not specified
        if node.returns is None:
            node.returns = ast.Name(id="None", ctx=ast.Load())
            print("Inferred return type of function to be None")
        else:
            print("Return type specified: ", node.returns.__dict__)

        # Force-Check if function returns a value other than the declared type
        # node.returns.id does not work because of the way ast works with types
        # So we need to analyze the function body
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                print("Return statement found: ", stmt.__dict__)
                if isinstance(stmt.value, ast.Name):
                    print("Return value is a name: ", stmt.value.__dict__)
                    print("Original return type: ", node.returns.__dict__)

                    print_error(create_error_message(
                        "Return value does not match declared return type",
                        self.filename,
                        stmt.lineno,
                        stmt.col_offset,
                        stmt.end_col_offset,
                        self.code.split("\n")[stmt.lineno-1],
                    ))
        return node

    def visit_Attribute(self, node):
        return node
