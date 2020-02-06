import paho.mqtt.client as mqtt
import ssl
import json
from firebase import firebase

firebase = firebase.FirebaseApplication("https://spicychorizo-794f1.firebaseio.com/", None)


def on_message(client, userdata, message):
    received_payload = json.loads(message.payload)
    # print("Received message:{} on topic{}".format(message.payload, message.topic))
    print(received_payload)
    result = firebase.post('/RAW', received_payload)
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
