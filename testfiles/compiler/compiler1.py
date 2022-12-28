import ast

from rich.console import Console
from rich.syntax import Syntax

import harpy.compiler

code = """
print('Hello World')
"""

tree = ast.parse(code)

compiler = harpy.compiler.run_compile(code, tree)

main = "\n".join(compiler.result)
rt_header = compiler.rt_header
rt_source = compiler.rt_source

main = Syntax(main, "cpp", line_numbers=True)
rt_header = Syntax(rt_header, "cpp", line_numbers=True)
rt_source = Syntax(rt_source, "cpp", line_numbers=True)


console = Console()

console.print("[bold]main.cpp[/bold]")
console.print(main)
console.print()

console.print("[bold]harpy/rt.h[/bold]")
console.print(rt_header)
console.print()

console.print("[bold]harpy/rt.cpp[/bold]")
console.print(rt_source)
console.print()
