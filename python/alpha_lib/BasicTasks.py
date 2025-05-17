from alpha_lib.Output import *
from alpha_lib.Task import *

class ChainTask(Task):
    def __init__(self, prologue, epilogue, error_msg, children):
        super().__init__('Chain')
        self.prologue = prologue
        self.epilogue = epilogue
        self.error_msg = error_msg
        self.children = children

    def start_message(self):
        return self.prologue

    def end_message(self):
        if any(map(lambda child: child.failed(), self.children)):
            return self.error_msg
        else:
            return self.epilogue

    def _run(self, env):
        return (True, None, env)

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
    def __init__(self, name):
        super().__init__('DisplayEnvironmentVariable')
        self.name = name

    def _run(self, env):
        out = OutputEntry() << cyan_text(self.name) << " = " << magenta_text(env[self.name])
        return (True, out, env)

class SetEnvironmentVariableTask(Task):
    def __init__(self, name, value):
        super().__init__('SetEnvironmentVariable')
        self.name = name
        self.value = value

    def _run(self, env):
        newenv = env.copy()
        newenv[self.name] = self.value
        out = OutputEntry() << "Set environmental variable " << cyan_text(self.name) << " to " << magenta_text(self.value)
        return (True, out, newenv)

class DeleteEnvironmentVariableTask(Task):
    def __init__(self, name):
        super().__init__('DeleteEnvironmentVariable')
        self.name = name

    def _run(self, env):
        if self.name in env:
            newenv = env.copy()
            del newenv[self.name]
            out = OutputEntry() << "Deleted environmental variable " << cyan_text(self.name)
            return (True, out, newenv)
        else:
            out = OutputEntry() << red_text("Failed to delete unexisting environmental variable ") << cyan_text(self.name)
            return (False, out, env)
