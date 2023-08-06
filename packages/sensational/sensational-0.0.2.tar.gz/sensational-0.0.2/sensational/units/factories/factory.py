class UnitsFactory:

    def __init__(self):
        pass

    def __call__(self, qty, unit):
        raise NotImplementedError()

    ##########################################################################
    # DISTANCE

    @property
    def meter(self):
        raise NotImplementedError()

    ##########################################################################
    # TIME

    @property
    def second(self):
        raise NotImplementedError()

    @property
    def minute(self):
        raise NotImplementedError()

    @property
    def hour(self):
        raise NotImplementedError()

    ##########################################################################
    # ANGLE

    @property
    def degree(self):
        raise NotImplementedError()

    ##########################################################################
    # TEMPERATURE

    @property
    def celsius(self):
        raise NotImplementedError()

    ##########################################################################
    # MAGNETIC FIELD

    @property
    def gauss(self):
        raise NotImplementedError()
