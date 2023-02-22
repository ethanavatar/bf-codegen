from __future__ import annotations
import typing as t

TapePointer = int
Storable = t.Union[int, str]

class Store:
    def __init__(self, ptr: TapePointer, size: int):
        self.ptr = ptr
        self.size = size

class Context:
    def __init__(self):
        self.top = 0
        self.pointer: int = 0
        self.output: str = ""

    def inc(times: int = 1) -> str:
        return "".join(["+" for _ in range(times)])# + "\n"

    def dec(times: int = 1) -> str:
        return "".join(["-" for _ in range(times)])# + "\n"

    def build_increment(self, times: int = 1) -> None:
        self.output += Context.inc(times)

    def build_decrement(self, times: int = 1) -> None:
        self.output += Context.dec(times)

    def build_shift_right(self) -> None:
        self.output += ">"
        self.pointer += 1
        if self.pointer > self.top:
            self.top = self.pointer

    def build_shift_left(self) -> None:
        self.output += "<"
        self.pointer -= 1

    def build_store(self, value: t.Iterable[Storable]) -> Store:
        self.seek_to(Store(self.top, 0))
        head = self.top

        if value == [0]:
            self.build_increment()
            self.build_decrement()
            self.build_shift_right()

            return Store(head, 1)

        for i in value:
            if isinstance(i, str):
                i = ord(i)

            if i < 0:
                raise ValueError("Cannot store negative values")

            if i > 255:
                raise ValueError("Cannot store values greater than 255")

            # increment the current cell by the value of the character
            self.build_increment(i)
            self.build_shift_right()

        return Store(head, len(value))

    def build_print(self, ptr: Store) -> None:
        self.seek_to(ptr)

        if ptr.size > 1:
            for i in range(ptr.size):
                self.output += "."

                if i < ptr.size - 1:
                    self.build_shift_right()

            return

        self.output += "."

    def seek_to(self, ptr: Store) -> None:
        # if the pointer is greater than the destination, shift left
        if ptr.ptr > self.pointer:
            times = ptr.ptr - self.pointer
            for _ in range(times):
                self.build_shift_right()

        # if the pointer is less than the destination, shift right
        elif ptr.ptr < self.pointer:
            times = self.pointer - ptr.ptr
            for _ in range(times):
                self.build_shift_left()

        # if the pointer is equal to the destination, do nothing

    def seek_to_start(self) -> None:
        self.seek_to(Store(0, 0))

    def build_loop(self, times: Store, body: t.Callable[[], None]) -> None:
        # seek to the cell that stores the loop counter
        self.seek_to(times)

        # start the loop if the counter is not zero
        self.output += "\n[\n"

        # execute the loop body
        body()

        # seek back to the loop counter and decrement it
        self.seek_to(times)
        self.build_decrement()

        # repeats until the loop counter is zero
        self.output += "\n]\n"

    def free(self, ptr: Store) -> None:
        self.seek_to(ptr)
        self.output += "[-]"

    def build_assign(self, ptr: Store, value: Storable) -> None:
        
        self.free(ptr)
        self.build_increment(value)

    # Maybe unneeded
    def build_realloc(self, ptr: Store) -> Store:

        # allocate a new cell for the destination
        dest = self.build_store([0])

        def body():
            # seek to the destination and increment it
            self.seek_to(dest)
            self.build_increment()

            # seek to the original value and decrement it
            self.seek_to(ptr)
            self.build_decrement()

        # execute the loop body until the original value is zero
        self.build_loop(
            times = ptr,
            body = body
        )

        return dest

    def move_value_to(self, src: Store, dest: Store) -> None:

        def body():
            # seek to the destination and increment it
            self.seek_to(dest)
            self.build_increment()

            # seek to the original value and decrement it
            self.seek_to(src)
            #self.build_decrement()

        # execute the loop body until the original value is zero
        self.build_loop(
            times = src,
            body = body
        )


    def build_duplicate_to(self, src: Store, a: Store, b: Store) -> None:

        def body():
            # seek to the first destination and increment it
            self.seek_to(a)
            self.build_increment()

            # seek to the second destination and increment it
            self.seek_to(b)
            self.build_increment()

            # seek to the original value and decrement it
            self.seek_to(src)
            #self.build_decrement()

        # execute the loop body until the original value is zero
        self.build_loop(
            times = src,
            body = body
        )

    def build_add(self, ptr: Store, value: int) -> Store:

        # allocate a temporary cell to duplicate the original value into
        temp = self.build_store([0])

        # allocate a new cell to store the result
        new_val = self.build_store([0])

        # duplicate the original value into both the temporary cell and the result cell
        self.build_duplicate_to(ptr, temp, new_val)

        # duplicate call leaves `ptr` at 0

        # move the temporary value into the original cell
        self.move_value_to(temp, ptr)

        # seek to the result cell and increment it by the given value
        self.seek_to(new_val)
        self.build_increment(value)

        return new_val

    def code(self) -> str:
        return self.output


def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
