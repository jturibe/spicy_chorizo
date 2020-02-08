import paho.mqtt.client as mqtt
import ssl
import json
from firebase import firebase
import datetime

firebase = firebase.FirebaseApplication("https://spicychorizo-794f1.firebaseio.com/", None)


def on_message(client, userdata, message):
    now = datetime.datetime.now()
    received_payload = json.loads(message.payload)
    cur_minute = now.minute

    cur_light = received_payload['light']
    cur_humidity = received_payload['humidity']
    cur_temperature = received_payload['temperature']
    # print("Received message:{} on topic{}".format(message.payload, message.topic))
    print(received_payload)

    result = firebase.delete('/l_hour/RAW/light', cur_minute)
    result = firebase.patch('/l_hour/RAW/light', {cur_minute: cur_light})
    print(result)

    result = firebase.delete('/l_hour/RAW/humidity', cur_minute)
    result = firebase.patch('/l_hour/RAW/humidity', {cur_minute: cur_humidity})
    print(result)

    result = firebase.delete('/l_hour/RAW/temperature', cur_minute)
    result = firebase.patch('/l_hour/RAW/temperature', {cur_minute: cur_temperature})
    print(result)

client = mqtt.Client()
client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key", tls_version=ssl.PROTOCOL_TLSv1_2)
con_code = client.connect("test.mosquitto.org",port=8884)

if not con_code:
    client.subscribe("IC.embedded/spicy_chorizo/#")
    print("Subscribed to IC.embedded/spicy_chorizo/#")
else:
    print(mqtt.error_string(con_code))

client.on_message = on_message
client.subscribe("IC.embedded/spicy_chorizo/#")

client.loop_forever() ##blocks for 100ms
print("Done")
