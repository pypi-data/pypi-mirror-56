#TODO enum type

from . import dirs
from . import storage


class SmartObject(object):

    def load_property_map(self, property_map=None):
        if not hasattr(self, '_property_map'):
            self._property_map = {}
        if isinstance(property_map, dict):
            self._property_map.update(property_map)
        else:
            import yaml
            fname = f'{dirs.property_maps_dir}/{property_map}' if \
                    property_map.find('/') == -1 else property_map
            with open(fname) as fh:
                self._property_map.update(yaml.load(fh))

    def apply_property_map(self):
        self._serialize_map = {None: []}
        self._primary_key_field = None
        self._deleted = False
        self._modified = {None: True}
        self._storages = set()
        for i, v in self._property_map.items():
            if v is None:
                v = {}
                self._property_map[i] = {}
            if 'type' in v:
                tp = v['type']
                if tp is not None:
                    v['type'] = eval(tp) if isinstance(tp, str) else tp
            if v.get('pk') is True:
                if self._primary_key_field is not None:
                    raise RuntimeError('Multiple primary keys defined')
                else:
                    self._primary_key_field = i
            if not hasattr(self, i):
                setattr(self, i, v.get('default'))
            self._serialize_map[None].append(i)
            ser = v.get('serialize')
            if 'store' in v and v['store'] is not False:
                storage_id = v['store']
                if storage_id is True:
                    storage_id = None
                    v['store'] = None
                self._modified[storage_id] = True
                self._storages.add(storage_id)
            if ser:
                for s in ser if isinstance(ser, list) else [ser]:
                    self._serialize_map.setdefault(s, []).append(i)

    def set_prop(self, key=None, value=None, save=False, sync=True):
        print(value)
        """
        Set object property by key/value

        To set multiple properties at once, specify value as dict

        Args:
            key: object property key
            value: object property value
            save: auto-save object if properties were modified
            sync: sync object if properties were modified

        Returns:
            True if property is set, False if unchanged

        Raises:
            AttributeError: if no such property or property is read-only
            ValueError: if property value is invalid or no key specified
        """

        # TODO: log set prop
        cerr = f'for objects of class "{self.__class__.__name__}"'
        if isinstance(value, dict):
            result = False
            for i, v in value.items():
                result = self.set_prop(i, v, save=False) or result
            if result is True and save:
                self.save()
            return result
        else:
            if key is None:
                raise ValueError('key is not specified')
            if not isinstance(key, str):
                raise ValueError('key should be string')
            p = self._property_map.get(key)
            if p is None:
                raise AttributeError(f'no such property: "{key}" {cerr}')
            if 'type' in p:
                tp = p.get('type')
                if tp is None:
                    raise AttributeError(
                        f'property "{key}" is read-only {cerr}')
                try:
                    if value is not None and type(value) is not tp:
                        if tp == str:
                            value = str(value)
                        elif tp == int or tp == float:
                            try:
                                value = tp(value)
                            except ValueError:
                                if p.get('accept-hex'):
                                    value = int(value, 16)
                                else:
                                    raise
                        else:
                            raise ValueError
                except ValueError:
                    raise ValueError(f'invalid value: {key}="{value}" {cerr}')
            if getattr(self, key) != value:
                setattr(self, key, value)
                if 'store' in p:
                    storage_id = p['store']
                    if storage_id is True: storage_id = None
                    self._modified[storage_id] = True
                # TODO: set default if value is None
                # TODO: val to boolean
                if save: self.save()
                return True
            return False

    def serialize(self, mode=None):
        return {key: getattr(self, key) for key in self._serialize_map[mode]}

    def load(self):
        for storage_id in self._storages:
            self.set_prop(value=storage.get_storage(storage_id).load(
                pk=getattr(self, self._primary_key_field)))
            self._modified[storage_id] = False

    def save(self, force=False):
        for storage_id in self._modified:
            if self._modified[storage_id] or force:
                storage.get_storage(storage_id).save(
                    pk=getattr(self, self._primary_key_field),
                    data={
                        key: getattr(self, key)
                        for key, props in self._property_map.items()
                        if 'store' in props and props['store'] == storage_id
                    })
                self._modified[storage_id] = False

    def delete(self):
        if not self._deleted:
            self._deleted = True
            for storage_id in self._storages:
                storage.get_storage(storage_id).delete(
                    getattr(self, self._primary_key_field))

    @property
    def deleted(self):
        return self._deleted
