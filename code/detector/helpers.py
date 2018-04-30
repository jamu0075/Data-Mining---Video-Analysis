
import os
import sys


def path_module_relative(module_name, path):
    return os.path.join(
        os.path.dirname(sys.modules[module_name].__file__), path
    )
