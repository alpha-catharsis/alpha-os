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
                         [SetEnvironmentVariableTask('ALPHA_OS_ROOT', '/tmp/alpha-os'),
                          SetUmaskTask(0o022),
                          CreateDirectoryTask('$ALPHA_OS_ROOT', False),
                          ImplementFHSTask(),
                          SetEnvironmentVariableTask('ALPHA_TOOLS', '$ALPHA_OS_ROOT/tools'),
                          CreateDirectoryTask('$ALPHA_TOOLS', False),
                          SetEnvironmentVariableTask('ALPHA_BOOTSTRAP', '$ALPHA_OS_ROOT/bootstrap'),
                          CreateDirectoryTask('$ALPHA_BOOTSTRAP', False),
                          ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP'),
                          SetEnvironmentVariableTask('ALPHA_OS_TARGET', 'x86_64-alphaos-linux-gnu'),
                          SetEnvironmentVariableTask('LC_ALL', 'POSIX'),
                          SetEnvironmentVariableTask('PATH', '$ALPHA_OS_ROOT/tools/bin:$PATH'),
                          SetEnvironmentVariableTask('CONFIG_SITE', '$ALPHA_OS_ROOT/usr/share/config.site'),
                          InstallBinutilsPass1Task(),
                          InstallGccPass1Task(),
                          InstallAPIHeadersTask(),
                          InstallGlibcTask(),
                          InstallLibstdcppTask(),
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
                          CreateDirectoryTask('$ALPHA_OS_ROOT/lib64', False),
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
        super().__init__('InstallBinutils',
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
                                                '--target=$ALPHA_OS_TARGET',
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
        super().__init__('InstallGccPass1',
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
                          SedTask('-e \'/m64=/s/lib64/lib/\' -i.orig',
                                  'gcc/config/i386/t-linux64',
                                  'use \'/lib\' in place of \'/lib64\''),
                          CreateDirectoryTask('build', False),
                          ChangeCurrentDirectoryTask('build'),
                          ConfigurePackageTask(['--target=$ALPHA_OS_TARGET',
                                                '--prefix=$ALPHA_TOOLS',
                                                '--with-glibc-version=2.41',
                                                '--with-sysroot=$ALPHA_OS_ROOT',
                                                '--with-newlib',
                                                '--without-headers',
                                                '--enable-default-pie',
                                                '--enable-default-ssp',
                                                '--disable-werror',
                                                '--disable-nls',
                                                '--disable-shared',
                                                '--disable-multilib',
                                                '--disable-threads',
                                                '--disable-libatomic',
                                                '--disable-libgomp',
                                                '--disable-libquadmath',
                                                '--disable-libssp',
                                                '--disable-libvtv',
                                                '--disable-libstdcxx',
                                                '--enable-languages=c,c++']),
                          CompilePackageTask(),
                          InstallPackageTask(),
                          ChangeCurrentDirectoryTask('..'),
                          GenerateLimitsHeaderTask(),
                          ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP')
                          ])

class GenerateLimitsHeaderTask(Task):
    def __init__(self):
        super().__init__('GenerateLimitsHeader')

    def _run(self):
        (success, _, err) = run_shell_cmd(f'cat gcc/limitx.h gcc/glimits.h gcc/limity.h > ' +
                                          '`dirname $($ALPHA_OS_TARGET-gcc -print-libgcc-file-name)`/include/limits.h')
        if not success:
            out = (OutputEntry() << red_text("Failed to generate ") << cyan_text('\'limits.h\'') <<
                   red_text(' header') <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        out = OutputEntry() << "Generated " << cyan_text('\'limits.h\'') << ' header'
        return (True, out)

class InstallAPIHeadersTask(ChainTask):
    def __init__(self):
        kernel_elem = yellow_text('API headers')
        kernel_url = 'https://www.kernel.org/pub/linux/kernel/v6.x/linux-6.14.6.tar.xz'
        kernel_filename = 'linux-6.14.6.tar.xz'
        kernel_dir = 'linux-6.14.6'
        super().__init__('InstallAPIHeaders',
                         OutputEntry() << 'Installing ' << kernel_elem,
                         OutputEntry() << 'Finished installing ' << kernel_elem,
                         OutputEntry() << red_text('Failed installing ') << kernel_elem,
                         [DownloadFileTask(kernel_url, kernel_filename),
                          UnpackArchiveTask(kernel_filename),
                          ChangeCurrentDirectoryTask(kernel_dir),
                          InstallKernelHeadersTask(),
                          ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP'),
                          ])

class InstallKernelHeadersTask(Task):
    def __init__(self):
        super().__init__('InstallKernelHeaders')

    def start_message(self):
        return OutputEntry() << 'Installing kernel headers'

    def end_message(self):
        if self.successful():
            return OutputEntry() << 'Completed installing kernel headers'
        return None

    def _run(self):
        (success, _, err) = run_shell_cmd('make mrproper')
        if success:
            (success, _, err) = run_shell_cmd('make headers')
        if success:
            (success, _, err) = run_shell_cmd('find usr/include -type f ! -name \'*.h\' -delete')
        if success:
            (success, _, err) = run_shell_cmd('cp -rv usr/include $ALPHA_OS_ROOT/usr')
        if not success:
            out = (OutputEntry() << red_text("Failed to install kernel headers ") <<
                   newline() << red_text('Reason: ') << newline() << yellow_text(err.decode('utf-8')))
            return (False, out)
        return (True, None)

class InstallGlibcTask(ChainTask):
    def __init__(self):
        glibc_elem = yellow_text('Glibc')
        glibc_url = 'https://ftp.gnu.org/gnu/glibc/glibc-2.41.tar.xz'
        glibc_filename = 'glibc-2.41.tar.xz'
        glibc_dir = 'glibc-2.41'
        glibc_fhs_patch_url = 'https://www.linuxfromscratch.org/patches/lfs/development/glibc-2.41-fhs-1.patch'
        glibc_fhs_patch_filename = 'glibc-2.41-fhs-1.patch'
        super().__init__('InstallGlibc',
                         OutputEntry() << 'Installing ' << glibc_elem,
                         OutputEntry() << 'Finished installing ' << glibc_elem,
                         OutputEntry() << red_text('Failed installing ') << glibc_elem,
                         [DownloadFileTask(glibc_url, glibc_filename),
                          UnpackArchiveTask(glibc_filename),
                          ChangeCurrentDirectoryTask(glibc_dir),
                          DownloadFileTask(glibc_fhs_patch_url, glibc_fhs_patch_filename),
                          CreateSymlinkTask('ld-linux.so.2', '$ALPHA_OS_ROOT/lib/ld-lsb.so.3'),
                          CreateSymlinkTask('../lib/ld-linux-x86-64.so.2', '$ALPHA_OS_ROOT/lib64'),
                          CreateSymlinkTask('../lib/ld-linux-x86-64.so.2', '$ALPHA_OS_ROOT/lib64/ld-lsb-x86-64.so.3'),
                          ApplyPatchTask('-Np1', glibc_fhs_patch_filename),
                          CreateDirectoryTask('build', False),
                          ChangeCurrentDirectoryTask('build'),
                          ShellTask('GlibcConfigParams',
                                    'echo "rootsbindir=/usr/sbin" > configparms',
                                    'Forced the use of /usr/sbin directory',
                                    red_text('Failed to force the use of /usr/sbin directory')),
                          ConfigurePackageTask(['--prefix=/usr',
                                                '--host=$ALPHA_OS_TARGET',
                                                '--build=$(../scripts/config.guess)',
                                                '--enable-kernel=5.4',
                                                '--disable-nscd',
                                                'libc_cv_slibdir=/usr/lib']),
                          CompilePackageTask(),
                          InstallPackageTask('$ALPHA_OS_ROOT'),
                          SedTask('\'/RTLDLIST=/s@/usr@@g\' -i ',
                                  '$ALPHA_OS_ROOT/usr/bin/ldd',
                                  'fix hard-coded path to the exectuable loader in ldd script'),
                          ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP'),
                          ])

class InstallLibstdcppTask(ChainTask):
    def __init__(self):
        libstdcpp_dir = 'gcc-14.2.0/libstdc++-v3'
        libstdcpp_elem = yellow_text('Libstdcpp')
        super().__init__('InstallLibstdcpp',
                         OutputEntry() << 'Installing ' << libstdcpp_elem,
                         OutputEntry() << 'Finished installing ' << libstdcpp_elem,
                         OutputEntry() << red_text('Failed installing ') << libstdcpp_elem,
                         [ChangeCurrentDirectoryTask(libstdcpp_dir),
                          CreateDirectoryTask('build', False),
                          ChangeCurrentDirectoryTask('build'),
                          ConfigurePackageTask(['--host=$ALPHA_OS_TARGET',
                                                '--build=$(../config.guess)',
                                                '--prefix=/usr',
                                                '--disable-multilib',
                                                '--disable-nls',
                                                '--disable-libstdcxx-pch',
                                                '--with-gxx-include-dir=/tools/$ALPHA_OS_TARGET/include/c++/14.2.0']),
                          CompilePackageTask(),
                          InstallPackageTask('$ALPHA_OS_ROOT'),
                          RemoveFileTask('$ALPHA_OS_ROOT/usr/lib/lib{stdc++{,exp,fs},supc++}.la'),
                          ChangeCurrentDirectoryTask('$ALPHA_BOOTSTRAP'),
                          ])
