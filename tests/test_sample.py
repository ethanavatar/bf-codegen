import bf_codegen
from bf_codegen import interpreter

def test_hello():
    context = bf_codegen.Context()
    hello_str = context.build_store("Hello, Sailor!\n")
    context.build_print(hello_str)

    prog = context.to_str()
    out = ""
    for ch in interpreter.run(prog):
        out += ch

    assert out == "Hello, Sailor!\n"
