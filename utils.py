class PairDict(dict):

    def set_key(self, fromm, to):
        self._key = fromm+'/'+to

    def __getitem__(self, key):
        return self.__dict__[key]

    def add(self, fromm, to, rate):
        self.set_key(fromm, to)
        self.__dict__[self._key] = rate

    def get(self, fromm, to):
        self.set_key(fromm, to)
        return self.__dict__.get(self._key)

    def has_key(self, key):
        return key in self.__dict__.keys()

    def keys(self):
        return self.__dict__.keys()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



