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
import matplotlib.pyplot  as plt


# Connect to Firebase
cred = credentials.Certificate("Firebase/spicychorizo-794f1-firebase-adminsdk-dckj3-acd1fd6dc2.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spicychorizo-794f1.firebaseio.com'
})

now = datetime.datetime.now()
last_hour = now.hour
last_day = now.weekday()



def filter_none(lst):
    res = []
    for val in lst:
        if val != None :
            res.append(val)
    return res

def average_hour_graph(hour, day): #current hour, day of today
    ref_today =  db.reference('/l_week/hour_AVG/weekday_' + str(day))
    ref_yesterday = db.reference('/l_week/hour_AVG/weekday_' + str((day-1)%7))

    light_values_today = ref_today.child('light').get()
    light_values_yesterday = ref_yesterday.child('light').get()

    graph_labels = []
    graph_data = []
    # graph_data[:,:] = np.NaN
    if light_values_yesterday is not None:
        for i in range(hour + 1, 24): #take the required hours from yesterday
            graph_labels.append(i)
            if str(i) in light_values_yesterday:
                graph_data.append(light_values_yesterday[str(i)])
            else:
                graph_data.append(np.NaN)
    else:
        for i in range(hour + 1, 24): #take the required hours from yesterday
            graph_labels.append(i)
            graph_data.append(np.NaN)

    if light_values_today is not None:
        for i in range(0, hour): #take the required hours from yesterday
            graph_labels.append(i)
            if str(i) in light_values_today:
                graph_data.append(light_values_today[str(i)])
            else:
                graph_data.append(np.NaN)
    else:
        for i in range(hour + 1, 24): #take the required hours from yesterday
            graph_labels.append(i)
            graph_data.append(np.NaN)

    cur_vals = db.reference('/current_measurement').get()

    graph_labels.append(hour)
    graph_data.append(cur_vals['light'])

    graph_data = np.asarray(graph_data)
    s1mask = np.isfinite(graph_data)
    xi = list(range(24))

    plot = plt.plot(xi, graph_data, linestyle='-', marker='o')
    plt.xticks(xi, graph_labels)
    plt.savefig('test.png')
    plt.clf()

#Calculate the average value for the hour
def average_hour(hour, day):

    ref = db.reference('/l_hour/RAW/')

    #Retreive RAW data about the last hour from Firebase
    light_values = ref.child('light').get()
    humidity_values = ref.child('humidity').get()
    temperature_values = ref.child('temperature').get()

    ref =  db.reference('/l_week/hour_AVG/weekday_' + str(day))

    if light_values is not None: #If there is any data
        light_values =  light_values.values()   #Extract values
        if len(light_values) != 0:              #Honestly just a cautionary check
            light_avg = statistics.mean(light_values) #Calculate the average
        else:
            light_avg = None
        ref_light = ref.child('light')
        ref_light.update({hour: light_avg})


    if humidity_values is not None:
        humidity_values = humidity_values.values()
        if len(humidity_values) != 0:
            humidity_avg = statistics.mean(humidity_values)
        else:
            humidity_avg = None
        ref_humidity = ref.child('humidity')
        ref_humidity.update({hour: humidity_avg})


    if humidity_values is not None:
        temperature_values = temperature_values.values()
        if len(temperature_values) != 0:
            temperature_avg = statistics.mean(temperature_values)
        else:
            temperature_avg = None
        ref_temperature = ref.child('temperature')
        ref_temperature.update({hour: temperature_avg})








