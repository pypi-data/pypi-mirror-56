import math
from time import sleep

from sensational.sensors.abstract.i2c import I2CSensor
from sensational.sensors.abstract.i2c import I2CByte
from sensational.sensors.abstract.i2c import I2CBlock
from sensational.sensors.abstract.i2c import I2CShort
from sensational.sensors.abstract.i2c import I2CUShort

from sensational.perceptions import Acceleration
from sensational.perceptions import Magnetism
from sensational.perceptions import Temperature

from sensational.units import u

from .ak8963 import AK8963


class MPU9250(I2CSensor):
    """
    SparkFun IMU Breakout MPU-9250

    Features:
    * 3-axis gyroscope
    * 3-axis accelerometer
    * 3-axis magnetometer
    * thermometer

    Product Page: https://www.sparkfun.com/products/13762

    Getting Started: https://learn.sparkfun.com/tutorials/mpu-9250-hookup-guide
    """

    AccelScale2G = 0x00                     # ±2G over 16 bits
    AccelScale4G = 0x01                     # ±4G over 16 bits
    AccelScale8G = 0x02                     # ±8G over 16 bits
    AccelScale16G = 0x03                    # ±16G over 16 bits

    GyroScale250DPS = 0x00                  # ±250 degrees per second over 16 bits
    GyroScale500DPS = 0x01                  # ±500 degrees per second over 16 bits
    GyroScale1000DPS = 0x02                 # ±1000 degrees per second over 16 bits
    GyroScale2000DPS = 0x03                 # ±2000 degrees per second over 16 bits

    AccelScaleValues = {
        # ±2G over 16 bits
        AccelScale2G: 2 / (2**15),
        # ±4G over 16 bits
        AccelScale4G: 4 / (2**15),
        # ±8G over 16 bits
        AccelScale8G: 8 / (2**15),
        # ±16G over 16 bits
        AccelScale16G: 16 / (2**15)
    }

    GyroScaleValues = {
        # ±250 degrees per second over 16 bits
        GyroScale250DPS: 250 / (2**15),
        # ±500 degrees per second over 16 bits
        GyroScale500DPS: 500 / (2**15),
        # ±1000 degrees per second over 16 bits
        GyroScale1000DPS: 1000 / (2**15),
        # ±2000 degrees per second over 16 bits
        GyroScale2000DPS: 2000 / (2**15),
    }

    DefaultAccelScale = AccelScale2G
    DefaultGyroScale = GyroScale250DPS
    DefaultMagnetometerScale = AK8963.DefaultScale
    DefaultMagnetometerMode = AK8963.DefaultMode

    @classmethod
    def apply_accel_scale(cls, scale, value):
        return cls.AccelScaleValues[scale] * value

    @classmethod
    def apply_gyro_scale(cls, scale, value):
        return cls.GyroScaleValues[scale] * value

    def __init__(self, bus, address=0x68, magnetometer_address=0x0C,
                 accelerometer_scale=DefaultAccelScale, gyroscope_scale=DefaultGyroScale,
                 magnetometer_scale=DefaultMagnetometerScale, magnetometer_mode=DefaultMagnetometerMode):
        I2CSensor.__init__(self, bus, address)

        self.magnetometer_address = magnetometer_address
        self.accelerometer_scale = accelerometer_scale
        self.gyroscope_scale = gyroscope_scale

        self._linear_acceleration = Acceleration()
        self._angular_acceleration = Acceleration()
        self._magnetism = Magnetism()
        self._temperature = Temperature()

        # self.accelerometer = Accelerometer()
        # self.compass = Compass()
        # self.gyroscope = Gyroscope()
        # self.thermometer = Thermometer()

        self.test_connection()
        self.calibrate()
        self.initialize()

        self.magnetometer = self.create_magnetometer(
            bus, magnetometer_address, magnetometer_scale, magnetometer_mode)

    ############################################################################
    # Sensor Data

    @property
    def linear_acceleration(self) -> Acceleration:
        return self._linear_acceleration
    
    @property
    def angular_acceleration(self) -> Acceleration:
        return self._angular_acceleration
    
    @property
    def magnetism(self) -> Magnetism:
        return self._magnetism
    
    @property
    def temperature(self) -> Temperature:
        return self._temperature

    @property
    def data(self):
        return {
            'linear_acceleration': self._linear_acceleration,
            'angular_acceleration': self._angular_acceleration,
            'magnetism': self._magnetism,
            'temperature': self._temperature,
        }

    ############################################################################
    # Registers

    SampleRateDivider = I2CByte(0x19)
    GyroOffsetX = I2CShort(0x13)
    GyroOffsetY = I2CShort(0x15)
    GyroOffsetZ = I2CShort(0x17)
    Config = I2CByte(0x1a)
    GyroConfig = I2CByte(0x1b)
    AccelConfig1 = I2CByte(0x1c)
    AccelConfig2 = I2CByte(0x1d)
    FifoEnable = I2CByte(0x23)
    I2CMasterControl = I2CByte(0x24)
    I2CSlave4Addr = I2CByte(0x31)
    I2CSlave4Reg = I2CByte(0x32)
    I2CSlave4Do = I2CByte(0x33)
    I2CSlave4Ctrl = I2CByte(0x34)
    I2CSlave4Di = I2CByte(0x35)
    InterruptPinConfig = I2CByte(0x37)
    InterruptEnable = I2CByte(0x38)
    InterruptStatus = I2CByte(0x3a)
    AccelOutputX = I2CShort(0x3b)
    AccelOutputY = I2CShort(0x3d)
    AccelOutputZ = I2CShort(0x3f)
    TemperatureOutput = I2CShort(0x41)
    GyroOutputX = I2CShort(0x43)
    GyroOutputY = I2CShort(0x45)
    GyroOutputZ = I2CShort(0x47)
    UserControl = I2CByte(0x6a)
    PowerManagement1 = I2CByte(0x6b)
    PowerManagement2 = I2CByte(0x6c)
    FifoCount = I2CUShort(0x72)
    FifoRW = I2CBlock(0x74, '>6h', 12)
    WhoAmI = I2CByte(0x75)
    AccelOffsetX = I2CShort(0x77)
    AccelOffsetY = I2CShort(0x7a)
    AccelOffsetZ = I2CShort(0x7d)

    ############################################################################
    # Helper Functions

    def _reset(self):
        self.PowerManagement1 = 0x80
        sleep(0.100)

    def _get_stable_time_source(self):
        self.PowerManagement1 = 0x01
        self.PowerManagement2 = 0x00
        sleep(0.200)

    def _enter_bias_calculation_mode(self):
        self.InterruptEnable = 0x00
        self.FifoEnable = 0x00
        self.PowerManagement1 = 0x00
        self.I2CMasterControl = 0x00
        self.UserControl = 0x00
        self.UserControl = 0x0c
        sleep(0.015)

    def _configure_scales(self):
        self.Config = 0x01
        self.SampleRateDivider = 0x00
        self.GyroConfig = self.gyroscope_scale
        self.AccelConfig1 = self.accelerometer_scale

    def _calculate_bias(self):
        self.UserControl = 0x40
        self.FifoEnable = 0x78
        sleep(0.040)
        self.FifoEnable = 0x00
        bytes_read = min(self.FifoCount, 512)
        packet_count = int(math.floor(bytes_read / 12) - 1)

        accel_bias = {'x': [], 'y': [], 'z': []}
        gyro_bias = {'x': [], 'y': [], 'z': []}
        for _ in range(packet_count):
            ax, ay, az, gx, gy, gz = self.FifoRW
            accel_bias['x'].append(ax)
            accel_bias['y'].append(ay)
            accel_bias['z'].append(az)
            gyro_bias['x'].append(gx)
            gyro_bias['y'].append(gy)
            gyro_bias['z'].append(gz)

        # Average accel bias and divide by 8 to get 2048 LSB/g to
        # match expected hardware register input
        for k, v in accel_bias.items():
            accel_bias[k] = (sum(v) / len(v)) / 8

        # Average gyro bias, divide by 4 to get 32.9LSB/deg/s, and
        # reverse sign to match expected hardware register input
        for k, v in gyro_bias.items():
            gyro_bias[k] = int((sum(v) / len(v)) / -4)

        # Read factory accel bias
        accel_bias_factory = {
            'x': self.AccelOffsetX,
            'y': self.AccelOffsetY,
            'z': self.AccelOffsetZ,
        }

        # Apply factory accel bias and temperature flag to accel bias
        for k, v in accel_bias_factory.items():
            temp_flag = v & 0x01
            accel_bias[k] = int(v - accel_bias[k]) | temp_flag

        # Write bias values to registers
        self.AccelOffsetX = accel_bias['x']
        self.AccelOffsetY = accel_bias['y']
        self.AccelOffsetZ = accel_bias['z']
        self.GyroOffsetX = gyro_bias['x']
        self.GyroOffsetY = gyro_bias['y']
        self.GyroOffsetZ = gyro_bias['z']

    ############################################################################
    # Initialization Functions

    def test_connection(self):
        assert (self.WhoAmI == 0x71), "Connection to MPU9250 could not be established"

    def calibrate(self):
        self._reset()
        self._get_stable_time_source()
        self._enter_bias_calculation_mode()
        self._configure_scales()
        self._calculate_bias()

    def initialize(self):
        self.PowerManagement1 = 0x00
        sleep(0.100)

        self.PowerManagement1 = 0x01
        sleep(0.200)

        self.Config = 0x03
        self.SampleRateDivider = 0x04

        # Configure Accelerometer scale
        c = self.AccelConfig1
        c = c & ~0xe0   # Clear self-test
        c = c & ~0x18   # Clear AFS Scale
        c = c | self.AccelScale2G
        self.AccelConfig1 = c

        # Configure Accelerometer sample rate
        c = self.AccelConfig2
        c = c & ~0x0f   # Clear accel_fchoice_b and A_DLPFG
        c = c | 0x03    # Set to sr=1kHz, bw=41Hz
        self.AccelConfig2 = c

        # Configure interrupts and bypass enable
        self.InterruptPinConfig = 0x22
        self.InterruptEnable = 0x01

    def create_magnetometer(self, bus, address, scale=DefaultMagnetometerScale, mode=DefaultMagnetometerMode):
        self.I2CSlave4Addr = 0x80 | address
        self.I2CSlave4Ctrl = 0x00
        self.I2CMasterControl = 0x80
        return AK8963(bus, address, scale, mode)

    ############################################################################
    # Signal Processing

    def _read_accelerometer(self):
        ax = self.apply_accel_scale(
            self.accelerometer_scale, self.AccelOutputX)
        ay = self.apply_accel_scale(
            self.accelerometer_scale, self.AccelOutputY)
        az = self.apply_accel_scale(
            self.accelerometer_scale, self.AccelOutputZ)
        self._linear_acceleration.update(
            u(ax, u.meter / u.second / u.second),
            u(ay, u.meter / u.second / u.second),
            u(az, u.meter / u.second / u.second)
        )

    def _read_temperature(self):
        # Read temp and scale based on chipset values to get ºC
        temp = self.TemperatureOutput / 333.87 + 21.0
        self._temperature.update(
            u(temp, u.celsius)
        )

    def _read_gyroscope(self):
        gx = self.apply_gyro_scale(self.gyroscope_scale, self.GyroOutputX)
        gy = self.apply_gyro_scale(self.gyroscope_scale, self.GyroOutputY)
        gz = self.apply_gyro_scale(self.gyroscope_scale, self.GyroOutputZ)
        self._angular_acceleration.update(
            u(gx, u.degree / u.second / u.second),
            u(gy, u.degree / u.second / u.second),
            u(gz, u.degree / u.second / u.second)
        )

    def _read_magnetometer(self):
        self.magnetometer.update()
        self._magnetism.update(**self.magnetometer.magnetism.data)

    def update(self):
        self._read_accelerometer()
        self._read_temperature()
        self._read_gyroscope()
        self._read_magnetometer()
