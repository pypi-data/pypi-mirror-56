import pint

from .factory import UnitsFactory


class PintUnitsFactory(UnitsFactory):

    def __init__(self):
        self._reg = pint.UnitRegistry()
        self._q = self._reg.Quantity

    def __call__(self, qty, unit):
        return self._q(qty, unit)

    ##########################################################################
    # DISTANCE

    @property
    def meter(self):
        return self._reg.meter

    ##########################################################################
    # TIME

    @property
    def second(self):
        return self._reg.second

    @property
    def minute(self):
        return self._reg.minute

    @property
    def hour(self):
        return self._reg.hour

    ##########################################################################
    # ANGLE

    @property
    def degree(self):
        """ Angular Degrees """
        return self._reg.degree

    ##########################################################################
    # TEMPERATURE

    @property
    def celsius(self):
        return self._reg.degC

    ##########################################################################
    # MAGNETIC FIELD

    @property
    def gauss(self):
        return self._reg.gauss
