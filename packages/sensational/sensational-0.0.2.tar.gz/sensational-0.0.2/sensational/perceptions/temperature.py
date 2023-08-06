class Temperature:
    def __init__(self):
        self._temperature = None

    def update(self, temperature):
        self.temperature = temperature
    
    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def data(self):
        return {'temp': self.temperature}

    def __repr__(self):
        return "<Temperature temp={}>".format(self.temperature)
