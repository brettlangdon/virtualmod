virtualmod
==========
Python package for creating and importing virtual modules.

## Install

```bash
pip install virtualmod
```

## Examples
### Module object
Manually creating and registering a module with `virtualmod`.

```python
import virtualmod

# Create a new empty virtual module
module = virtualmod.create_module('custom_module')

# Add attribute to module
module.key = 'value'


# Use decorator to add a function to the module
# NOTE: You can use `add_to_module(module, name='new_name')` to override the module attribute name
@virtualmod.add_to_module(module)
def module_function(name):
    print('Hello', name)


# Use decorator to add a class to the module
@virtualmod.add_to_module(module)
class ModuleClass:
    pass


# Import and use our virtual module
import custom_module

print('Key:', custom_module.key)
custom_module.module_function('virtualmod')
print(custom_module.ModuleClass())
```

### Class definition
`virtualmod` also comes with the ability to use class definitions to define virtual modules.

```python
import virtualmod


# Use class definition to define our virtual module "custom_module"
class CustomModule(virtualmod.VirtualModule):
    # Define the module's name (would be "CustomModule" otherwise)
    __module_name__ = 'custom_module'

    # Add an attribute
    key = 'value'

    # Add a function
    # NOTE: There is no `cls` or `self`
    def module_function(name):
        print('Hello', name)

    # Add a class to the module
    class ModuleClass:
        pass


# Import and use our virtual module
import custom_module

print('Key:', custom_module.key)
custom_module.module_function('virtualmod')
print(custom_module.ModuleClass())
```

### Override an existing module
`virtualmod`'s module finder is registered before the standard builtin finders.
This means if you register a module under a name of an existing module yours would be found and loaded first

```python
import virtualmod

# Create a virtual module under the name "socket"
my_socket = virtualmod.create_module('socket')

# Import socket module
import socket

# Test if the loaded socket module is the one we created
print(socket is my_socket)
```
