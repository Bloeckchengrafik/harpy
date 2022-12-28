import ast
from datetime import datetime

from harpy.errors.CompileError import CompileError
from harpy.rt.platforms import PLATFORMS
from harpy.typechecker.check import get_resulting_type

NEW_LINE = "\n"


class Compiler:
    """The Harpy compiler."""

    def __init__(self, source, tree, platform) -> None:
        """Initialize the compiler."""
        self.source = source
        self.tree = tree
        self.namespace = {}
        self.result = []
        self.rt = []
        self.rt_header = f"""
#pragma once
            
/*
 * This file is automatically generated by the Harpy compiler.
 * Do not edit this file.
 *
 * Generated on {datetime.now()}
 */

"""
        self.rt_source = ""
        self.platform = PLATFORMS[platform]
        self.global_rt = self.platform.get_global_rt()
        self.optable = self.platform.get_optable()

    def compile_program(self):
        """Compile the entire program."""

        self.result.append("#include \"rt.h\"")
        self.result.append("")
        self.result.append("int main(int argc, char *argv[]) {")
        self.compile(indentation=1)
        self.result.append("}")

        self.build_rt()

    def compile(self, indentation=0):
        """Compile the given AST into c++."""
        body: list[ast.Expr] = self.tree.body
        self.result.extend(self.compile_expressions(body, indentation))

    def needs_semicolon(self, value):
        return not (value.endswith("{") or value.endswith("}") or value.endswith(";") or len(value.strip()) == 0)

    def compile_expressions(self, value: list[ast.Expr], indentation=0):
        result = []
        for expr in value:
            frag = self.compile_fragment(expr)
            if len(frag.split("\n")) == 1:
                result.append("    " * indentation + frag + (";" if self.needs_semicolon(frag) else ""))
            else:
                split = frag.split("\n")
                for line in split:
                    result.append("    " * indentation + line + (";" if self.needs_semicolon(line) else ""))

        return result

    def build_rt(self):
        """Build the runtime."""
        self.rt = list(set(self.rt))
        for dep in self.rt:
            self.rt_header += "// BEGIN " + dep.__class__.__name__ + "\n"
            self.rt_header += dep.hpp() + "\n"
            self.rt_header += "// END " + dep.__class__.__name__ + "\n"

            self.rt_source += "// BEGIN " + dep.__class__.__name__ + "\n"
            self.rt_source += dep.cpp() + "\n"
            self.rt_source += "// END " + dep.__class__.__name__ + "\n"

    def compile_fragment(self, value):
        """Compile a fragment."""
        if isinstance(value, ast.Str):
            return self.compile_str(value)
        elif isinstance(value, ast.Call):
            return self.compile_call(value)
        elif isinstance(value, ast.Assign):
            return self.compile_assignment(value)
        elif isinstance(value, ast.Constant):
            return self.compile_constant(value)
        elif isinstance(value, ast.BinOp):
            return self.compile_binary_operation(value)
        elif isinstance(value, ast.Expr):
            return self.compile_fragment(value.value)
        elif isinstance(value, ast.Name):
            return value.id
        elif isinstance(value, ast.If):
            return self.compile_if(value)
        elif isinstance(value, ast.Pass):
            return ""
        elif isinstance(value, ast.Compare):
            return self.compile_compare(value)
        elif isinstance(value, list):
            return self.compile_expressions(value, 1)
        else:
            raise TypeError(f"Unexpected AST node: {value}")

    def compile_constant(self, value: ast.Constant):
        return f"{value.value}"

    def compile_str(self, value: ast.Str):
        # Escape the string
        unescaped = value.s
        escaped = unescaped.replace('"', '\\"')
        return f'"{escaped}"'

    def compile_call(self, value: ast.Call):
        args = value.args
        compiled_args = []
        for arg in args:
            compiled_args.append(self.compile_fragment(arg))

        # TODO: Check if the function is a named function
        # noinspection PyUnresolvedReferences
        function_id = value.func.id
        # TODO: Shadowing

        if self.global_rt.get(function_id) is None:
            raise NameError(f"Name '{function_id}' is not defined")

        rt = self.global_rt[function_id]

        for dep in rt.depends():
            if dep not in self.rt:
                self.rt.append(dep)

        self.rt.append(rt)

        return f"{function_id}({', '.join(compiled_args)})"

    def compile_binary_operation(self, value: ast.BinOp):
        return f"{self.compile_fragment(value.left)} " \
               f"{self.optable[value.op.__class__]} {self.compile_fragment(value.right)}"

    def compile_assignment(self, value: ast.Assign):
        target = value.targets[0]
        if not isinstance(target, ast.Name):
            raise TypeError(f"Unexpected AST node: {target}")

        if self.namespace.get(target.id) is None:
            self.namespace[target.id] = get_resulting_type(value.value)
            return f"auto {target.id} = {self.compile_fragment(value.value)}"
        elif self.namespace[target.id] != get_resulting_type(value.value):
            raise CompileError(
                f"Cannot assign {get_resulting_type(value.value)} to {self.namespace[target.id]}",
                "<input>",
                value.lineno,
                value.col_offset,
                self.source
            )

        return f"{target.id} = {self.compile_fragment(value.value)}"

    def compile_if(self, value: ast.If):
        return \
            f"\nif ({self.compile_fragment(value.test)}) {{\n{NEW_LINE.join(self.compile_fragment(value.body))}\n}}\n"

    def compile_compare(self, value: ast.Compare):
        return f"{self.compile_fragment(value.left)} " \
               f"{self.optable[value.ops[0].__class__]} {self.compile_fragment(value.comparators[0])}"


def run_compile(source, tree, platform="cpp_std") -> Compiler:
    """Compile the given AST into c++."""
    compiler = Compiler(source, tree, platform)
    compiler.compile_program()
    return compiler
