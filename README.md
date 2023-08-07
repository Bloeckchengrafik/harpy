# 🦅 The Harpy Python Compiler

_Harpy: A new fast and compilable pythonic scripting language_

## 📖 Table of Contents

- [📖 Table of Contents](#-table-of-contents)
- [📚 Introduction](#-introduction)
- [🖥️ Installation](#-installation)
- [🖊️ Usage](#-usage)
- [🧑 Contributing](#-contributing)
- [💼 License](#-license)

## 📚 Introduction

Harpy is a new fast and compilable way to write python code. It is a python to C++ compiler that can compile python code
to a binary that can be executed without the need of a python interpreter.

It is using the python ast module to parse the python code and then compile it to the AST. The AST is then cross
compiled to C++ and finally compiled to a binary.
This makes it possible to compile python code to a binary that can be executed without the need of a python interpreter.
Also, this form of python works on embedded systems that do not have the capability to run a full python interpreter.

### This project is still in development and is not ready for production use. 

## 🖥️ Installation

Since Harpy is still in development, it is not available on PyPI. To install Harpy, you need to clone the repository and
use `python3 -m harpy` in the current working directory to run it.

## 🖊️ Usage

If you just want to test it, install [just](https://github.com/casey/just) and run `just all` in the root directory of the
repository. This will run the tests and compile the example code found in the `test_data` directory.

Write a python script and compile it to a binary using

```bash
python3 -m harpy -i <file>.py 
```

This will create a binary file named `a.out` in the current working directory. You can run this binary using native
commands. If you want to run it directly, you can use the `-r` flag.

```bash
python3 -m harpy -i <file>.py -r
```

You can also modify the behaviour of the compiler by using the following flags:

- `-i` or `--input`: The input file
- `-c` or `--compiler`: The compiler to use. Defaults to `g++`
- `-o` or `--output`: The output file. Defaults to `a.out`
- `-r` or `--run`: Run the program after compiling. Defaults to `False`
- `-p` or `--platform`: Set the runtime platform. Defaults to `cpp_std`. This is the only platform available at the moment.

## 🧑 Contributing

I'd love to have your helping hand on Harpy! If you have any questions, feel free to open an issue. If you want to
contribute, just submit a pull request.

## 💼 License

Harpy is licensed under the MIT license. See the [LICENSE](LICENSE) file for more information.