class UnitsProvider:

    def __init__(self, factory):
        self._factory = factory

    def SetFactory(self, factory):
        self._factory = factory

    def __call__(self, qty, unit):
        return self._factory(qty, unit)

    def __getattr__(self, name):
        return getattr(self._factory, name)
