# LayerUpon

**An esoteric stack-based programming language written entirely with brackets and spaces.**

> A weird little programming language where brackets do the work, spaces read input, and everything runs on a stack.

LayerUpon is an esoteric programming language (esolang) built around a stack-based virtual machine.

Its source code uses only these characters:

```text
( ) [ ] { } < >
```

And one additional character:

```text
SPACE
```

Despite its minimal syntax, LayerUpon supports arithmetic, input/output, stack manipulation, labels, conditional jumps, and loops.

The official interpreter is written in Python.

## ✨ Features

* **Minimal syntax** — only four types of brackets and spaces.
* **Stack-based execution** — all calculations operate on a stack.
* **Binary number encoding** — `[` represents 1 and `]` represents 0.
* **Arithmetic operations** — addition, subtraction, multiplication, and integer division.
* **Character I/O** — read characters and output Unicode characters.
* **Stack manipulation** — copy elements from different stack depths.
* **Labels and jumps** — implement loops and conditional control flow.
* **Custom threshold jumps** — jump when a value differs from a specified constant.
* **Debug mode** — inspect instructions and stack contents during execution.
* **Python interpreter** — Python 3.8+.
* **Windows IDE** — a graphical editor with syntax highlighting and execution controls.

## 📜 Instruction Set

| Syntax      | Instruction | Description                                                     |
| ----------- | ----------- | --------------------------------------------------------------- |
| `(...)`     | `PUSH`      | Decode a binary number and push it onto the stack.              |
| `)(`        | `PRINT`     | Pop a value and output its Unicode character.                   |
| `[]`        | `ADD`       | Pop `b`, pop `a`, push `a + b`.                                 |
| `][`        | `SUB`       | Pop `b`, pop `a`, push `a - b`.                                 |
| `{}`        | `MUL`       | Pop `b`, pop `a`, push `a * b`.                                 |
| `}{`        | `DIV`       | Pop `b`, pop `a`, push `a // b`.                                |
| ` ` (space) | `INPUT`     | Read one non-newline character and push its Unicode code point. |
| `<...>`     | `PICK`      | Copy an element from the stack at the specified depth.          |
| `>...<`     | `LABEL`     | Define a label with a numeric ID.                               |
| `><`        | `JNZ_NE`    | Jump if the condition is not equal to zero.                     |
| `>(...)<`   | `JNZ_NE`    | Jump if the condition is not equal to a specified threshold.    |

### Binary Encoding

LayerUpon represents non-negative integers using square brackets:

* `[` represents binary `1`.
* `]` represents binary `0`.

For example:

| LayerUpon   | Binary    | Decimal |
| ----------- | --------- | ------: |
| `()`        | Empty     |       0 |
| `([)`       | `1`       |       1 |
| `([])`      | `10`      |       2 |
| `([[)`      | `11`      |       3 |
| `([]])`     | `100`     |       4 |
| `([][)`     | `101`     |       5 |
| `([]]]]][)` | `1000001` |      65 |

The parentheses indicate a `PUSH` instruction.

For example:

```text
([][)
```

Means:

```text
PUSH 5
```

## 🚀 Getting Started

### Requirements

* Python 3.8 or newer
* No third-party dependencies for the command-line interpreter

