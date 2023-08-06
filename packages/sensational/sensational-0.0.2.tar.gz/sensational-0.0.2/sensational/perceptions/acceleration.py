from .conceptual import AxialPerception


class Acceleration(AxialPerception):
    def __repr__(self):
        return "<Acceleration x={} y={} z={}>".format(self.x, self.y, self.z)
