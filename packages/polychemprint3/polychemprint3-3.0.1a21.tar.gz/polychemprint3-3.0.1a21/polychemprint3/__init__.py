import sys, os
import importlib
import pkgutil

sys.path.insert(0, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))

import polychemprint3

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(polychemprint3.__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module

print (__all__)
import __all__
from polychemprint3 import __main__

def main():


    print("h")
    __main__.main()



if __name__ == "__main__":
    main()
