import ast


class BaseCFunction:
    def __init__(self, name, cpp_src):
        self.name = name
        self.cpp_src = cpp_src


class CFunction(BaseCFunction):
    def __init__(self, compiler, node: ast.FunctionDef):
        super().__init__("", "")
        print(node.__dict__)
