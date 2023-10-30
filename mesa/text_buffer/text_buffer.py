class TextBuffer:
    def __init__(self) -> None:
        self.buffer = ""
        self.pointer = 0

    def shift_left(self):
        if self.pointer != 0:
            self.pointer -= 1

    def shift_right(self):
        if self.pointer != len(self.buffer):
            self.pointer += 1

    def add(self, char):
        if self.pointer == 0:
            self.buffer = char + self.buffer
        elif self.pointer == len(self.buffer):
            self.buffer = self.buffer + char
        else:
            self.left_part = self.buffer[: self.pointer]

            self.right_part = self.buffer[self.pointer :]
            self.buffer = self.left_part + char + self.right_part

    def pop(self):
        if self.pointer == len(self.buffer):
            self.buffer = self.buffer[:-1]
        else:
            self.left_part = self.buffer[: self.pointer - 1]

            self.right_part = self.buffer[self.pointer :]
            self.buffer = self.left_part + self.right_part
        self.shift_left()

    def delete(self):
        self.buffer = ""
        self.pointer = 0
