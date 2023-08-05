from . import dirs

import importlib
from functools import partial

storages = {}


def define_storage(storage, id=None):
    storages[id] = storage


def get_storage(id=None):
    try:
        return storages[id]
    except KeyError:
        raise RuntimeError(f'Storage "{id}" is not defined')


class DummyStorage:

    def load(self, *args, **kwargs):
        return {}

    def save(self, *args, **kwargs):
        return True

    def delete(self, *args, **kwargs):
        return True


class _AbstractFileStorage:

    def __init__(self):
        self.dir = None
        self.ext = 'dat'
        self.binary = False
        self.empty_nofile = True

    def save(self, pk, data={}):
        with open((self.dir if self.dir is not None else dirs.storage_dir) +
                  '/' + pk.replace('/', '___') + '.' + self.ext,
                  'w' + ('b' if self.binary else '')) as fh:
            fh.write(self.dumps(data))
        return True

    def load(self, pk, data={}):
        try:
            with open((self.dir if self.dir is not None else dirs.storage_dir) +
                      '/' + pk.replace('/', '___') + '.' + self.ext,
                      'r' + ('b' if self.binary else '')) as fh:
                return self.loads(fh.read())
        except FileNotFoundError:
            if self.empty_nofile: return {}
            raise

    def delete(self, pk):
        # TODO - do not delete files instantly
        import os
        try:
            os.unlink((self.dir if self.dir is not None else dirs.storage_dir) +
                      '/' + pk.replace('/', '___') + '.' + self.ext)
            return True
        except:
            return False


class JSONStorage(_AbstractFileStorage):

    def __init__(self, pretty=False):
        super().__init__()
        self.ext = 'json'
        try:
            j = importlib.import_module('rapidjson')
        except:
            j = importlib.import_module('json')
        self.loads = j.loads
        self.dumps = partial(j.dumps, indent=4,
                             sort_keys=True) if pretty else j.dumps


class YAMLStorage(_AbstractFileStorage):

    def __init__(self, pretty=False):
        super().__init__()
        self.ext = 'yml'
        yaml = importlib.import_module('yaml')
        self.loads = yaml.load
        self.dumps = partial(yaml.dump, default_flow_style=not pretty)


class PickleStorage(_AbstractFileStorage):

    def __init__(self):
        super().__init__()
        self.ext = 'p'
        self.binary = True
        pickle = importlib.import_module('pickle')
        self.loads = pickle.loads
        self.dumps = pickle.dumps


class MessagePackStorage(_AbstractFileStorage):

    def __init__(self):
        super().__init__()
        self.ext = 'msgpack'
        self.binary = True
        self.msgpack = importlib.import_module('msgpack')
        self.loads = partial(self.msgpack.loads, raw=False)

    def dumps(self, data):
        return self.msgpack.Packer(use_bin_type=True).pack(data)


# TODO: db storage
