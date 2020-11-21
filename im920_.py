# テスト用
import sys


class Im920:
    def __init__(self, port="COM3"):
        with open("test/data.csv", 'r') as f:
            self.data = f.readlines()
        self._buf = list()
        self.i = 0
        self.update_buf()

    @property
    def buf(self):
        r = self._buf
        if len(self._buf) == 0:
            self.i += 1
            self.update_buf()
        return r

    def receive(self):
        if self._buf == []:
            return []
        return self._buf.pop(0)

    def update_buf(self):
        try:
            self._buf = self.data[self.i].split(',')
        except IndexError:
            print("data end")
            sys.exit()


if __name__ == "__main__":
    im920 = Im920("COM3")
    while len(im920.buf) > 0:
        print(im920.receive())
    print(im920.buf)
