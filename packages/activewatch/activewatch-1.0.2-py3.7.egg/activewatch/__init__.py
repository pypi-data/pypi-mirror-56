__version__ = '1.0.2'

from enum import Enum
from importlib import import_module

class NoValue(Enum):
     def __repr__(self):
         return '<%s.%s>' % (self.__class__.__name__, self.name)

from activewatch.service import Service

def client(service_name, session, *args, **kwargs):

    try:
        if '.' in service_name:
            module_name, class_name = service_name.rsplit('.', 1)
        else:
            module_name = service_name
            class_name = service_name.capitalize()

        service_module = import_module('.' + module_name, package='activewatch.services')
        service_class = getattr(service_module, class_name)
        service_instance = service_class(session, *args, **kwargs)

    except (AttributeError, AssertionError, ModuleNotFoundError):
        raise ImportError('{} is not part of our service collection!'.format(service_name))
    else:
        if not issubclass(service_class, Service):
            raise ImportError("We currently don't have {}, but you are welcome to send in the PR for it!".format(
                                                                                                        service_name))

    return service_instance
