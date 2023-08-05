import sys, os
import importlib
import pkgutil

sys.path.insert(0, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
import polychemprint3

from polychemprint3 import __main__
from polychemprint3 import tools, sequence, axes, commandLineInterface, user, utility
from tools import *
from sequence import *
from axes import *
from commandLineInterface import *
from user import *
from utility import *

def main():
    __main__.main()
if __name__ == "__main__":
    main()
