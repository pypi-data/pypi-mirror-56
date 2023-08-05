__version__ = '0.0.1'

from . import dirs

from .smartobject import SmartObject

from .storage import get_storage, define_storage, DummyStorage
from .storage import JSONStorage, YAMLStorage, PickleStorage, MessagePackStorage
