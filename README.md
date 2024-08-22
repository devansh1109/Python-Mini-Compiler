# Python Lexer and Parser with PLY

## Overview

This project includes a lexer and parser implementation using the PLY (Python Lex-Yacc) library. The lexer and parser are designed to handle a custom syntax, which supports basic control structures and functions, including `for` loops, `while` loops, `if-else` conditions, and function definitions. The grammar also supports list and tuple declarations.

## Features

- **Lexer:** Tokenizes input based on predefined patterns, including keywords (`for`, `while`, `if`, `else`, `elif`, `def`), delimiters (`:`, `,`, `(`, `)`, `{`, `}`, `[`, `]`, `"`), and indentation-based changes.
- **Parser:** Parses the tokenized input to build a syntactic structure. Supports:
  - For loops
  - While loops
  - If-else conditions
  - Function definitions
  - List and tuple declarations

## Requirements

- Python 3.x
- PLY library

## Installation

Install PLY using pip if it's not already installed:

```bash
pip install ply
```

# Usage
- **Define the Syntax:** The lexer and parser are defined to handle a custom syntax.
- **Input the Code:** Run the script and input the code lines interactively. End input with a blank line.
- **Parse and Validate:** The parser checks the input syntax and prints validation messages for the different types of constructs.

```bash
Enter the syntax
for i in range(10):
    print(i)

def my_function(x, y):
    return x + y

if x > 5:
    print("x is greater than 5")
else:
    print("x is 5 or less")

while x < 10:
    x = x + 1
```

The above input will produce output indicating the validity of function definitions, loops, and conditionals.

# Lexer Rules
- **Keywords:** for, while, if, else, elif, def, in, range
- **Identifiers:** Variable and function names
- **Delimiters:** :, ,, (, ), {, }, [, ], "
- **Indentation:** Managed using a stack to handle nested blocks
# Parser Rules
- **For Loop:** for IDENTIFIER in cond : INDENT statements DEDENT
- **Function Definition:** def IDENTIFIER ( args ) : INDENT statements DEDENT
- **If-Else Condition:** if cond : INDENT statements DEDENT (elif or else ...)
- **While Loop:** while cond : INDENT statements DEDENT
- **Tuple Declaration:** ( tupl_elements )

# Error Handling

Errors are reported with line and position details if syntax issues are detected.

#Contributing
Contributions are welcome! Please open an issue or submit a pull request to contribute to the project.
