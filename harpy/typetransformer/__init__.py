import ast


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

        return node

    def visit_Attribute(self, node):
        return node
