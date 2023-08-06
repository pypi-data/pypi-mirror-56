from time import sleep

from sensational.sensors.abstract.i2c import I2CSensor
from sensational.sensors.abstract.i2c import I2CByte
from sensational.sensors.abstract.i2c import I2CBlock
from sensational.sensors.abstract.i2c import I2CShort
from sensational.sensors.abstract.i2c import I2CUShort

from sensational.perceptions import Magnetism

from sensational.units import u


class AK8963(I2CSensor):

    Scale14Bits = 0x00              # 0.6 mG per LSB ~= ±9.8 gauss
    Scale16Bits = 0x01              # 0.15 mG per LSB ~= ±9.8 gauss

    Mode8Hz = 0x02
    Mode100Hz = 0x06

    ScaleValues = {
        Scale14Bits: 0.0006,        # 0.6 mG per LSB
        Scale16Bits: 0.00015,       # 0.15 mG per LSB
    }

    DefaultScale = Scale16Bits
    DefaultMode = Mode8Hz

    @classmethod
    def apply_scale(cls, scale, value):
        return cls.ScaleValues[scale] * value

    def __init__(self, bus, address=0x0c, scale=DefaultScale, mode=DefaultMode):
        I2CSensor.__init__(self, bus, address)
        self._scale = scale
        self._mode = mode
        self._magnetism = Magnetism()
        self.test_connection()
        self.initialize()

    ############################################################################
    # Sensor Data

    @property
    def magnetism(self) -> Magnetism:
        return self._magnetism
    
    @property
    def data(self):
        return self.magnetism

    ############################################################################
    # Registers

    WhoAmI = I2CByte(0x00)
    Info = I2CByte(0x01)
    Status1 = I2CByte(0x02)
    OutputX = I2CShort(0x03, big_endian=True)
    OutputY = I2CShort(0x05, big_endian=True)
    OutputZ = I2CShort(0x07, big_endian=True)
    Status2 = I2CByte(0x09)
    Control = I2CByte(0x0a)
    ASTC = I2CByte(0x0c)

    CalibrationX = I2CByte(0x10)
    CalibrationY = I2CByte(0x11)
    CalibrationZ = I2CByte(0x12)

    ############################################################################
    # Helper Functions

    def _reset(self):
        self.Control = 0x00
        sleep(0.010)

    # TODO: Work on Bias Calculations
    # def _calculate_bias(self):
    #     self.Control = 0x0f   # Enter Fuse ROM access mode
    #     sleep(0.010)

    #     # Read factory calibration values
    #     x = self.CalibrationX
    #     y = self.CalibrationY
    #     z = self.CalibrationZ

    def _configure_mode(self):
        control = (self._scale << 4) | self._mode
        self.Control = control
        sleep(0.010)

    def end_read(self):
        # Read from status2 to signal chip that read is done
        # Value is unused beyond this, but retrieval is required
        _ = self.Status2

    ############################################################################
    # Helper Properties

    @property
    def data_ready(self):
        return self.Status1 & 0x01

    ############################################################################
    # Initialization Functions

    def test_connection(self):
        assert (self.WhoAmI == 0x48), "Connection to AK8963 could not be established"

    def initialize(self):
        self._reset()
        # self._calculate_bias()
        self._configure_mode()

    ############################################################################
    # Signal Processing

    def update(self):
        if self.data_ready:
            mx = self.apply_scale(self._scale, self.OutputX)
            my = self.apply_scale(self._scale, self.OutputY)
            mz = self.apply_scale(self._scale, self.OutputZ)
            self.end_read()
            self._magnetism.update(
                u(mx, u.gauss),
                u(my, u.gauss),
                u(mz, u.gauss)
            )
