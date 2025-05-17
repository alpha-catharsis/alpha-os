import os.path

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

    def _run(self):
        return (True, None)

class DisplayEnvironmentTask(Task):
    def __init__(self):
        super().__init__('DisplayEnvironment')

    def start_message(self):
        return OutputEntry() << yellow_text('Start of environment variables')

    def end_message(self):
        return OutputEntry() << yellow_text('End of environment variables')

    def _run(self):
        for key in env.keys():
            self >> DisplayEnvironmentVariableTask(key)
        return (True, None)

class DisplayEnvironmentVariableTask(Task):
    def __init__(self, name):
        super().__init__('DisplayEnvironmentVariable')
        self.name = name

    def _run(self):
        out = OutputEntry() << cyan_text(self.name) << " = " << magenta_text(os.environ[self.name])
        return (True, out)

class SetEnvironmentVariableTask(Task):
    def __init__(self, name, value):
        super().__init__('SetEnvironmentVariable')
        self.name = name
        self.value = value

    def _run(self):
        os.environ[self.name] = os.path.expandvars(self.value)
        out = OutputEntry() << "Set environmental variable " << cyan_text(self.name) << " to " << magenta_text(self.value)
        return (True, out)

class DeleteEnvironmentVariableTask(Task):
    def __init__(self, name):
        super().__init__('DeleteEnvironmentVariable')
        self.name = name

    def _run(self):
        if self.name in os.environ:
            del os.environ[self.name]
            out = OutputEntry() << "Deleted environmental variable " << cyan_text(self.name)
            return (True, out)
        else:
            out = OutputEntry() << red_text("Failed to delete unexisting environmental variable ") << cyan_text(self.name)
            return (False, out)

class CreateDirectoryTask(Task):
    def __init__(self, dirpath, must_not_exist):
        super().__init__('CreateDirectory')
        self.dirpath = dirpath
        self.must_not_exist = must_not_exist

    def _run(self):
        (exist, _, _) = run_shell_cmd(f'test -d {self.dirpath}')
        if exist and self.must_not_exist:
            out = OutputEntry() << red_text("Attempted to create the already existing directory ") << cyan_text(self.dirpath)
            return (False, out)
        else:
            if not exist:
                (success, _, err) = run_shell_cmd(f'mkdir {self.dirpath}')
                if not success:
                    out = (OutputEntry() << red_text("Failed to create directory ") << cyan_text(self.dirpath) <<
                           red_text(', reason: ') << newline() << yellow_text(err.decode('utf-8')))
                    return (False, out)
            out = OutputEntry() << "Created directory " << cyan_text(self.dirpath)
            if exist:
                out << yellow_text(' (skipped)')
            return (True, out)

class DeleteDirectoryTask(Task):
    def __init__(self, dirpath):
        super().__init__('DeleteDirectory')
        self.dirpath = dirpath

    def _run(self):
        (success, _, err) = run_shell_cmd(f'rmdir {self.dirpath}')
        if not success:
            out = (OutputEntry() << red_text("Failed to delete directory ") << cyan_text(self.dirpath) <<
                   red_text(', reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Deleted directory " << cyan_text(self.dirpath)
        return (True, out)

class RecursiveDeleteDirectoryTask(Task):
    def __init__(self, dirpath):
        super().__init__('RecursiveDeleteDirectory')
        self.dirpath = dirpath

    def _run(self):
        (success, _, err) = run_shell_cmd(f'rm -r {self.dirpath}')
        if not success:
            out = (OutputEntry() << red_text("Failed to recursively delete directory ") << cyan_text(self.dirpath) <<
                   red_text(', reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Recursively deleted directory " << cyan_text(self.dirpath)
        return (True, out)