#Calculate the average value for the day
def average_day(day):

    ref = db.reference('/l_week/hour_AVG/weekday_' + str(day))

    #Retreive data from Firebase
    light_values = ref.child('light').get()
    humidity_values = ref.child('humidity').get()
    temperature_values = ref.child('temperature').get()



    ref =  db.reference('/l_week/week_AVG')

    #Check for None values
    if light_values is not None:
        light_values =  light_values.values()   #Extract values
        if len(light_values) != 0:
            light_avg = statistics.mean(light_values)
        else:
            light_avg = None
        ref_light = ref.child('light')
        ref_light.update({day: light_avg})


    if humidity_values is not None:
        humidity_values =  humidity_values.values()   #Extract values
        if len(humidity_values) != 0:
            humidity_avg = statistics.mean(humidity_values)
        else:
            humidity_avg = None
        ref_humidity = ref.child('humidity')
        ref_humidity.update({day: humidity_avg})


    if temperature_values is not None:
        temperature_values =  temperature_values.values()   #Extract values
        #Calculate mean
        if len(temperature_values) != 0:
            temperature_avg = statistics.mean(temperature_values)
        else:
            temperature_avg = None
        ref_temperature = ref.child('temperature')
        ref_temperature.update({day: temperature_avg})






#Calculate the average value for every hour over the period of the last week
def average_hour_over_day():

    week_record = np.empty([3, 7, 24])
    week_record[:,:,:] = np.NaN
    ref = db.reference('/l_week/hour_AVG')
    data = ref.get()

    if data is not None:
        for day in range(7):
            if 'weekday_' + str(day) in data:

                light_values = data['weekday_' + str(day)]['light']
                humidity_values = data['weekday_' + str(day)]['humidity']
                temperature_values = data['weekday_' + str(day)]['temperature']



                for i in range(24):
                        if str(i) in light_values:
                            week_record[0, day, i] = light_values[str(i)]
                        if str(i) in humidity_values:
                            week_record[1, day, i] = humidity_values[str(i)]
                        if str(i) in temperature_values:
                            week_record[2, day, i] = temperature_values[str(i)]

        day_hour_avg = np.nanmean(week_record, axis=1)
        day_hour_avg = np.nan_to_num(day_hour_avg)

        ref = db.reference('/l_week/week_hour_AVG')
        ref_light = ref.child('light')
        ref_hum = ref.child('humidity')
        ref_temp = ref.child('temperature')



        ref_light.update ({0: day_hour_avg[0][0],
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

        ref_hum.update ({0: day_hour_avg[1][0],
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

        ref_temp.update ( {0: day_hour_avg[2][0],
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

    for day in range(7):

        ref = db.reference('/l_week/hour_AVG/weekday_' + str(day))
        ref_light = ref.child('light')
        ref_hum = ref.child('humidity')
        ref_temp = ref.child('temperature')


        ref_light.update({  0: 0,
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


        ref_hum.update({    0: 0,
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

        ref_temp.update({ 0: 0,
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








def initialise_averages():
    for day in range(7):
        print(day)
        average_day(day)






def on_message(client, userdata, message):
    global last_hour
    global last_day
    print('Received a message')

    now = datetime.datetime.now()
    received_payload = json.loads(message.payload)
    cur_minute = now.minute
    cur_hour = now.hour
    cur_day = now.weekday()



    if(cur_hour != last_hour):
        print('The hour has changed -> Updating averages and graphs')
        average_hour(last_hour, last_day)
        average_hour_over_day()

    if(cur_day != last_day):
        print('The day has changed -> Updating averages and graphs')
        average_day(last_day)


    # print('The hour has changed -> Updating averages and graphs')
    # average_hour(last_hour, last_day)
    # average_hour_over_day()
    # print('The day has changed -> Updating averages and graphs')
    # average_day(last_day)
    # print('------Done-------')

    cur_light = received_payload['light']
    cur_humidity = received_payload['humidity']
    cur_temperature = received_payload['temperature']

    print(received_payload)

    #Unpload to current data
    ref = db.reference('/current_measurement')
    ref.update({
        'light': cur_light,
        'humidity': cur_humidity,
        'temperature': cur_temperature
    })


    #Unpload to hourly backlog
    ref = db.reference('/l_hour/RAW')
    ref.child('light').update({cur_minute: cur_light})
    ref.child('humidity').update({cur_minute: cur_humidity})
    ref.child('temperature').update({cur_minute: cur_temperature})

    average_hour_graph(cur_hour, cur_day)

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
# flood_database()
# initialise_averages()
# average_hour_graph(last_hour, last_day)
average_hour(last_hour, last_day)
client.loop_forever() ##blocks for 100ms
print("Done")
