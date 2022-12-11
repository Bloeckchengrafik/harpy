import ast
from harpy.typechecker import TypeChecker


code = """
a = 1
"""

transformable = ast.parse(code)
tc = TypeChecker(transformable, {
    "filename": "testfiles/type_checker/typechecker_test_basic2.py/code",
    "code": code
})

tc.check()

assert len(tc.errors) == 0
assert len(tc.warnings) == 1