### Run a Program

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/LayerUpon.git
cd LayerUpon
```

Replace `YOUR_USERNAME` with the actual GitHub account name.

Run a LayerUpon source file:

```bash
python LayerUpon.py --debug f hello.layer
```

Enable debugging:

```bash
python LayerUpon.py --debug t hello.layer
```

You can also run a file without specifying the debug flag:

```bash
python LayerUpon.py hello.layer
```

### Debug Options

| Option      | Description                        |
| ----------- | ---------------------------------- |
| `--debug t` | Enable execution tracing.          |
| `--debug f` | Disable execution tracing.         |
| No flag     | Run normally without debug output. |

When debug mode is enabled, the interpreter displays the program counter, current operation, instruction value, and stack contents.

## 💻 Examples

### Example 1: Print a Character

Create a file named `hello.layer`:

```text
([]]]]][)
)(
```

Output:

```text
A
```

Explanation:

1. `([]]]]][)` pushes `65` onto the stack.
2. `)(` pops `65` and prints the corresponding Unicode character.
3. The program finishes.

The result is the letter `A`.

### Example 2: Basic Arithmetic

```text
([][)
([[)
[]
```

Equivalent pseudocode:

```text
PUSH 5
PUSH 3
ADD
```

Final stack:

```text
[8]
```

LayerUpon performs arithmetic using integers stored on the stack.

### Example 3: Single-Digit Addition

LayerUpon can even implement a small calculator:

```text
 ([[]]]])][ [])(
```

This program reads two digit characters, adds their numeric values, and prints the result.

Example interaction:

```text
4
1
5
```

The final `5` is the program's output.

How it works:

1. Read the first digit character.
2. Subtract `48` to convert it from an ASCII-compatible digit code point to its numeric value.
3. Read the second digit character.
4. Add the second character's code point.
5. Print the resulting character.

This example works when the sum is between `0` and `9`.

If the sum exceeds `9`, the result will not be a multi-character decimal number.

## 🧠 Stack Model

LayerUpon operates on a stack of integers.

For example:

```text
PUSH 5
PUSH 3
ADD
```

Changes the stack as follows:

```text
[]
[5]
[5, 3]
[8]
```

The last element is the top of the stack.

### PICK

The `PICK` instruction copies an existing stack value without removing it.

For a stack:

```text
[10, 20, 30]
```

The following depths refer to:

| Depth | Value |
| ----- | ----: |
| 0     |    30 |
| 1     |    20 |
| 2     |    10 |

If the requested depth exceeds the stack size, the interpreter copies the bottom element.

If the stack is empty, `PICK` does nothing.

## 🔀 Labels and Conditional Jumps

LayerUpon supports conditional control flow through labels and jump instructions.

### Labels

Labels use this syntax:

```text
>binary<
```

For example:

```text
>[<
```

Defines label `1`.

Labels do not modify the stack.

### Standard Conditional Jump

```text
><
```

This instruction removes two values from the stack:

1. `cond` — the condition, popped first.
2. `target_id` — the destination label, popped second.

If `cond != 0`, execution jumps to `target_id`.

Otherwise, execution continues with the next instruction.

For example:

```text
([)
([)
><
```

Equivalent pseudocode:

```text
PUSH 1       # Target label
PUSH 1       # Condition
JUMP_IF_NOT_ZERO
```

### Custom Threshold Jump

LayerUpon also supports:

```text
>(binary)<
```

This instruction jumps if the condition is **not equal to the specified threshold**.

For example:

```text
>([[)<
```

The threshold is binary `11`, which is decimal `3`.

Equivalent pseudocode:

```text
target = pop()
```

More precisely, the pop order is:

```text
cond = pop()
target = pop()

if cond != 3:
    jump(target)
```

The shorthand:

```text
><
```

Is equivalent to:

```text
>()<
```

Both use threshold `0`.

This feature allows programs to compare stack values against constants without requiring a separate comparison instruction.

## ⌨️ Input and Output

### INPUT

A single space character is an `INPUT` instruction.

It reads one character from standard input and pushes its Unicode code point onto the stack.

In the current interpreter, carriage returns and newline characters are skipped.

This makes it convenient to enter characters separately in a Windows terminal.

**Important:** Spaces are executable instructions. Adding or removing spaces can change program behavior.

### PRINT

The instruction:

```text
)(
```

Pops the top stack value and converts it to a Unicode character using Python's `chr()` function.

For example:

```text
PUSH 65
PRINT
```

Outputs:

```text
A
```

## 🛠️ LayerUpon IDE

LayerUpon also includes a graphical IDE built with **Python and PySide6**.

Features include:

* Dark-themed code editor
* Bracket syntax highlighting
* Multiple editor tabs
* Create, open, and save `.layer` files
* Unsaved-change warnings
* Integrated execution terminal
* Interactive character input
* Debug execution logs
* Optional whitespace visualization
* Run and stop controls

### Keyboard Shortcuts

| Shortcut     | Action                  |
| ------------ | ----------------------- |
| `F5`         | Run the current program |
| `F6`         | Run with debug tracing  |
| `Shift + F5` | Stop execution          |
| `Ctrl + S`   | Save the current file   |

The current debug mode provides execution tracing. Interactive instruction-by-instruction stepping is a planned enhancement.

### Run the IDE

Install PySide6:

```bash
pip install PySide6
```

Start the IDE:

```bash
python IDE.py
```

## 📦 Windows Executable

LayerUpon can be packaged into a standalone Windows executable using PyInstaller.

Install PyInstaller:

```bash
pip install pyinstaller
```

For example, build the IDE:

```bash
pyinstaller --onefile --name LayerUpon-IDE IDE.py
```

The generated executable will be located in the `dist` directory.

A graphical build can also be created using `--windowed`, but interactive standard input/output must be tested in that configuration.

Prebuilt binaries, when available, can be distributed through the repository's GitHub Releases page.

## 🔬 Computational Model

LayerUpon combines:

* An integer stack
* Arithmetic operations
* Conditional jumps
* Labels
* Stack manipulation

These features support general-purpose control flow and computation.

### Two-Counter Machine Compiler

The project also explores compilation from a two-counter machine (TCM) into LayerUpon.

Two counters, `A` and `B`, can be encoded as a single integer:

$$
S = 2^A \times 3^B
$$

Incrementing a counter corresponds to multiplying `S` by the appropriate prime number.

Conditional decrement operations can be constructed using integer division, multiplication, subtraction, and conditional jumps.

This provides a constructive approach to studying LayerUpon's computational capabilities.

A complete Turing-completeness claim assumes unbounded integer precision, stack capacity, and execution time, together with a correct translation of a universal two-counter machine.

## ⚠️ Language Notes

LayerUpon intentionally has several unusual behaviors.

**Whitespace is significant.** ASCII spaces represent INPUT instructions and must not be inserted for formatting purposes.

**Line breaks are ignored in source code.** Programs can be written across multiple lines without changing their meaning.

**Non-language characters are filtered out.** However, bracket and space characters inside apparent comments are still interpreted, so ordinary text comments are not automatically safe.

**Stack underflow is generally tolerated.** Arithmetic operations with insufficient operands do nothing.

**Integer division uses floor division.** The current interpreter also has a specific behavior for division by zero: operands are removed without pushing a result.

**Unknown jump labels do not cause an exception.** Execution continues with the next instruction.

These behaviors describe the current interpreter and may be refined in future versions.

## 🗺️ Roadmap

* [x] Stack-based interpreter
* [x] Binary integer encoding
* [x] Arithmetic instructions
* [x] Character input/output
* [x] Labels and conditional jumps
* [x] Custom threshold jumps
* [x] Debug execution tracing
* [x] Initial graphical IDE implementation
* [ ] Interactive single-step debugger
* [ ] Breakpoints and stack inspection
* [ ] Improved syntax error reporting
* [ ] Additional example programs
* [ ] Automated interpreter tests
* [ ] Stable Windows release builds
* [ ] Formal language specification

## 🤝 Contributing

Contributions, bug reports, example programs, and suggestions are welcome.

If you find a problem, please open a GitHub issue with:

* A description of the problem
* The LayerUpon source code involved
* Expected behavior
* Actual behavior
* Python version and operating system

## 📄 License

See the `LICENSE` file for the repository's licensing terms.

---

**LayerUpon — Because apparently eight brackets and a space are enough to make programming interesting.**
