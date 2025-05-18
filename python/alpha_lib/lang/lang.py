from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

@dataclass
class Module:
    name: str
    consts: dict[str, any]
    proc_defs: dict[str, ProcDef]

@dataclass
class ProcDef:
    params: dict[str, type]
    steps: list[ProcStep] | NoneType

@dataclass
class ImmArg:
    val: any

class RefType(Enum):
    CONST = 0
    ARG = 1

@dataclass
class RefArg:
    name: str
    ref_type : RefType

@dataclass
class ProcStep:
    qual_proc_name: str
    args: dict[str, ImmArg | RefArg]

class Universe:
    def __init__(self) -> None:
        self.modules: dict[str, Module] = {}
        self.builtin_proc_defs: dict[str, ProcDef] = {}

    def add_builtin_proc_def(self, proc_def_name: str, proc_def: ProcDef) -> None:
        self.builtin_proc_defs[proc_def_name] = proc_def

    def load_module(self, module: Module) -> None:
        if module.name in self.modules:
            raise RuntimeError(f'module \'{module.name}\' loaded twice')
        self.modules[module.name] = module

    def proc_def(self, qualified_name: str) -> (ProcDef, Module | NoneType):
        (module_name, proc_def_name) = qualified_name.split(".", 1)
        if module_name == 'builtin':
            builtin_proc_def = self.builtin_proc_defs.get(proc_def_name)
            if builtin_proc_def is None:
                raise RuntimeError(f'unknown builtin proc def \'{proc_def_name}\'')
            return (builtin_proc_def, None)
        else:
            module: Module = self.modules.get(module_name)
            if module is None:
                raise RuntimeError(f'unknown module \'{module_name}\'')
            proc_def = module.proc_defs.get(proc_def_name)
            if proc_def is None:
                raise RuntimeError(f'unknown proc def \'{proc_def_name}\' in module \'{module_name}\'')
            return (proc_def, module)

    def run_proc(self, qual_proc_name: str, args: dict[str, ImmArg | RefArg], proc: Proc | NoneType=None) -> None:
        (proc_def, module) =  self.proc_def(qual_proc_name)
        reified_args: dic[str, any] = reify_args(proc, proc_def.params, args)
        if module is None:
            proc_def.run(self, reified_args)
        else:
            Proc(module, proc_def, reified_args).run(self)


def reify_args(proc: Proc, params: dict[str, type], args: dict[str, ImmArg | RefArg]) -> dict[str, any]:
        reified_args: dict[str, any] = {}
        for param_name, param_ty in params.items():
            if param_name not in args:
                raise RuntimeError(f'parameter \'{param_name}\' not provided')
            arg = args[param_name]
            if isinstance(arg, ImmArg):
                arg_val = arg.val
            else:
                if arg.ref_type == RefType.CONST:
                    arg_val = proc.module.consts.get(arg.name)
                    if arg_val is None:
                        raise RuntimeError(f'reference to unexisitng constant \'{arg.name}\'')
                elif arg.ref_type == RefType.ARG:
                    arg_val = proc.args.get(param_name)
                    if arg_val is None:
                        raise RuntimeError(f'reference to unexisitng argument \'{arg.name}\'')
                else:
                    raise SystemError('BUG!')
            if not isinstance(arg_val, param_ty):
                raise RuntimeError(f'type mismatch for parameter \'{param_name}\', ' +
                                   f'expected a \'{param_ty}\' but provided a \'{type(arg_val)}')
            reified_args[param_name] = arg_val
        for arg_name in args.keys():
            if arg_name not in params:
                raise RuntimeError(f'provided unrequired argument  \'{arg_name}\'')
        return reified_args

class Proc:
    def __init__(self, module: Module, proc_def: ProcDef, args: dict[str, ImmArg | RefArg]) -> None:
        self.module = module
        self.proc_def = proc_def
        self.args = args
        self.vars = {}

    def run(self, universe: Universe) -> None:
        for step in self.proc_def.steps:
            universe.run_proc(step.qual_proc_name, step.args, self)

class PrintProcDef(ProcDef):
    def __init__(self):
        super().__init__({'message': str}, [])

    def run(self, universe: Universe, args: dict[str, any]) -> None:
        print(args['message'])
