import smbus
import time

bus = smbus.SMBus(1)
while True:
    bus.write_byte(0x40, 0xE5)
    time.sleep(2)
    hmb, hlb = bus.read_i2c_block_data(0x40, 0xE5,2)
    hmb = hmb << 8
    hum = 125*(hmb + hlb) / 65536 - 6
    print("RH% = ", hum)
    bus.write_byte(0x40, 0xE3)
    time.sleep(2)
    mb, lb, cm = bus.read_i2c_block_data(0x40, 0xE3, 3)
    mb = mb << 8
    temp = (mb + lb)*175.72 / 65536 - 46.85
    print("Temperature(Celsius): ", temp)
