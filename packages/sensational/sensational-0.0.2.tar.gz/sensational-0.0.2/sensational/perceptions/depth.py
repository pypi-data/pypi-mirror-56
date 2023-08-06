class Depth:
    def __init__(self):
        self._depth = None

    def update(self, depth):
        self.depth = depth
    
    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def data(self):
        return {'depth': self.depth}

    def __repr__(self):
        return "<Depth depth={}>".format(self.depth)
