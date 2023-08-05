__author__ = ['Miguel Ramos Pernas']
__email__ = ['miguel.ramos.pernas@cern.ch']


# Python
import importlib
import inspect
import os
import pkgutil


PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))


__all__ = ['PACKAGE_PATH']

for loader, module_name, ispkg in pkgutil.walk_packages(__path__):

    if module_name.endswith('setup') or module_name.endswith('__'):
        continue

    # Import all classes and functions
    mod = importlib.import_module('.' + module_name, package='hep_spt.stats')

    __all__ += mod.__all__

    for n, c in inspect.getmembers(mod):
        if n in mod.__all__:
            globals()[n] = c


__all__ = list(sorted(__all__))
