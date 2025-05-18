#!/usr/bin/env python3

from alpha_lib.lang.lang import *

if __name__ == '__main__':
    my_proc_def = ProcDef({'message': str}, [ProcStep('builtin.print', {'message': RefArg('message', RefType.ARG)})] * 3)
    my_mod = Module('my-module', {}, {'greetings': my_proc_def})

    univ = Universe()
    univ.add_builtin_proc_def('print', PrintProcDef())
    univ.load_module(my_mod)

    univ.run_proc('builtin.print', {'message': ImmArg('Hello cruel world!')})
    univ.run_proc('my-module.greetings', {'message': ImmArg('Hello beautiful world!')})

    print('OK')
