

class DotDict(dict):
    def __getattr__(self, attr):
        if attr not in self:
            self[attr] = None
        return self[attr]

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            value = DotDict(value)
        self[key] = value

    def __delattr__(self, key):
        del self[key]
