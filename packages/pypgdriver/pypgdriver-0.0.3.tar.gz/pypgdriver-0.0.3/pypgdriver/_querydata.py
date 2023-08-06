class _QeryData(dict):

    def __init__(self, data):
        super(_QeryData, self).__init__(data.items())

    def __getattr__(self, name):
        return super(_QeryData, self).__getitem__(name)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('Key must be string.')
        return super(_QeryData, self).__setitem__(key, value)

    def __getitem__(self, key):
        return super(_QeryData, self).__getitem__(key)
