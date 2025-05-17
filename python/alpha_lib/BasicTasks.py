import subprocess

from alpha_lib.Output import *
from alpha_lib.Task import *

class ChainTask(Task):
    def __init__(self, name, prologue, epilogue, error_msg, children):
        super().__init__(name)
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

class CreateDirectoryTask(Task):
    def __init__(self, dirpath, must_not_exist):
        super().__init__('CreateDirectory')
        self.dirpath = dirpath
        self.must_not_exist = must_not_exist

    def _run(self, env):
        exist_check = subprocess.Popen(f'test -d {self.dirpath}', shell=True, env=env)
        exist_check.communicate()
        exist = exist_check.returncode == 0
        if exist and self.must_not_exist:
            out = OutputEntry() << red_text("Attempted to create the already existing directory ") << cyan_text(self.dirpath)
            return (False, out, env)
        else:
            if not exist:
                create_dir = subprocess.Popen(f'mkdir {self.dirpath}', shell=True, env=env, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                (_, err) = create_dir.communicate()
                failed = create_dir.returncode != 0
                if failed:
                    out = (OutputEntry() << red_text("Failed to create directory ") << cyan_text(self.dirpath) <<
                           red_text(', reason: ') << newline() << yellow_text(err.decode('utf-8')))
                    return (False, out, env)
            out = OutputEntry() << "Created directory " << cyan_text(self.dirpath)
            if exist:
                out << yellow_text(' (skipped)')
            return (True, out, env)
