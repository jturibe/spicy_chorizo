import smbus
import time

bus = smbus.SMBus(1)
bus.write_byte(0x40, 0xF5)
time.sleep(2)
print(bus.read_byte(0x40))
