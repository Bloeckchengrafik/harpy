import ast
from datetime import datetime
from rich.color import Color

from harpy.compiler.CFunction import BaseCFunction
from harpy.errors.CompileError import CompileError
from harpy.rt.platforms import PLATFORMS
from harpy.typechecker.check import get_resulting_type

NEW_LINE = "\n"
LBRACE = "{"
RBRACE = "}"
HARPY_WARNING = f"""
/*
 * This file is automatically generated by the Harpy compiler.
 * Do not edit this file.
 *
 * Generated on {datetime.now()}
 */
 """


class Compiler:
    """The Harpy compiler."""

    def __init__(self, source, tree, platform) -> None:
        """Initialize the compiler."""
        self.source = source
        self.tree = tree
        self.namespace = {}
        self.result = [f"{HARPY_WARNING}\n"]
        self.function_sector: list[BaseCFunction] = []
        self.rt = []
        self.rt_header = f"#pragma once\n\n{HARPY_WARNING}\n"
        self.rt_source = f"{HARPY_WARNING}\n"
        self.platform = PLATFORMS[platform]
        self.global_rt = self.platform.get_global_rt()
        self.optable = self.platform.get_optable()

    def compile_program(self):
        """Compile the entire program."""

        self.result.append("#include \"rt.h\"")
        self.result.append("")

        self.function_sector.append(
            BaseCFunction("main", f"int main(int argc, char *argv[]) {LBRACE}{NEW_LINE}"
                                  f"{NEW_LINE.join(self.compile(indentation=1))} "
                                  f"{NEW_LINE}{RBRACE}"))

        self.build_funcs()
        self.build_rt()

    def compile(self, indentation=0):
        """Compile the given AST into c++."""
        body: list[ast.Expr] = self.tree.body
        return self.compile_expressions(body, indentation)

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

    def build_funcs(self):
        for func in self.function_sector:
            self.result.extend([
                f"// BEGIN {func.name}",
                func.cpp_src,
                f"// END {func.name}\n"
            ])

    def build_rt(self):
        """Build the runtime."""
        self.rt = list(set(self.rt))
        for dep in self.rt:
            self.rt_header += "// BEGIN " + dep.provides()[0] + "\n"
            self.rt_header += dep.hpp() + "\n"
            self.rt_header += "// END " + dep.provides()[0] + "\n"

            self.rt_source += "// BEGIN " + dep.provides()[0] + "\n"
            self.rt_source += dep.cpp() + "\n"
            self.rt_source += "// END " + dep.provides()[0] + "\n"

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
        elif isinstance(value, ast.UnaryOp):
            return self.compile_unary_op(value)
        else:
            raise TypeError(f"Unexpected AST node: ast.{value.__class__.__name__}")

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

        if not value.func.__dict__.get("id"):
            raise CompileError(
                f"Function calls must be named",
                "<input>",
                value.lineno,
                value.col_offset,
                self.source
            )

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
            raise TypeError(f"Unexpected AST node: {target.__class__.__name__}")

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

    def compile_unary_op(self, value: ast.UnaryOp):
        return f"{self.optable[value.op.__class__]}{self.compile_fragment(value.operand)}"


def run_compile(source, tree, platform="cpp_std") -> Compiler:
    """Compile the given AST into c++."""
    compiler = Compiler(source, tree, platform)
    compiler.compile_program()
    return compiler
