import os.path
import urllib.request

from alpha_lib.Output import *
from alpha_lib.Task import *

class ShellTask(Task):
    def __init__(self, name, cmd, success_msg, fail_msg):
        super().__init__(name)
        self.name = name
        self.cmd = cmd
        self.success_msg = success_msg
        self.fail_msg = fail_msg

    def _run(self):
        (success, _, err) = run_shell_cmd(self.cmd)
        if not success:
            out = (OutputEntry() << self.fail_msg <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << self.success_msg
        return (True, out)

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
                           newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
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
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
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
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Recursively deleted directory " << cyan_text(self.dirpath)
        return (True, out)

class ChangeCurrentDirectoryTask(Task):
    def __init__(self, dirpath):
        super().__init__('ChangeCurrentDirectory')
        self.dirpath = dirpath

    def _run(self):
        try:
            os.chdir(os.path.expandvars(self.dirpath))
            out = OutputEntry() << "Changed current directory to " << cyan_text(self.dirpath)
            return (True, out)
        except Exception as e:
            out = (OutputEntry() << red_text("Failed to change current directory to ") << cyan_text(self.dirpath) <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(e))
            return (False, out)

class MoveFileTask(Task):
    def __init__(self, curpath, newpath):
        super().__init__('MoveFile')
        self.curpath = curpath
        self.newpath = newpath

    def _run(self):
        (success, _, err) = run_shell_cmd(f'mv {self.curpath} {self.newpath}')
        if not success:
            out = (OutputEntry() << red_text("Failed to move file ") << cyan_text(self.curpath) <<
                   red_text(' to ') << cyan_text(self.curpath) <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Moved file " << cyan_text(self.curpath) << ' to ' << cyan_text(self.newpath)
        return (True, out)

class RemoveFileTask(Task):
    def __init__(self, filepath):
        super().__init__('RemoveFile')
        self.filepath = filepath

    def _run(self):
        (success, _, err) = run_shell_cmd(f'rv {self.filepath}')
        if not success:
            out = (OutputEntry() << red_text("Failed to remove file ") << cyan_text(self.filepath) <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Removed file " << cyan_text(self.filepath)
        return (True, out)

class CreateSymlinkTask(Task):
    def __init__(self, target, name):
        super().__init__('CreateSimlink')
        self.target = target
        self.name = name

    def _run(self):
        (success, _, err) = run_shell_cmd(f'ln -sf {self.target} {self.name}')
        if not success:
            out = (OutputEntry() << red_text("Failed to create symbolink link ") << cyan_text(self.name) <<
                   red_text(' to target ') << cyan_text(self.target) <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Created symbolic link " << cyan_text(self.name) << ' to target ' << cyan_text(self.target)
        return (True, out)

class ApplyPatchTask(Task):
    def __init__(self, params, filename):
        super().__init__('ApplyPatch')
        self.params = params
        self.filename = filename

    def _run(self):
        (success, _, err) = run_shell_cmd(f'patch {self.params} -i {self.filename}')
        if not success:
            out = (OutputEntry() << red_text("Failed to apply patch ") << cyan_text(self.filename) <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Applied patch " << cyan_text(self.filename)
        return (True, out)

class SetUmaskTask(Task):
    def __init__(self, umask):
        super().__init__('SetUmask')
        self.umask = umask

    def _run(self):
        os.umask(self.umask)
        out = OutputEntry() << "Set umask to " << cyan_text(oct(self.umask))
        return (True, out)

class SedTask(Task):
    def __init__(self, cmds, filepath, msg=None):
        super().__init__('Sed')
        self.cmds = cmds
        self.filepath = filepath
        self.msg = msg

    def _run(self):
        (success, _, err) = run_shell_cmd(f'sed {self.cmds} {self.filepath}')
        if not success:
            out = (OutputEntry() << red_text("Failed to modify file ") << cyan_text(self.filepath) << red_text(' with ') <<
                   yellow_text('sed'))
            if self.msg is None:
                out << red_text(' through commands ') << cyan_text(self.cmds)
            else:
                out << red_text(' to ') << cyan_text(self.msg)
            out << newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8'))
            return (False, out)
        out = OutputEntry() << "Modified file " << cyan_text(self.filepath) << ' with ' << yellow_text('sed')
        if self.msg is None:
            out << ' through commands ' << cyan_text(self.cmds)
        else:
            out << ' to ' << cyan_text(self.msg)
        return (True, out)


class DownloadFileTask(Task):
    def __init__(self, url, filename):
        super().__init__('DownloadFile')
        self.url = url
        self.filename = filename
        self.exist = None

    def start_message(self):
        (self.exist, _, _) = run_shell_cmd(f'test -f {self.filename}')
        out = (OutputEntry() << "Downloading " << cyan_text(self.filename) <<
               ' from URL ' << cyan_text(self.url))
        if self.exist:
            out << yellow_text(' (skipped)')
        return out

    def end_message(self):
        if not self.exist and self.successful():
            return OutputEntry() << "Completed download of " << cyan_text(self.filename)
        return None

    def _run(self):
        if not self.exist:
            try:
                urllib.request.urlretrieve(self.url, self.filename)
                return (True, None)
            except Exception as e:
                out = (OutputEntry() << red_text("Failed to download ") << cyan_text(self.filename) <<
                       red_text(' from URL ') << cyan_text(self.url) << newline() << red_text('Reason: ') <<
                       newline() << yellow_text(e))
                return (False, out)
        return (True, None)

class UnpackArchiveTask(Task):
    def __init__(self, filepath):
        super().__init__('UnpackArchive')
        self.filepath = filepath
        self.ext = None
        self.comp_flag = None
        self.dirpath = None
        self.exist = None

    def start_message(self):
        (_, self.ext) = os.path.splitext(self.filepath)
        if self.ext == '.gz':
            self.comp_flag = 'z'
            self.dirpath = self.filepath[:-7]
        elif self.ext == '.bz2':
            self.comp_flag = 'j'
            self.dirpath = self.filepath[:-8]
        elif self.ext == '.tar':
            self.comp_flag = ''
            self.dirpath = self.filepath[:-4]
        elif self.ext == '.xz':
            self.comp_flag = ''
            self.dirpath = self.filepath[:-7]
        out = OutputEntry() << "Extracting archive " << cyan_text(self.filepath)
        if self.dirpath is not None:
            (self.exist, _, _) = run_shell_cmd(f'test -d {self.dirpath}')
            if self.exist:
                out << yellow_text(' (skipped)')
        return out

    def end_message(self):
        if self.successful():
            return OutputEntry() << "Completed the extraction of the archive " << cyan_text(self.filepath)
        return None

    def _run(self):
        if self.comp_flag is None:
            out = OutputEntry() << red_text("Invalid archive extension ") << cyan_text(self.filepath)
            return (False, out)
        else:
            if self.exist:
                return (True, None)
            else:
                (success, _, err) = run_shell_cmd(f'tar -x{self.comp_flag}f {self.filepath}')
                if not success:
                    out = (OutputEntry() << red_text("Failed to extract archive ") << cyan_text(self.filepath) <<
                           newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
                    return (False, out)
                return (True, None)

class ConfigurePackageTask(Task):
    def __init__(self, flags):
        super().__init__('ConfigurePackage')
        self.flags = flags

    def start_message(self):
        return OutputEntry() << 'Configuring package'

    def end_message(self):
        if self.successful():
            return OutputEntry() << 'Completed package configuration'
        return None

    def _run(self):
        config_cmd = '../configure ' + ' '.join(self.flags)
        (success, _, err) = run_shell_cmd(config_cmd)
        if not success:
            out = (OutputEntry() << red_text("Failed to configure package ") <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        return (True, None)

class CompilePackageTask(Task):
    def __init__(self):
        super().__init__('CompilePackage')

    def start_message(self):
        return OutputEntry() << 'Compiling package'

    def end_message(self):
        if self.successful():
            return OutputEntry() << 'Completed package compilation'
        return None

    def _run(self):
        (success, _, err) = run_shell_cmd('make -j4')
        if not success:
            out = (OutputEntry() << red_text("Failed to compile package ") <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        return (True, None)

class InstallPackageTask(Task):
    def __init__(self, destdir=None):
        super().__init__('InstallPackage')
        self.destdir = destdir

    def start_message(self):
        if self.destdir is not None:
            return OutputEntry() << 'Installing package in directory ' << cyan_text(self.destdir)
        else:
            return OutputEntry() << 'Installing package'

    def end_message(self):
        if self.successful():
            if self.destdir is not None:
                return OutputEntry() << 'Completed package installation in directory' << cyan_text(self.destdir)
            else:
                return OutputEntry() << 'Completed package installation'
        return None

    def _run(self):
        if self.destdir is not None:
            (success, _, err) = run_shell_cmd(f'make DESTDIR={self.destdir} install')
        else:
            (success, _, err) = run_shell_cmd('make install')
        if not success:
            out = (OutputEntry() << red_text("Failed to install package ") <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        return (True, None)
