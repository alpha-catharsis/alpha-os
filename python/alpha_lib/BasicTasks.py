from alpha_lib.Output import *
from alpha_lib.Task import *

class DisplayEnvironmentTask(Task):
    def __init__(self):
        super().__init__('DisplayEnvironment')

    def start_message(self):
        return OutputEntry() << yellow_text('Start of environment variables')

    def end_message(self):
        return OutputEntry() << yellow_text('End of environment variables')

    def _run(self, env):
        for key in env.keys():
            self >> DisplayEnvironmentVariableTask(key)
        return (True, None, env)

class DisplayEnvironmentVariableTask(Task):
    def __init__(self, varname):
        super().__init__('DisplayEnvironmentVariable')
        self.varname = varname

    def _run(self, env):
        out = OutputEntry() << cyan_text(self.varname) << " = " << magenta_text(env[self.varname])
        return (True, out, env)
