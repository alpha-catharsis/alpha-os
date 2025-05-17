#!/usr/bin/env python3

from alpha_lib.Output import *

if __name__ == '__main__':
    entry1 = OutputEntry()
    entry1 << yellow_text("1245")
    entry1.display(1, 80)
