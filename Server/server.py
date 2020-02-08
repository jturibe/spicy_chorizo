import paho.mqtt.client as mqtt
import ssl
import json
from firebase import firebase
import datetime
import statistics
import numpy as np
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


# Connect to Firebase
firebase = firebase.FirebaseApplication("https://spicychorizo-794f1.firebaseio.com/", None)
cred = credentials.Certificate("Firebase/spicychorizo-794f1-firebase-adminsdk-dckj3-acd1fd6dc2.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spicychorizo-794f1.firebaseio.com'
})

now = datetime.datetime.now()
last_hour = now.hour
print(last_hour)
last_day = now.weekday()


#Calculate the average value for the hour
def average_hour(hour, day):

    light_values = firebase.get('/l_hour/RAW/light', None)
    humidity_values = firebase.get('/l_hour/RAW/humidity', None)
    temperature_values = firebase.get('/l_hour/RAW/temperature', None)

    light_values = list(filter(None, light_values))
    humidity_values = list(filter(None, humidity_values))
    temperature_values = list(filter(None, temperature_values))

    light_avg = statistics.mean(light_values)
    humidity_avg = statistics.mean(humidity_values)
    temperature_avg = statistics.mean(temperature_values)

    datapath = '/l_week/hour_AVG/weekday_' + str(day)
    result = firebase.patch(datapath + '/light', {hour: light_avg})
    result = firebase.patch(datapath + '/humidity', {hour: humidity_avg})
    result = firebase.patch(datapath + '/temperature', {hour: temperature_avg})



#Calculate the average value for the day
def average_day(day):

    datapath = '/l_week/hour_AVG/weekday_' + str(day)

    light_values = firebase.get(datapath + '/light', None)
    humidity_values = firebase.get(datapath + '/humidity', None)
    temperature_values = firebase.get(datapath + '/temperature', None)

    light_avg = statistics.mean(light_values)
    humidity_avg = statistics.mean(humidity_values)
    temperature_avg = statistics.mean(temperature_values)

    result = firebase.patch('/l_week/week_AVG/light', {day: light_avg})
    result = firebase.patch('/l_week/week_AVG/humidity', {day: humidity_values})
    result = firebase.patch('/l_week/week_AVG/temperature', {day: temperature_values})




#Calculate the average value for every hour over the period of the last week
def average_hour_over_day():

    week_record = np.zeros((3, 7, 24))

    ref = db.reference('/l_week/hour_AVG')
    data = ref.get()

    for day in range(7):

        light_values = data['weekday_' + str(day)]['light']
        humidity_values = data['weekday_' + str(day)]['humidity']
        temperature_values = data['weekday_' + str(day)]['temperature']

        for i in range(24):

            if not (light_values[i] is None):
                week_record[0][day][i] = light_values[i]

            if not (humidity_values[i] is None):
                week_record[1][day][i] = humidity_values[i]

            if not (temperature_values[i] is None):
                week_record[1][day][i] = temperature_values[i]


    day_hour_avg = np.mean(week_record, axis=1)

    ref = db.reference('/l_week/week_hour_AVG')
    ref_light = ref.child('light')
    ref_hum = ref.child('humidity')
    ref_temp = ref.child('temperature')

    ref_light.set ({0: day_hour_avg[0][0],
                    1: day_hour_avg[0][1],
                    2: day_hour_avg[0][2],
                    3: day_hour_avg[0][3],
                    4: day_hour_avg[0][4],
                    5: day_hour_avg[0][5],
                    6: day_hour_avg[0][6],
                    7: day_hour_avg[0][7],
                    8: day_hour_avg[0][8],
                    9: day_hour_avg[0][9],
                    10: day_hour_avg[0][10],
                    11: day_hour_avg[0][11],
                    12: day_hour_avg[0][12],
                    13: day_hour_avg[0][13],
                    14: day_hour_avg[0][14],
                    15: day_hour_avg[0][15],
                    16: day_hour_avg[0][16],
                    17: day_hour_avg[0][17],
                    18: day_hour_avg[0][18],
                    19: day_hour_avg[0][19],
                    20: day_hour_avg[0][20],
                    21: day_hour_avg[0][21],
                    22: day_hour_avg[0][22],
                    23: day_hour_avg[0][23]})

    ref_hum.set ({0: day_hour_avg[1][0],
                    1: day_hour_avg[1][1],
                    2: day_hour_avg[1][2],
                    3: day_hour_avg[1][3],
                    4: day_hour_avg[1][4],
                    5: day_hour_avg[1][5],
                    6: day_hour_avg[1][6],
                    7: day_hour_avg[1][7],
                    8: day_hour_avg[1][8],
                    9: day_hour_avg[1][9],
                    10: day_hour_avg[1][10],
                    11: day_hour_avg[1][11],
                    12: day_hour_avg[1][12],
                    13: day_hour_avg[1][13],
                    14: day_hour_avg[1][14],
                    15: day_hour_avg[1][15],
                    16: day_hour_avg[1][16],
                    17: day_hour_avg[1][17],
                    18: day_hour_avg[1][18],
                    19: day_hour_avg[1][19],
                    20: day_hour_avg[1][20],
                    21: day_hour_avg[1][21],
                    22: day_hour_avg[1][22],
                    23: day_hour_avg[1][23]})

    ref_temp.set ( {0: day_hour_avg[2][0],
                    1: day_hour_avg[2][1],
                    2: day_hour_avg[2][2],
                    3: day_hour_avg[2][3],
                    4: day_hour_avg[2][4],
                    5: day_hour_avg[2][5],
                    6: day_hour_avg[2][6],
                    7: day_hour_avg[2][7],
                    8: day_hour_avg[2][8],
                    9: day_hour_avg[2][9],
                    10: day_hour_avg[2][10],
                    11: day_hour_avg[2][11],
                    12: day_hour_avg[2][12],
                    13: day_hour_avg[2][13],
                    14: day_hour_avg[2][14],
                    15: day_hour_avg[2][15],
                    16: day_hour_avg[2][16],
                    17: day_hour_avg[2][17],
                    18: day_hour_avg[2][18],
                    19: day_hour_avg[2][19],
                    20: day_hour_avg[2][20],
                    21: day_hour_avg[2][21],
                    22: day_hour_avg[2][22],
                    23: day_hour_avg[2][23]})





