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

while True:
    bus.write_byte(0x40, 0xE5)
    time.sleep(5)
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

    thisdict = {
      "temperature": temp_out,
      "humidity": hum_out
    }

    message = json.dumps(thisdict)
    msg_info = client.publish("IC.embedded/spicy_chorizo/test", message)
    print("Message published:", mqtt.error_string(msg_info.rc))
