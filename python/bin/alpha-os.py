#!/usr/bin/env python3

import os

from alpha_lib.Output import *
from alpha_lib.Task import *
from alpha_lib.BasicTasks import *

if __name__ == '__main__':
    t = CreateDirectoryTask('$HOME/xyz', False)
    execute(t, os.environ)
