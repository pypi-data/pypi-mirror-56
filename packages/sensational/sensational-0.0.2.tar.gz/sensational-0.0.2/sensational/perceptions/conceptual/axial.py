class AxialPerception:
    """
    An abstract perception which operates in three axes.
    """

    def __init__(self):
        self._x = None
        self._y = None
        self._z = None

    def update(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @z.setter
    def z(self, value):
        self._z = value

    @property
    def data(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def __repr__(self):
        return "<AxialPerception x={} y={} z={}>".format(self.x, self.y, self.z)
