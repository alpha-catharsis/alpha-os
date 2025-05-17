import subprocess

from alpha_lib.Output import *
from alpha_lib.Task import *
from alpha_lib.BasicTasks import *

class BootstrapAlphaOSTask(ChainTask):
    def __init__(self):
        alpha_os_elem = yellow_text('Alpha OS')
        super().__init__('BootstrapAlphaOS',
                         OutputEntry() << 'Boostrapping ' << alpha_os_elem,
                         OutputEntry() << 'Finished boostrapping ' << alpha_os_elem,
                         OutputEntry() << red_text('Error boostrapping ') << alpha_os_elem,
                         [SetEnvironmentVariableTask('ALPHA_OS_ROOT', '/home/alpha/alpha-os'),
                          CreateDirectoryTask('$ALPHA_OS_ROOT', False),
                          ImplementFHSTask(),
                          SetEnvironmentVariableTask('ALPHA_BOOTSTRAP', '/home/alpha/alpha-os/bootstrap'),
                          CreateDirectoryTask('$ALPHA_BOOTSTRAP', False)])


class ImplementFHSTask(ChainTask):
    def __init__(self):
        fhs_elem = yellow_text('Filesystem Hierarchy Standard (FHS)')
        super().__init__('ImplementFHSTask',
                         OutputEntry() << 'Implementing ' << fhs_elem,
                         OutputEntry() << 'Finished implementing ' << fhs_elem,
                         OutputEntry() << red_text('Error implementing ') << fhs_elem,
                         [CreateDirectoryTask('$ALPHA_OS_ROOT/bin', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/boot', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/dev', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/etc', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/etc/opt', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/home', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/lib', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/media', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/mnt', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/opt', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/root', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/run', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/sbin', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/srv', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/tmp', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/bin', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/include', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/lib', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/libexec', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/bin', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/etc', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/games', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/include', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/lib', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/man', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/sbin', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/share', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/local/src', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/sbin', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/share', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/usr/src', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var/lib', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var/lock', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var/log', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var/opt', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var/run', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var/spool', False),
                          CreateDirectoryTask('$ALPHA_OS_ROOT/var/tmp', False)])
