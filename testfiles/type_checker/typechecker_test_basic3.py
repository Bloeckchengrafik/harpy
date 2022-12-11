import ast
from harpy.typechecker import TypeChecker


code = """
def f(x: int)->int:
    return x
    
def g(x):
    return f(x)
    
if __name__ == "__main__":
    print(g(1))
"""

ast = ast.parse(code)
tc = TypeChecker(ast, {
    "filename": "testfiles/type_checker/typechecker_test_basic3.py/code",
    "code": code
})

tc.check()

assert len(tc.errors) == 1
assert len(tc.warnings) == 1
