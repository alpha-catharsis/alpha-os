import os.path
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
                          SetEnvironmentVariableTask('ALPHA_TOOLS', '$ALPHA_OS_ROOT/tools'),
                          CreateDirectoryTask('$ALPHA_TOOLS', False),
                          SetEnvironmentVariableTask('ALPHA_BOOTSTRAP', '$ALPHA_OS_ROOT/bootstrap'),
                          CreateDirectoryTask('$ALPHA_BOOTSTRAP', False),
                          ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP'),
                          # InstallBinutilsPass1Task()
                          InstallGccPass1Task()
                          ])

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

class InstallBinutilsPass1Task(ChainTask):
    def __init__(self):
        binutils_elem = yellow_text('binutils (pass 1)')
        binutils_url = 'https://sourceware.org/pub/binutils/releases/binutils-2.44.tar.xz'
        binutils_filename = 'binutils-2.44.tar.xz'
        binutils_dir = 'binutils-2.44'
        super().__init__('BootstrapAlphaOS',
                         OutputEntry() << 'Installing ' << binutils_elem,
                         OutputEntry() << 'Finished installing ' << binutils_elem,
                         OutputEntry() << red_text('Failed installing ') << binutils_elem,
                         [DownloadFileTask(binutils_url, binutils_filename),
                          UnpackArchiveTask(binutils_filename),
                          ChangeCurrentDirectoryTask(binutils_dir),
                          CreateDirectoryTask('build', False),
                          ChangeCurrentDirectoryTask('build'),
                          ConfigurePackageTask(['--prefix=$ALPHA_TOOLS',
                                                '--with-sysroot=$ALPHA_OS_ROOT',
                                                '--target=x86_64-pc-linux',
                                                '--disable-nls',
                                                '--enable-gprofng=no',
                                                '--disable-werror',
                                                '--enable-new-dtags',
                                                '--enable-default-hash-style=gnu']),
                          CompilePackageTask(),
                          InstallPackageTask(),
                          ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP'),
                          ])

class InstallGccPass1Task(ChainTask):
    def __init__(self):
        gcc_elem = yellow_text('gcc (pass 1)')
        gcc_url = 'https://ftp.gnu.org/gnu/gcc/gcc-14.2.0/gcc-14.2.0.tar.xz'
        gcc_filename = 'gcc-14.2.0.tar.xz'
        gcc_dir = 'gcc-14.2.0'
        mpfr_url = 'https://ftp.gnu.org/gnu/mpfr/mpfr-4.2.2.tar.xz'
        mpfr_filename = 'mpfr-4.2.2.tar.xz'
        mpfr_dir = 'mpfr-4.2.2'
        gmp_url = 'https://ftp.gnu.org/gnu/gmp/gmp-6.3.0.tar.xz'
        gmp_filename = 'gmp-6.3.0.tar.xz'
        gmp_dir = 'gmp-6.3.0'
        mpc_url = 'https://ftp.gnu.org/gnu/mpc/mpc-1.3.1.tar.gz'
        mpc_filename = 'mpc-1.3.1.tar.gz'
        mpc_dir = 'mpc-1.3.1'
        super().__init__('BootstrapAlphaOS',
                         OutputEntry() << 'Installing ' << gcc_elem,
                         OutputEntry() << 'Finished installing ' << gcc_elem,
                         OutputEntry() << red_text('Failed installing ') << gcc_elem,
                         [DownloadFileTask(gcc_url, gcc_filename),
                          UnpackArchiveTask(gcc_filename),
                          ChangeCurrentDirectoryTask(gcc_dir),
                          DownloadFileTask(mpfr_url, mpfr_filename),
                          UnpackArchiveTask(mpfr_filename),
                          MoveFileTask(mpfr_dir, 'mpfr'),
                          DownloadFileTask(gmp_url, gmp_filename),
                          UnpackArchiveTask(gmp_filename),
                          MoveFileTask(gmp_dir, 'gmp'),
                          DownloadFileTask(mpc_url, mpc_filename),
                          UnpackArchiveTask(mpc_filename),
                          MoveFileTask(mpc_dir, 'mpc'),
                          # CreateDirectoryTask('build', False),
                          # ChangeCurrentDirectoryTask('build'),
                          # ConfigurePackageTask(['--prefix=$ALPHA_TOOLS',
                          #                       '--with-sysroot=$ALPHA_OS_ROOT',
                          #                       '--target=x86_64-pc-linux',
                          #                       '--disable-nls',
                          #                       '--enable-gprofng=no',
                          #                       '--disable-werror',
                          #                       '--enable-new-dtags',
                          #                       '--enable-default-hash-style=gnu']),
                          # CompilePackageTask(),
                          # InstallPackageTask(),
                          # ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP'),
                          ])
