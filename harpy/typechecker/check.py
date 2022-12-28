import ast


def get_resulting_type(node) -> str:
    if isinstance(node, ast.Str):
        return 'str'
    if isinstance(node, ast.Num):
        return 'int'
    elif isinstance(node, ast.Call):
        return 'auto'
    elif isinstance(node, ast.BinOp):
        node: ast.BinOp
        return get_resulting_type(node.left)

    raise TypeError(f"Unexpected AST node: {node}")
