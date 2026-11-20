# LayerUpon - Esoteric bracket-based programming language
# Independent command-line interpreter, no GUI dependency
# Syntax: () [] {} <> space
# Python 3.8+ compatible
import sys
sys.stdout.reconfigure(encoding='utf-8')
from typing import List, Dict, Tuple


def filter_parens(s: str) -> str:
    keep = set("()[]{}<> ")
    return "".join(ch for ch in s if ch in keep)


def parse_number(s: str) -> int:
    bits = []
    for c in s:
        if c == '[':
            bits.append('1')
        elif c == ']':
            bits.append('0')
    if not bits:
        return 0
    return int(''.join(bits), 2)


def tokenize(paren_stream: str) -> List[Tuple[str, int]]:
    tokens: List[Tuple[str, int]] = []
    i = 0
    n = len(paren_stream)
    while i < n:
        if paren_stream[i] == '>' and i+1 < n and paren_stream[i+1] == '(':
            j = i + 2
            buf = ""
            while j < n and paren_stream[j] != ')':
                buf += paren_stream[j]
                j += 1
            if j+1 < n and paren_stream[j+1] == '<':
                threshold = parse_number(buf)
                tokens.append(("JNZ_NE", threshold))
                i = j + 2
                continue
        if paren_stream.startswith("><", i):
            tokens.append(("JNZ_NE", 0))
            i += 2
            continue
        if paren_stream.startswith(")(", i):
            tokens.append(("PRINT", 0))
            i += 2
        elif paren_stream.startswith("[]", i):
            tokens.append(("ADD", 0))
            i += 2
        elif paren_stream.startswith("][", i):
            tokens.append(("SUB", 0))
            i += 2
        elif paren_stream.startswith("{}", i):
            tokens.append(("MUL", 0))
            i += 2
        elif paren_stream.startswith("}{", i):
            tokens.append(("DIV", 0))
            i += 2
        elif paren_stream[i] == '(':
            # PUSH ( binary )
            j = i + 1
            buf = ""
            while j < n and paren_stream[j] != ')':
                buf += paren_stream[j]
                j += 1
            num = parse_number(buf)
            tokens.append(("PUSH", num))
            i = j + 1
        elif paren_stream[i] == '>':
            #LABEL >binary<
            j = i + 1
            buf = ""
            while j < n and paren_stream[j] != '<':
                buf += paren_stream[j]
                j += 1
            num = parse_number(buf)
            tokens.append(("LABEL", num))
            i = j + 1
        elif paren_stream[i] == '<':
            #PICK <binary>
            j = i + 1
            buf = ""
            while j < n and paren_stream[j] != '>':
                buf += paren_stream[j]
                j += 1
            num = parse_number(buf)
            tokens.append(("PICK", num))
            i = j + 1
        elif paren_stream[i] == ' ':
            tokens.append(("INPUT", 0))
            i += 1
        else:
            i += 1
    return tokens


def run(tokens: List[Tuple[str, int]], debug: bool):
    stack = []
    pc = 0
    label_map: Dict[int, int] = {}
    for idx, (op, val) in enumerate(tokens):
        if op == "LABEL":
            label_map[val] = idx

    while pc < len(tokens):
        op, val = tokens[pc]
        if debug:
            print(f"[DEBUG] pc={pc}, op={op:6s}, threshold={val}, stack={stack}", flush=True)

        if op == "PUSH":
            stack.append(val)
            pc += 1
        elif op == "ADD":
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            pc += 1
        elif op == "SUB":
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            pc += 1
        elif op == "MUL":
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            pc += 1
        elif op == "DIV":
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                if b != 0:
                    stack.append(a // b)
            pc += 1
        elif op == "PRINT":
            if stack:
                v = stack.pop()
                print(chr(v), end="", flush=True)
            pc += 1
        elif op == "LABEL":
            pc += 1
        elif op == "JNZ_NE":
            threshold = val
            if len(stack) >= 2:
                cond = stack.pop()
                target = stack.pop()
                if cond != threshold:
                    pc = label_map.get(target, pc + 1)
                else:
                    pc += 1
            else:
                pc += 1
        elif op == "PICK":
            if stack:
                depth = min(val, len(stack) - 1)
                stack.append(stack[-(depth + 1)])
            pc += 1
        elif op == "INPUT":
            ch = sys.stdin.read(1)
            if ch == "":
                raise EOFError("INPUT: EOF reached")
            stack.append(ord(ch))
            pc += 1
        else:
            pc += 1


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    debug_flag = False
    filepath = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--debug":
            if i + 1 >= len(args):
                print("Error: --debug requires t or f")
                return
            debug_flag = (args[i+1].lower() == "t")
            i += 2
        else:
            filepath = args[i]
            i += 1
    if filepath is None:
        print("Usage: python LayerUpon.py [--debug t/f] your_file.layer")
        print("Example: python LayerUpon.py --debug t hello.layer")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            src = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return
    stream = filter_parens(src)
    tokens = tokenize(stream)
    run(tokens, debug_flag)


if __name__ == "__main__":
    main()
