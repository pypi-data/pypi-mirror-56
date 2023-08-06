import collections as _coll


class RevDict(_coll.UserDict):
    def __delitem__(self, key):
        value = self.data.pop(key)
        self.data.pop(value)

    def __setitem__(self, key, value):
        if key in self:
            del self[self[key]]
        if value in self:
            del self[value]
        self.data[key] = value
        self.data[value] = key

    def __getattr__(self, item):
        if item in self:
            return self[item]
        else:
            raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {item!r}')
