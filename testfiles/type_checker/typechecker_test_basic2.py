import ast
from harpy.typechecker import TypeChecker


code = """
def f(x: int):
    return x
    
def g(x: int):
    return f(x)
    
if __name__ == "__main__":
    print(g(1))
"""

ast = ast.parse(code)
tc = TypeChecker(ast, {
    "filename": "testfiles/type_checker/typechecker_test_basic2.py/code",
    "code": code
})

tc.check()

assert len(tc.errors) == 0
assert len(tc.warnings) == 2
