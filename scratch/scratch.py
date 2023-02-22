import bf_codegen
from bf_codegen import interpreter

#check = lambda program, expected: "".join([ch for ch in interpreter.run(program)]) == expected

context = bf_codegen.Context()
#hello_str = context.build_store("Hello, Sailor!\n")
#context.build_print(hello_str)

newline = context.build_store(["\n"])

def body():
    sum = context.build_add(loop_times, 48)
    context.build_print(sum)

    context.build_assign(sum, 0)
    context.build_print(newline)

loop_times = context.build_store([8])
context.build_loop(
    times = loop_times,
    body = body
)

prog = context.to_str()
#print("program length:", len(prog))
#print(prog)
out = interpreter.run(prog)
