import ast

from harpy.compiler import Compiler


class Harpy:
    def __init__(self):
        self.source = ""
        self.main = ""
        self.rt = ""
        self.rt_header = ""

    def load(self, filename):
        """Load the given file."""
        with open(filename, "r") as f:
            self.source = f.read()

    def compile(self, platform):
        """Compile the loaded source."""
        tree = ast.parse(self.source)
        compiler = Compiler(self.source, tree, platform)
        compiler.compile_program()
        self.main = "\n".join(compiler.result)
        self.rt = compiler.rt_source
        self.rt_header = compiler.rt_header
