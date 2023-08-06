from numericalunits import m as u_meter
from numericalunits import s as u_second
from numericalunits import minute as u_minute
from numericalunits import hour as u_hour
from numericalunits import G as u_gauss

from .factory import UnitsFactory


class NumericalUnitsUnitsFactory(UnitsFactory):

    def __init__(self):
        pass

    def __call__(self, qty, unit):
        return qty * unit

    ##########################################################################
    # DISTANCE

    @property
    def meter(self):
        return u_meter

    ##########################################################################
    # TIME

    @property
    def second(self):
        return u_second

    @property
    def minute(self):
        return u_minute

    @property
    def hour(self):
        return u_hour

    ##########################################################################
    # ANGLE

    @property
    def degree(self):
        """ Angular Degrees """
        # TODO: Add this if Numerical Units supports it
        raise NotImplementedError()

    ##########################################################################
    # TEMPERATURE

    @property
    def celsius(self):
        # TODO: Add this if Numerical Units supports it
        raise NotImplementedError()

    ##########################################################################
    # MAGNETIC FIELD

    @property
    def gauss(self):
        return u_gauss
