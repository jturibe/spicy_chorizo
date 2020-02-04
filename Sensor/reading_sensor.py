import numpy as np
import smbus

DEVICE_ADDRESS = 0x5b

if __name__ == "__main__":
     bus = smbus.SMBus(1)

     while True:
         data = bus.read_byte(DEVICE_ADDRESS)
         print(data)
     
