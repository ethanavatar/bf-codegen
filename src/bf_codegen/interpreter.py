import sys

def interpret(src: str):
    tape = [0]
    ptr = 0

    if not src:
        return

    i = 0
    while i < len(src):
        c = src[i]
        if c == ">":
            ptr += 1
            if ptr == len(tape):
                tape.append(0)

        elif c == "<":
            ptr -= 1
            if ptr < 0:
                raise IndexError("Tape pointer went negative")

        elif c == "+":
            tape[ptr] += 1

            if tape[ptr] > 255:
                raise ValueError("Tape value went above 255")

        elif c == "-":
            tape[ptr] -= 1

            if tape[ptr] < 0:
                raise ValueError("Tape value went negative")

        elif c == ".":
            print(chr(tape[ptr]), end="")
            yield chr(tape[ptr])

        elif c == ",":
            tape[ptr] = ord(input())

        elif c == "[":
            if tape[ptr] == 0:
                depth = 1
                while depth > 0:
                    i += 1
                    if src[i] == "[":
                        depth += 1
                    elif src[i] == "]":
                        depth -= 1

        elif c == "]":
            if tape[ptr] != 0:
                depth = 1
                while depth > 0:
                    i -= 1
                    if src[i] == "]":
                        depth += 1
                    elif src[i] == "[":
                        depth -= 1

        i += 1

run = lambda program: "".join([ch for ch in interpret(program)])

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 bf.py <file>")
        return

    with open(sys.argv[1]) as f:
        src = f.read()

    run(src)

if __name__ == "__main__":
    main()