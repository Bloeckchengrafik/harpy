import optparse
import os
import shutil
from rich.console import Console
from rich.markdown import Markdown

from harpy.harpy import Harpy

console = Console()

parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="input", help="The input file")
parser.add_option("-c", "--compiler", dest="compiler", help="The compiler to use", default="g++")
parser.add_option("-o", "--output", dest="output", help="The output file", default="a.out")
parser.add_option("-r", "--run", dest="run", help="Run the program after compiling", action="store_true", default=False)
parser.add_option("-p", "--platform", dest="platform", help="Set the runtime platform", choices=["cpp_std"], default="cpp_std")

options, args = parser.parse_args()

if not options.input:
    parser.error("No input file specified")

markdown = Markdown(f"""
# 🦅 Harpy Compiler

- Input file: `{options.input}`
- Compiler: `{options.compiler}`
- Output file: `{options.output}`
- Run: `{options.run}`
- Platform: `{options.platform}`

This program is licensed under the MIT license. See LICENSE for more information.

---
""")
console.print(markdown)

harpy = Harpy()
harpy.load(options.input)
harpy.compile(options.platform)

run_dir = ".harpy"

if not os.path.exists(run_dir):
    os.mkdir(run_dir)
else:
    for f in os.listdir(run_dir):
        # Remove all directories
        if os.path.isdir(os.path.join(run_dir, f)):
            # Remove the directory and all its contents
            shutil.rmtree(os.path.join(run_dir, f))
        else:
            os.remove(os.path.join(run_dir, f))

os.chdir(run_dir)

with open("main.cpp", "w") as f:
    f.write(harpy.main)

with open("rt.h", "w") as f:
    f.write(harpy.rt_header)

with open("rt.cpp", "w") as f:
    f.write(harpy.rt)

os.system(f"{options.compiler} main.cpp rt.cpp -o ../{options.output}")

if options.run:
    os.system(f"../{options.output}")
