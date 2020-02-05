import smbus
import time

bus = smbus.SMBus(1)
while True:
    # bus.write_byte(0x40, 0xF5)
    # time.sleep(2)
    # print("Humidity: ",  bus.read_i2c_block_data(0x40, 0xE7,2))
    bus.write_byte(0x40, 0xE3)
    time.sleep(2)
    print("Temperature: ", bus.read_i2c_block_data(0x40, 0xE3,2))
