# import numpy as np
import smbus
import time
# import pigpio

# from Adafruit_CCS811 import Adafruit_CCS811

CSS811_DEVICE_ADDRESS = 0x5b
CSS811_STATUS = 0x00
CSS811_MEAS_MODE = 0x01
CSS811_ALG_RESULT_DATA = 0x02
CSS811_RAW_DATA = 0x03
CSS811_ENV_DATA = 0x05
CSS811_NTC = 0x06
CSS811_THRESHOLDS = 0x10
CSS811_BASELINE = 0x11
CSS811_HW_ID = 0x20
CSS811_HW_VERSION = 0x21
CSS811_FW_BOOT_VERSION = 0x23
CSS811_FW_APP_VERSION = 0x24
CSS811_ERROR_ID = 0xE0
CSS811_APP_START = 0xF4
CSS811_SW_RESET = 0xFF


CONSTANT_POWER_MODE = 0x10


# def data_available(bus):
#     bus.i2c_read_byte_data(CSS811_DEVICE_ADDRESS, CSS811_STATUS)
#     return value & 1 << 3


def main():
    bus = smbus.SMBus(1)

    #Startup
    try:
        #Write nothing to APP_START register to set the sensor to
        #change the mode of the CCS811 from Boot mode to running the application
        print("Starting the app")
        bus.write_byte(CSS811_DEVICE_ADDRESS, CSS811_APP_START)
        time.sleep(1.02)

        #Recieve the status of the sensor:
        status = bus.read_byte_data(CSS811_DEVICE_ADDRESS, CSS811_STATUS)
        #Firmware mode:
        if (status >> 7) & 1:
            print("Firmware is in application mode. CCS811 is ready to take ADC measurements")
        else:
            print("Firmware is still in boot mode, this allows new firmware to be loaded")

        if (status >> 4) & 1:
            print("Valid application firmware loaded")
        else:
            print("No application firmware loaded")

        if status & 1:
            print("There is an error on the I²C or sensor:")
            print(bus.read_byte_data(CSS811_DEVICE_ADDRESS, CSS811_ERROR_ID))


        print("Setting the mode to constant power mode")
        bus.write_byte_data(CSS811_DEVICE_ADDRESS, CONSTANT_POWER_MODE, CSS811_MEAS_MODE)
        #Recieve the status of the sensor:
        status = bus.read_byte_data(CSS811_DEVICE_ADDRESS, CSS811_STATUS)
        if status & 1:
            print("There is an error on the I²C or sensor:")
            print(bus.read_byte_data(CSS811_DEVICE_ADDRESS, CSS811_ERROR_ID))
            print('exiting...')


        print("Confirming the mode:")
        print(bus.read_byte_data(CSS811_DEVICE_ADDRESS, CSS811_MEAS_MODE))
    except:
        print("Ive done a fuck")

    while True:
        try:
            value = bus.read_byte_data(CSS811_DEVICE_ADDRESS, CSS811_STATUS)
            print(value)
            value = (value >> 3) & 1
            if value :
                x = bus.read_word_data(addr,0x02)
                print(x)

            time.sleep(1.02)
        except:
            print('exiting...')
            break



# class CCS811:
#     def __init__(self):
#         self.pi = pigpio.pi()
#         self.device = self.pi.i2c_open(1, 0x5B)
#         self.tVOC = 0
#         self.CO2 = 0
#
#     def print_error(self):
#         error = self.pi.i2c_read_byte_data(self.device, CSS811_ERROR_ID)
#         message = 'Error: '
#
#         if error & 1 << 5:
#             message += 'HeaterSupply '
#         elif error & 1 << 4:
#             message += 'HeaterFault '
#         elif error & 1 << 3:
#             message += 'MaxResistance '
#         elif error & 1 << 2:
#             message += 'MeasModeInvalid '
#         elif error & 1 << 1:
#             message += 'ReadRegInvalid '
#         elif error & 1 << 0:
#             message += 'MsgInvalid '
#
#         print(message)
#
#     def check_for_error(self):
#         value = self.pi.i2c_read_byte_data(self.device, CSS811_STATUS)
#         return value & 1 << 0
#
#     def app_valid(self):
#         value = self.pi.i2c_read_byte_data(self.device, CSS811_STATUS)
#         return value & 1 << 4
#
#     def set_drive_mode(self, mode):
#         if mode > 4:
#             mode = 4
#
#         setting = self.pi.i2c_read_byte_data(self.device, CSS811_MEAS_MODE)
#         setting &= ~(0b00000111 << 4)
#         setting |= (mode << 4)
#         self.pi.i2c_write_byte_data(self.device, CSS811_MEAS_MODE, setting)
#
#     def configure_ccs811(self):
#         hardware_id = self.pi.i2c_read_byte_data(self.device, CSS811_HW_ID)
#
#         if hardware_id != 0x81:
#             raise ValueError('CCS811 not found. Please check wiring.')
#
#         if self.check_for_error():
#             self.print_error()
#             raise ValueError('Error at Startup.')
#
#         if not self.app_valid():
#             raise ValueError('Error: App not valid.')
#
#         self.pi.i2c_write_byte(self.device, CSS811_APP_START)
#
#         if self.check_for_error():
#             self.print_error()
#             raise ValueError('Error at AppStart.')
#
#         self.set_drive_mode(1)
#
#         if self.check_for_error():
#             self.print_error()
#             raise ValueError('Error at setDriveMode.')
#
#     def setup(self):
#         print('Starting CCS811 Read')
#         self.configure_ccs811()
#
#         result = self.get_base_line()
#
#         print("baseline for this sensor: 0x")
#         if result < 0x100:
#             print('0')
#         if result < 0x10:
#             print('0')
#         print(result)
#
#     def get_base_line(self):
#         a, b = self.pi.i2c_read_i2c_block_data(self.device, CSS811_BASELINE, 2)
#         baselineMSB = b[0]
#         baselineLSB = b[1]
#         baseline = (baselineMSB << 8) | baselineLSB
#         return baseline
#
#     def data_available(self):
#         value = self.pi.i2c_read_byte_data(self.device, CSS811_STATUS)
#         return value & 1 << 3
#
#     def run(self):
#
#         self.setup()
#
#         while True:
#             if self.data_available():
#                 self.read_logorithm_results()
#
#                 print("CO2[%d] tVOC[%d]" % (self.CO2, self.tVOC))
#
#             elif self.check_for_error():
#                 self.print_error()
#
#             time.sleep(1)
#
#     def read_logorithm_results(self):
#         b, d = self.pi.i2c_read_i2c_block_data(self.device, CSS811_ALG_RESULT_DATA, 4)
#
#         co2MSB = d[0]
#         co2LSB = d[1]
#         tvocMSB = d[2]
#         tvocLSB = d[3]
#
#         self.CO2 = (co2MSB << 8) | co2LSB
#         self.tVOC = (tvocMSB << 8) | tvocLSB
#




if __name__ == "__main__":
    main()

    # c = CCS811()
    # c.run()