def flood_database(): #helper function to flood the database with 0

    datapath = '/l_week/hour_AVG/weekday_'
    for day in range(7):
        result = firebase.patch(datapath + str(day) + '/light', {0: 0,
                                                                1: 0,
                                                                2: 0,
                                                                3: 0,
                                                                4: 0,
                                                                5: 0,
                                                                6: 0,
                                                                7: 0,
                                                                8: 0,
                                                                9: 0,
                                                                10: 0,
                                                                11: 0,
                                                                12: 0,
                                                                13: 0,
                                                                14: 0,
                                                                15: 0,
                                                                16: 0,
                                                                17: 0,
                                                                18: 0,
                                                                19: 0,
                                                                20: 0,
                                                                21: 0,
                                                                22: 0,
                                                                23: 0})


        result = firebase.patch(datapath + str(day) + '/humidity', {0: 0,
                                                                1: 0,
                                                                2: 0,
                                                                3: 0,
                                                                4: 0,
                                                                5: 0,
                                                                6: 0,
                                                                7: 0,
                                                                8: 0,
                                                                9: 0,
                                                                10: 0,
                                                                11: 0,
                                                                12: 0,
                                                                13: 0,
                                                                14: 0,
                                                                15: 0,
                                                                16: 0,
                                                                17: 0,
                                                                18: 0,
                                                                19: 0,
                                                                20: 0,
                                                                21: 0,
                                                                22: 0,
                                                                23: 0})

        result = firebase.patch(datapath + str(day) + '/temperature', {0: 0,
                                                                1: 0,
                                                                2: 0,
                                                                3: 0,
                                                                4: 0,
                                                                5: 0,
                                                                6: 0,
                                                                7: 0,
                                                                8: 0,
                                                                9: 0,
                                                                10: 0,
                                                                11: 0,
                                                                12: 0,
                                                                13: 0,
                                                                14: 0,
                                                                15: 0,
                                                                16: 0,
                                                                17: 0,
                                                                18: 0,
                                                                19: 0,
                                                                20: 0,
                                                                21: 0,
                                                                22: 0,
                                                                23: 0})







def on_message(client, userdata, message):
    print('Received a message')

    now = datetime.datetime.now()
    received_payload = json.loads(message.payload)
    cur_minute = now.minute
    cur_hour = now.hour
    cur_day = now.weekday()

    print('test')
    print('cur_hour:', cur_hour)
    print('last_hour', last_hour)
    print(cur_day)
    print(last_day)

    if(cur_hour != last_hour):
        print('The hour has changed -> Updating averages and graphs')
        average_hour(last_hour, last_day)
        average_hour_over_day()

    if(cur_day != last_day):
        print('The day has changed -> Updating averages and graphs')
        average_day(last_day)


    print('test2')

    cur_light = received_payload['light']
    cur_humidity = received_payload['humidity']
    cur_temperature = received_payload['temperature']

    print(received_payload)

    #Unpload to current data
    result = firebase.patch('/current_measurement', {'light': cur_light})
    print(result)

    result = firebase.patch('/current_measurement', {'humidity': cur_humidity})
    print(result)

    result = firebase.patch('/current_measurement', {'temperature': cur_temperature})
    print(result)

    #Unpload to hourly backlog
    result = firebase.patch('/l_hour/RAW/light', {cur_minute: cur_light})
    print(result)

    result = firebase.patch('/l_hour/RAW/humidity', {cur_minute: cur_humidity})
    print(result)

    result = firebase.patch('/l_hour/RAW/temperature', {cur_minute: cur_temperature})
    print(result)


    last_hour = cur_hour
    last_day = cur_day





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
