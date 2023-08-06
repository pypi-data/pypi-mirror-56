import struct


class I2CSensor:

    def __init__(self, bus, address):
        self._bus = bus
        self._address = address

    @property
    def bus(self):
        return self._bus

    @property
    def address(self):
        return self._address


class I2CByte:
    def __init__(self, register_address):
        self._register_address = register_address

    def __get__(self, instance: I2CSensor, owner) -> int:
        return instance.bus.read_byte_data(instance.address, self._register_address)

    def __set__(self, instance: I2CSensor, value: int):
        instance.bus.write_byte_data(
            instance.address, self._register_address, value)


class I2CBlock:
    def __init__(self, register_address, block_format, block_length):
        self._register_address = register_address
        self._block_format = block_format
        self._block_length = block_length

    def __get__(self, instance: I2CSensor, owner) -> tuple:
        byte_list = instance.bus.read_i2c_block_data(
            instance.address, self._register_address, self._block_length)
        return struct.unpack(self._block_format, bytes(byte_list))

    def __set__(self, instance: I2CSensor, value: list):
        byte_data = struct.pack(self._block_format, *value)
        instance.bus.write_i2c_block_data(
            instance.address, self._register_address, byte_data)


class I2CShort(I2CBlock):
    def __init__(self, register_address, big_endian=True):
        block_format = ['<h', '>h'][big_endian]
        I2CBlock.__init__(self, register_address, block_format, 2)

    def __get__(self, instance: I2CSensor, owner) -> int:
        return I2CBlock.__get__(self, instance, owner)[0]

    def __set__(self, instance: I2CSensor, value: int):
        return I2CBlock.__set__(self, instance, [value])


class I2CUShort(I2CBlock):
    def __init__(self, register_address, big_endian=True):
        block_format = ['<H', '>H'][big_endian]
        I2CBlock.__init__(self, register_address, block_format, 2)

    def __get__(self, instance: I2CSensor, owner) -> int:
        return I2CBlock.__get__(self, instance, owner)[0]

    def __set__(self, instance: I2CSensor, value: int):
        return I2CBlock.__set__(self, instance, [value])
