from .conceptual import AxialPerception


class Magnetism(AxialPerception):

    def __repr__(self):
        return "<Magnetism x={} y={} z={}>".format(self.x, self.y, self.z)
