#!/usr/bin/env python3

import os

from alpha_lib.Output import *
from alpha_lib.Task import *
from alpha_lib.BasicTasks import *
from alpha_lib.Bootstrap import *

if __name__ == '__main__':
    print()
    t = BootstrapAlphaOSTask()
    execute(t, 0, 160)
