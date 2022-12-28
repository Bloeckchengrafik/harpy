import ast
from harpy.typetransformer import TypeTransformer
# from rich.console import Console
# from rich.syntax import Syntax

code = """
def f(x: int) -> None:
    return x

def g(x: int):
    return f(x)

if __name__ == "__main__":
    print(g(1))
"""

code_ast = ast.parse(code)

tc = TypeTransformer(code)
code_ast = tc.visit(code_ast)

# syntax = Syntax(ast.unparse(code_ast), "python", theme="nord", line_numbers=True)
# console = Console()
# console.print(syntax)
