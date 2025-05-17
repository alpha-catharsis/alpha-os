#!/usr/bin/env python3

import os

from alpha_lib.Output import *
from alpha_lib.Task import *
from alpha_lib.BasicTasks import *


if __name__ == '__main__':
    t = ChainTask(OutputEntry() << yellow_text('Playing with environment variables'),
                  OutputEntry() << yellow_text('Finished playing with environment variables'),
                  OutputEntry() << red_text('Unexpected problem playing with environment variables'),
                  [SetEnvironmentVariableTask('XYZ', '/home/alpha'),
                   SetEnvironmentVariableTask('ABC', '0123456789'),
                   DisplayEnvironmentTask(),
                   DeleteEnvironmentVariableTask('ABC'),
                   DisplayEnvironmentTask()])
    execute(t, {})
