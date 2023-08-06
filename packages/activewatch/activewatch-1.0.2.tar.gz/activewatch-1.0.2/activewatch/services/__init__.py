from ..service import Service
from importlib import import_module
import pkgutil
import os
import sys

"""

"""

for (_, name, _) in pkgutil.iter_modules([os.path.dirname(__file__)]):
    imported_module = import_module('.' + name, package='activewatch.services')

    class_name = list(filter(lambda x: x != 'Service' and not x.startswith('__'),
                             dir(imported_module)))

    service_class = getattr(imported_module, class_name[0])

    if issubclass(service_class, Service):
        setattr(sys.modules[__name__], name, service_class)
