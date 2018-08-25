import importlib
from importlib.abc import Loader, MetaPathFinder
import sys

registry = dict()

module_cls = type(sys)
spec_cls = type(sys.__spec__)


class VirtualModule:
    __slots__ = ['name', 'module', 'spec']

    def __init__(self, name):
        self.name = name
        self.module = module_cls(name)
        self.spec = spec_cls(name=name, loader=VirtualModuleLoader)
        setattr(self.module, '__spec__', self.spec)

    def set_attribute(self, name, value):
        setattr(self.module, name, value)

    def delete_attribute(self, name):
        delattr(self.module, name)


def create_module(name):
    module = VirtualModule(name)
    registry[name] = module
    return module


def copy_module(module):
    name = module.__name__
    if hasattr(module, '__spec__'):
        name = module.__spec__.name

    virt_mod = VirtualModule(name)
    for key, value in module.__dict__.items():
        if key in ('__spec__', '__name__', '__loader__', '__package__'):
            continue
        virt_mod.set_attribute(key, value)

    registry[name] = virt_mod
    importlib.reload(module)
    return virt_mod


def as_module(cls_or_name):
    if isinstance(cls_or_name, str):
        cls = None
        name = cls_or_name
    elif isinstance(cls_or_name, type):
        cls = cls_or_name
        name = getattr(cls, '__module_name__', cls.__name__)
    else:
        raise ValueError('Expected as_module to be passed a string or a class type')

    def wrapper(cls):
        module = create_module(name)

        for key, value in cls.__dict__.items():
            if key.startswith('__') and key.endswith('__'):
                continue

            module.set_attribute(key, value)
        return module

    if cls is None:
        return wrapper
    return wrapper(cls)


class VirtualModuleLoader(Loader):
    def create_module(spec):
        if spec.name not in registry:
            return None

        return registry[spec.name].module

    def exec_module(module):
        module_name = module.__name__
        if hasattr(module, '__spec__'):
            module_name = module.__spec__.name

        sys.modules[module_name] = module


class VirtualModuleFinder(MetaPathFinder):
    def find_spec(fullname, path, target=None):
        if fullname in registry:
            return registry[fullname].spec
        return None


sys.meta_path.insert(0, VirtualModuleFinder)
