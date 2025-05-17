import enum
import os
import subprocess
import sys
import threading

class OutputElem:
    def __init__(self):
        pass

    def hsize(self):
        raise NotImplementedError()

    def vsize(self):
        raise NotImplementedError()

    def output(self):
        raise NotImplementedError()

    def split(self, size):
        raise NotImplementedError()


class NewlineElem(OutputElem):
    def __init__(self):
        pass

    def hsize(self):
        return 0

    def vsize(self):
        return 1

    def output(self):
        return "\n"


def newline():
    return NewlineElem()


class OutputColor(enum.Enum):
    BLACK = 90
    RED = 91
    GREEN = 92
    YELLOW = 93
    BLUE = 94
    MAGENTA = 95
    CYAN = 96
    WHITE = 37 # non-bright white


class TextElem(OutputElem):
    def __init__(self, color, text):
        super().__init__()
        self.color = color
        self.text = text

    def hsize(self):
        return len(self.text)

    def vsize(self):
        return 0

    def output(self):
        return f"\x1b[{self.color.value}m{self.text}\x1b[30m"

    def split(self, size):
        return (TextElem(self.color, self.text[:size]), TextElem(self.color, self.text[size:]))


def to_text(obj):
    if isinstance(obj, OutputElem):
        return obj.output()
    if isinstance(obj, str):
        return obj
    else:
        return str(obj)

def black_text(obj):
    return TextElem(OutputColor.BLACK, to_text(obj))

def red_text(obj):
    return TextElem(OutputColor.RED, to_text(obj))

def green_text(obj):
    return TextElem(OutputColor.GREEN, to_text(obj))

def yellow_text(obj):
    return TextElem(OutputColor.YELLOW, to_text(obj))

def blue_text(obj):
    return TextElem(OutputColor.BLUE, to_text(obj))

def magenta_text(obj):
    return TextElem(OutputColor.MAGENTA, to_text(obj))

def cyan_text(obj):
    return TextElem(OutputColor.CYAN, to_text(obj))

def white_text(obj):
    return TextElem(OutputColor.WHITE, to_text(obj))

class OutputEntry:
    def __init__(self):
        self.elements = []

    def __lshift__(self, other):
        if isinstance(other, OutputElem):
            self.elements.append(other)
        else:
            self.elements.append(white_text(str(other)))
        return self

    def display(self, level, max_col):
        col = level * 2
        i = 0
        elem = None
        sys.stdout.write(" " * (level * 2))
        while i < len(self.elements):
            if elem is None:
                elem = self.elements[i]
            if elem.hsize() + col > max_col:
                (first_elem, elem) = elem.split(max_col - col)
                sys.stdout.write(first_elem.output())
                sys.stdout.write("\n" + " " * (level * 2))
                col = level * 2
            else:
                sys.stdout.write(elem.output())
                i += 1
                if elem.vsize() > 0:
                    sys.stdout.write(" " * (level * 2))
                    col = level * 2
                else:
                    col += elem.hsize()
                elem = None
        sys.stdout.write("\n")
        sys.stdout.flush()


