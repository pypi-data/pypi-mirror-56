import sys, os
import importlib
import pkgutil

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages():
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module

import __all__
from polychemprint3 import __main__

def main():

    sys.path.insert(0, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))

    __main__.main()
    print("h")


if __name__ == "__main__":
    main()
