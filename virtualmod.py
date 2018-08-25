import importlib
from importlib.abc import Loader, MetaPathFinder
import sys

__all__ = [
    'MetaVirtualModule',
    'VirtualModule',
    'add_to_module',
    'create_module',
]

# Our virtual module registry
registry = dict()

# Built in module class
module_cls = type(sys)
# Built in module spec class
spec_cls = type(sys.__spec__)


def create_module(module_name):
    """Function for create a new empty virtual module and register it"""
    module = module_cls(module_name)
    setattr(module, '__spec__', spec_cls(name=module_name, loader=VirtualModuleLoader))
    registry[module_name] = module
    return module


def add_to_module(module, name=None):
    """Decorator to register a function or class to a module"""
    def wrapper(value):
        key = name or getattr(value, '__name__', None)
        if key:
            setattr(module, key, value)
        return value
    return wrapper


class VirtualModuleLoader(Loader):
    """Module loader class used for pulling virtual modules from our registry"""
    def create_module(spec):
        if spec.name not in registry:
            return None

        return registry[spec.name]

    def exec_module(module):
        module_name = module.__name__
        if hasattr(module, '__spec__'):
            module_name = module.__spec__.name

        sys.modules[module_name] = module


class VirtualModuleFinder(MetaPathFinder):
    """Module finder to register with sys.meta_path for finding module specs from our registry"""
    def find_spec(fullname, path, target=None):
        if fullname in registry:
            return registry[fullname].__spec__
        return None


class MetaVirtualModule(type):
    """Metaclass used for automatically creating and registering VirtualModule class definitions"""
    def __init__(cls, name, bases, attrs):
        # Initialize the class
        super(MetaVirtualModule, cls).__init__(name, bases, attrs)

        # Do not register our base class
        if name == 'VirtualModule':
            return

        module_name = getattr(cls, '__module_name__', cls.__name__) or name
        # DEV: `create_module` will registry this module for us
        module = create_module(module_name)

        # Copy over class attributes
        for key, value in attrs.items():
            if key in ('__name__', '__module_name__', '__module__', '__qualname__'):
                continue
            setattr(module, key, value)


class VirtualModule(metaclass=MetaVirtualModule):
    """Base virtual module class for creating modules from class definitions"""
    pass


# Push our virtual module finder at the beginning of the sys.meta_path
# DEV: Push in first so we always look for virtual modules first
sys.meta_path.insert(0, VirtualModuleFinder)
