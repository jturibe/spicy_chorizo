import smbus
import time
import json
import paho.mqtt.client as mqtt
import ssl

bus = smbus.SMBus(1)

client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key", tls_version=ssl.PROTOCOL_TLSv1_2)
con_code = client.connect("test.mosquitto.org",port=8884)

if not con_code:
    msg_info = client.publish("IC.embedded/spicy_chorizo/test","hello")
    print("Message published:", mqtt.error_string(msg_info.rc))
else:
    print(mqtt.error_string(con_code))

#power on light sensor:
bus.write_byte(0x39, 0x80)
bus.write_byte(0x39, 0x3)
while True:
    #-----------Temperature and Humidity ------------------
    bus.write_byte(0x40, 0xE5)
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
    hum_out = float(hum)
    temp_out = float(temp)



    #------------------Light--------------------------------------
    bus.write_byte(0x39, 0x8C)
    light_LSB = bus.read_byte(0x39)
    bus.write_byte(0x39, 0x8D)
    light_MSB = bus.read_byte(0x39)

    light_MSB = light_MSB << 8
    light = int(light_MSB + light_LSB)
    print("Light: ", light)

    thisdict = {
      "temperature": temp_out,
      "humidity": hum_out,
      "light": light
    }

    message = json.dumps(thisdict)
    msg_info = client.publish("IC.embedded/spicy_chorizo/test", message)
    print("Message published:", mqtt.error_string(msg_info.rc))

    time.sleep(5)
