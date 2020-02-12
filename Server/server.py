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
from firebase_admin import messaging
import matplotlib.pyplot  as plt
import seaborn
import base64
import time
# Connect to Firebase
cred = credentials.Certificate("Firebase/spicychorizo-794f1-firebase-adminsdk-dckj3-acd1fd6dc2.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spicychorizo-794f1.firebaseio.com'
})

now = datetime.datetime.now()
last_hour = now.hour
last_day = now.weekday()


 #######################################################################################################
 #-----------------------------Helper functions--------------------------------------------------------
 #######################################################################################################
def list_to_dict(raw_data):
    if raw_data is None:
        return {}
    if type(raw_data) == type({}):
        return raw_data
    dict = {}
    for i in range(len(raw_data)):
        if raw_data[i] != None:
            print(raw_data[i])
            if not np.isnan(raw_data[i]):
                dict[str(i)] = raw_data[i]

    return dict

def filter_none(lst):
    res = []
    for val in lst:
        if val != None :
            res.append(val)
    return res





 #######################################################################################################
 #-----------------------------Graph creation--------------------------------------------------------
 #######################################################################################################
def update_day_graphs(cur_day):
    ref = db.reference('/l_week/week_AVG/')
    #Retrieve data from firebase
    humidity_values = list_to_dict(ref.child('humidity').get())
    temperature_values = list_to_dict(ref.child('temperature').get())

    ref = db.reference('/user_settings')
    settings = ref.get()
    if(settings is None):
        settings = { 'humidity_max' : 70,
                     'humidity_min' : 60,
                     'temperature_max' : 18,
                     'temperature_min' : 7
        }

    average_day_graph_temp(cur_day, temperature_values, settings[temperature_min], settings[temperature_max])



def update_hour_graphs(cur_hour, cur_day):

    ref = db.reference('/l_week/hour_AVG/weekday_' + str(cur_day))
    #Retreive data from Firebase
    humidity_values_today = ref.child('humidity').get()
    temperature_values_today = ref.child('temperature').get()
    humidity_values_today = list_to_dict(humidity_values_today)
    temperature_values_today = list_to_dict(temperature_values_today)

    ref = db.reference('/l_week/hour_AVG/weekday_' + str((cur_day-1)%7))
    #Retreive data from Firebase
    humidity_values_yesterday = ref.child('humidity').get()
    temperature_values_yesterday = ref.child('temperature').get()
    humidity_values_yesterday = list_to_dict(humidity_values_yesterday)
    temperature_values_yesterday = list_to_dict(temperature_values_yesterday)

    ref = db.reference('/user_settings')
    settings = ref.get()
    if(settings is None):
        settings = { 'humidity_max' : 70,
                     'humidity_min' : 60,
                     'temperature_max' : 18,
                     'temperature_min' : 7
        }

    average_hour_graph_temp(cur_hour, cur_day, temperature_values_yesterday, temperature_values_today, settings['temperature_max'], settings['temperature_min'])
    average_hour_graph_hum(cur_hour, cur_day, humidity_values_yesterday, humidity_values_today, settings['humidity_max'], settings['humidity_min'])

def average_hour_graph_temp(hour, day, temp_values_yesterday, temp_values_today, upper_range, lower_range): #current hour, day of today
    # ref_today =  db.reference('/l_week/hour_AVG/weekday_' + str(day))
    # ref_yesterday = db.reference('/l_week/hour_AVG/weekday_' + str((day-1)%7))
    #
    # light_values_today = ref_today.child('light').get()
    # light_values_yesterday = ref_yesterday.child('light').get()
    graph_labels = []
    graph_data = []
    # graph_data[:,:] = np.NaN

    if temp_values_yesterday is not None:
        for i in range(hour + 1, 24): #take the required hours from yesterday
            graph_labels.append(str(i) + ":00")
            if str(i) in temp_values_yesterday:
                graph_data.append(temp_values_yesterday[str(i)])
            else:
                graph_data.append(np.NaN)
    else:
        for i in range(hour + 1, 24): #take the required hours from yesterday
            graph_labels.append(str(i) + ":00")
            graph_data.append(np.NaN)

    if temp_values_today is not None:
        for i in range(0, hour): #take the required hours from today
            graph_labels.append(str(i) + ":00")
            if str(i) in temp_values_today:
                graph_data.append(temp_values_today[str(i)])
            else:
                graph_data.append(np.NaN)
    else:
        for i in range(0, hour): #take the required hours from yesterday
            graph_labels.append(str(i) + ":00")
            graph_data.append(np.NaN)

    cur_vals = db.reference('/current_measurement').get()

    graph_labels.append(str(hour) + ":00")
    graph_data.append(cur_vals['temperature'])
    time_labels = []
    graph_data = np.asarray(graph_data)
    series = np.array(graph_data).astype(np.double)
    mask = np.isfinite(series)
    xi = np.arange(24)
    allowed_ticks = [0, 4, 8, 12, 16, 20, 23]
    time_labels = []
    for tick in allowed_ticks:
        time_labels.append(graph_labels[tick])
    plot = plt.plot(xi[mask], graph_data[mask], linestyle='-', color='#000000',linewidth=2)
    plt.xticks(allowed_ticks, time_labels)
    plt.locator_params(axis='x', nbins=24)
    #plt.fill_between(xi[mask], graph_data[mask], y2=0, facecolor='#4D071D', alpha=0.5)

    upper_array = [upper_range]*24
    lower_array = [lower_range]*24
    upper = plt.plot(xi, upper_array, linestyle='--', color='#808080',linewidth=1.25)
    lower = plt.plot(xi, lower_array, linestyle='--', color='#808080',linewidth=1.25)
    plt.fill_between(xi, upper_array, y2=lower_array, facecolor='#C5FFA8', alpha=0.25)
    plt.ylabel("Temperature(°C)", fontname="sans-serif", fontweight="light", fontsize="12")
    plt.xlabel("Time(hourly)", fontname="sans-serif", fontweight="light", fontsize="12")
    axes = plt.gca()
    axes.set_ylim([min([graph_data[mask].min()*0.8,lower_range*0.8]),max([graph_data[mask].max()*1.2,upper_range*1.2])])
    seaborn.despine(left=True, bottom=True, right=True)
    plt.savefig('average_hour_graph_temp.png')
    plt.clf()
    with open("average_hour_graph_temp.png", "rb") as img_file:
        image_string = base64.b64encode(img_file.read())

    ref_average_hour_graph_temp = db.reference('/graphs_temp')
    ref_average_hour_graph_temp.update({'average_hour_graph': image_string.decode()})

def average_hour_graph_hum(hour, day, hum_values_yesterday, hum_values_today, upper_range, lower_range): #current hour, day of today
    # ref_today =  db.reference('/l_week/hour_AVG/weekday_' + str(day))
    # ref_yesterday = db.reference('/l_week/hour_AVG/weekday_' + str((day-1)%7))
    #
    # light_values_today = ref_today.child('light').get()
    # light_values_yesterday = ref_yesterday.child('light').get()
    graph_labels = []
    graph_data = []
    # graph_data[:,:] = np.NaN

    if hum_values_yesterday is not None:
        for i in range(hour + 1, 24): #take the required hours from yesterday
            graph_labels.append(str(i) + ":00")
            if str(i) in hum_values_yesterday:
                graph_data.append(hum_values_yesterday[str(i)])
            else:
                graph_data.append(np.NaN)
    else:
        for i in range(hour + 1, 24): #take the required hours from yesterday
            graph_labels.append(str(i) + ":00")
            graph_data.append(np.NaN)

    if hum_values_today is not None:
        for i in range(0, hour): #take the required hours from today
            graph_labels.append(str(i) + ":00")
            if str(i) in hum_values_today:
                graph_data.append(hum_values_today[str(i)])
            else:
                graph_data.append(np.NaN)
    else:
        for i in range(0, hour): #take the required hours from yesterday
            graph_labels.append(str(i) + ":00")
            graph_data.append(np.NaN)

    cur_vals = db.reference('/current_measurement').get()

    graph_labels.append(str(hour) + ":00")
    graph_data.append(cur_vals['humidity'])
    time_labels = []
    graph_data = np.asarray(graph_data)
    series = np.array(graph_data).astype(np.double)
    mask = np.isfinite(series)
    xi = np.arange(24)
    allowed_ticks = [0, 4, 8, 12, 16, 20, 23]
    time_labels = []
    for tick in allowed_ticks:
        time_labels.append(graph_labels[tick])
    plot = plt.plot(xi[mask], graph_data[mask], linestyle='-', color='#000000',linewidth=2)
    plt.xticks(allowed_ticks, time_labels)
    plt.locator_params(axis='x', nbins=24)
    #plt.fill_between(xi[mask], graph_data[mask], y2=0, facecolor='#4D071D', alpha=0.25)

    upper_array = [upper_range]*24
    lower_array = [lower_range]*24
    upper = plt.plot(xi, upper_array, linestyle='--', color='#808080',linewidth=1.25)
    lower = plt.plot(xi, lower_array, linestyle='--', color='#808080',linewidth=1.25)
    plt.fill_between(xi, upper_array, y2=lower_array, facecolor='#C5FFA8', alpha=0.25)
    plt.ylabel("Relative Humidity(%)", fontname="sans-serif", fontweight="light", fontsize="12")
    plt.xlabel("Time(hourly)", fontname="sans-serif", fontweight="light", fontsize="12")
    axes = plt.gca()
    axes.set_ylim([min([graph_data[mask].min()*0.8,lower_range*0.8]),max([graph_data[mask].max()*1.2,upper_range*1.2])])
    seaborn.despine(left=True, bottom=True, right=True)
    plt.savefig("average_hour_graph_hum.png")
    plt.clf()
    with open("average_hour_graph_hum.png", "rb") as img_file:
        image_string = base64.b64encode(img_file.read())

    ref_average_hour_graph_temp = db.reference('/graphs_hum')
    ref_average_hour_graph_temp.update({'average_hour_graph': image_string.decode()})








 #######################################################################################################
 #-----------------------------Data processing--------------------------------------------------------
 #######################################################################################################

#Calculate the average value for the hour
def average_hour(hour, day):

    ref = db.reference('/l_hour/RAW/')

    #Retreive RAW data about the last hour from Firebase
    light_values = ref.child('light').get()
    humidity_values = ref.child('humidity').get()
    temperature_values = ref.child('temperature').get()

    ref =  db.reference('/l_week/hour_AVG/weekday_' + str(day))

    if light_values is not None: #If there is any data, process it. Otherwise nothing happens
        light_values = list_to_dict(light_values)       #Ensure data is a dict
        light_values =  light_values.values()           #Extract values
        if len(light_values) != 0:                      #Honestly just a cautionary check
            light_avg = statistics.mean(light_values)   #Calculate the average
        else:
            light_avg = None
        ref_light = ref.child('light')
        ref_light.update({hour: light_avg})


    if humidity_values is not None:
        humidity_values = list_to_dict(humidity_values)
        humidity_values = humidity_values.values()
        if len(humidity_values) != 0:
            humidity_avg = statistics.mean(humidity_values)
        else:
            humidity_avg = None
        ref_humidity = ref.child('humidity')
        ref_humidity.update({hour: humidity_avg})


    if humidity_values is not None:
        temperature_values = list_to_dict(temperature_values)
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

    #Set upload reference
    ref =  db.reference('/l_week/week_AVG')
    ref_light = ref.child('light')
    ref_humidity = ref.child('humidity')
    ref_temperature = ref.child('temperature')

    #Check for None values
    if light_values is not None:
        light_values = list_to_dict(light_values)
        light_values =  light_values.values()   #Extract values
        if len(light_values) != 0:
            light_avg = statistics.mean(light_values)
        else:
            light_avg = None
        ref_light.update({day: light_avg})


    if humidity_values is not None:
        humidity_values = list_to_dict(humidity_values)
        humidity_values =  humidity_values.values()   #Extract values
        if len(humidity_values) != 0:
            humidity_avg = statistics.mean(humidity_values)
        else:
            humidity_avg = None
        ref_humidity.update({day: humidity_avg})


    if temperature_values is not None:
        temperature_values = list_to_dict(temperature_values)
        temperature_values =  temperature_values.values()   #Extract values
        if len(temperature_values) != 0:
            temperature_avg = statistics.mean(temperature_values)
        else:
            temperature_avg = None
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
                if 'light' in data['weekday_' + str(day)]:
                    light_values = data['weekday_' + str(day)]['light']
                    light_values = list_to_dict(light_values)
                else:
                    light_values = None

                if 'humidity' in data['weekday_' + str(day)]:
                    humidity_values = data['weekday_' + str(day)]['humidity']
                    humidity_values = list_to_dict(humidity_values)
                else:
                    humidity_values = None

                if 'temperature' in data['weekday_' + str(day)]:
                    temperature_values = data['weekday_' + str(day)]['temperature']
                    temperature_values = list_to_dict(temperature_values)
                else:
                    temperature_values = None



                for i in range(24):
                    if light_values is not None:
                        if str(i) in light_values:
                            week_record[0, day, i] = light_values[str(i)]
                    if humidity_values is not None:
                        if str(i) in humidity_values:
                            week_record[1, day, i] = humidity_values[str(i)]
                    if temperature_values is not None:
                        if str(i) in temperature_values:
                            week_record[2, day, i] = temperature_values[str(i)]


        day_hour_avg = np.nanmean(week_record, axis=1)


        ref = db.reference('/l_week/week_hour_AVG')
        ref_light = ref.child('light')
        ref_hum = ref.child('humidity')
        ref_temp = ref.child('temperature')


        light_values = list_to_dict(day_hour_avg[0])
        humidity_values = list_to_dict(day_hour_avg[1])
        temperature_values = list_to_dict(day_hour_avg[2])


        ref_light.update(light_values)
        ref_hum.update(humidity_values)
        ref_temp.update(temperature_values)






def initialise_averages(): #helper function to flood the averages
    for day in range(7):
        print(day)
        average_day(day)


 #######################################################################################################
 #-----------------------------Notifications--------------------------------------------------------
 #######################################################################################################
def send_notifications(received_payload):
    ref = db.reference('/notifis')
    notif_data_temp = ref.child('temperature').get()
    if(notif_data_temp is None):
        notif_data_temp = { 'last_event_notified': 0,
                            'last_trend_notified': 0,
                            'trend_high_perc': 0,
                            'trend_low_perc': 0
        }
    notif_data_hum = ref.child('humidity').get()
    if(notif_data_hum is None):
        notif_data_hum = { 'last_event_notified': 0,
                            'last_trend_notified': 0,
                            'trend_high_perc': 0,
                            'trend_low_perc': 0
        }

    cur_humidity = received_payload['humidity']
    cur_temperature = received_payload['temperature']



    ref_settings = db.reference('/user_settings')
    settings = ref_settings.get()

    if(settings is None): #If the re is no user settings on the database. In the final
                        #product this would flag a seperate notification saying thet the temperature
                        #is different from the one we recomend
        settings = { 'humidity_max' : 30,
                     'humidity_min' : 10,
                     'temperature_max' : 30,
                     'temperature_min' : 5
        }

    if(cur_temperature > settings['temperature_max']): #temperature is more than desired

        if not(notif_data_temp['trend_high_perc'] >= 1):
            notif_data_temp['trend_high_perc'] = notif_data_temp['trend_high_perc'] + 0.01666666666 #add to percentage of time spent hot
        if not(notif_data_temp['trend_low_perc'] <= 0):
            notif_data_temp['trend_low_perc'] = notif_data_temp['trend_low_perc'] - 0.01666666666 #add to percentage of time spent hot


        if (time.time() - notif_data_temp['last_trend_notified']) > 300: #a full day or week (5 minutes for demo) has passed since the last trend notification
            if(notif_data_temp['trend_high_perc']>= 0.5): #If there is a trend of high temperature in the last 5 min
                topic = "event_updates"
                message = messaging.Message(
                    notification=messaging.Notification(
                        title='Careful!',
                        body='Your wine has been overheating for too long!',
                    ),
                    topic=topic,
                )
                response = messaging.send(message)
                notif_data_temp['last_trend_notified'] = time.time()


    elif(cur_temperature < settings['temperature_min']): #temperature is more less desired

        if not(notif_data_temp['trend_low_perc'] >= 1):
            notif_data_temp['trend_low_perc'] = notif_data_temp['trend_low_perc'] + 0.01666666666 #add to percentage of time spent hot

        if not(notif_data_temp['trend_high_perc'] <= 0):
            notif_data_temp['trend_high_perc'] = notif_data_temp['trend_high_perc'] - 0.01666666666 #add to percentage of time spent hot


        if (time.time() - notif_data_hum['last_trend_notified']) > 300: #a full day or week (5 minutes for demo) has passed since the last trend notification
            if(notif_data_temp['trend_low_perc']>= 0.5): #If there is a trend of high temperature in the last 5 min
                topic = "event_updates"
                message = messaging.Message(
                    notification=messaging.Notification(
                        title='Careful!',
                        body='Your wine has been freezing for too long!',
                    ),
                    topic=topic,
                )
                response = messaging.send(message)
                notif_data_temp['last_trend_notified'] = time.time()

    else:
        if not(notif_data_temp['trend_low_perc'] <= 0):
            notif_data_temp['trend_low_perc'] = notif_data_temp['trend_low_perc'] - 0.01666666666 #add to percentage of time spent hot

        if not(notif_data_temp['trend_high_perc'] <= 0):
            notif_data_temp['trend_high_perc'] = notif_data_temp['trend_high_perc'] - 0.01666666666 #add to percentage of time spent hot





    if(cur_humidity > settings['humidity_max']): #humidity is more than desired

        if not(notif_data_hum['trend_high_perc'] >= 1):
            notif_data_hum['trend_high_perc'] = notif_data_hum['trend_high_perc'] + 0.01666666666 #add to percentage of time spent too moist
        if not(notif_data_hum['trend_low_perc'] <= 0):
            notif_data_hum['trend_low_perc'] = notif_data_hum['trend_low_perc'] - 0.01666666666 #take away from percentage of time spent too dry


        if (time.time() - notif_data_hum['last_trend_notified']) > 300: #a full day or week (5 minutes for demo) has passed since the last trend notification
            if(notif_data_hum['trend_high_perc']>= 0.5): #If there is a trend of high humidity in the last 5 min
                topic = "event_updates"
                message = messaging.Message(
                    notification=messaging.Notification(
                        title='Careful!',
                        body='Your wine storage is too humid!',
                    ),
                    topic=topic,
                )
                response = messaging.send(message)
                notif_data_hum['last_trend_notified'] = time.time()


    elif(cur_humidity < settings['humidity_min']): #humidity is less than desired

        if not(notif_data_hum['trend_low_perc'] >= 1):
            notif_data_hum['trend_low_perc'] = notif_data_hum['trend_low_perc'] + 0.01666666666 #add to percentage of time spent too dry

        if not(notif_data_hum['trend_high_perc'] <= 0):
            notif_data_hum['trend_high_perc'] = notif_data_hum['trend_high_perc'] - 0.01666666666 #take away from percentage of time spent too moist


        if (time.time() - notif_data_hum['last_trend_notified']) > 300: #a full day or week (5 minutes for demo) has passed since the last trend notification
            if(notif_data_hum['trend_low_perc']>= 0.5): #If there is a trend of high humidity in the last 5 min
                topic = "event_updates"
                message = messaging.Message(
                    notification=messaging.Notification(
                        title='Careful!',
                        body='Your wine storage is not humid enough!',
                    ),
                    topic=topic,
                )
                response = messaging.send(message)
                notif_data_hum['last_trend_notified'] = time.time()

    else:
        if not(notif_data_hum['trend_low_perc'] <= 0):
            notif_data_hum['trend_low_perc'] = notif_data_hum['trend_low_perc'] - 0.01666666666 #take away from percentage of time spent too dry

        if not(notif_data_hum['trend_high_perc'] <= 0):
            notif_data_hum['trend_high_perc'] = notif_data_hum['trend_high_perc'] - 0.01666666666 #take away from percentage of time spent too moist


    ref.child('temperature').update(notif_data_temp)
    ref.child('humidity').update(notif_data_hum)



def send_to_topic():
    topic = "event_updates"

    message = messaging.Message(
        notification=messaging.Notification(
            title='EMERGENCY',
            body='TEMPERATURE IS TOO HOT HOT HOT',
        ),
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_topic]





 #######################################################################################################
 #-----------------------------On message--------------------------------------------------------
 #######################################################################################################
def on_message(client, userdata, message):
    #Global variables
    global last_hour
    global last_day

    print('Received a message')
    received_payload = json.loads(message.payload)

    #Current time
    now = datetime.datetime.now()
    cur_minute = now.minute
    cur_hour = now.hour
    cur_day = now.weekday()


    #Check if averages need to be updated
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


    #Retreive the individual values
    cur_light = received_payload['light']
    cur_humidity = received_payload['humidity']
    cur_temperature = received_payload['temperature']

    #Compress light value for user display
    compressed_light = 'Bright'
    if(cur_light<10):
        compressed_light = 'Dark'
    elif(cur_light<50):
        compressed_light = 'Dim'


    print(received_payload)
    print('Light levels compressed')

    #Upload to current data
    ref = db.reference('/current_measurement')
    ref.update({
        'light': compressed_light,
        'humidity': cur_humidity,
        'temperature': cur_temperature
    })
    print('Current measurements updated')

    #Unpload to hourly backlog
    ref = db.reference('/l_hour/RAW')
    ref.child('light').update({cur_minute: cur_light})
    ref.child('humidity').update({cur_minute: cur_humidity})
    ref.child('temperature').update({cur_minute: cur_temperature})

    #Update last 24h average graphs since they contain last value as the current one
    update_hour_graphs(cur_hour, cur_day)
    print('Updated last 24h average graphs')

    send_notifications(received_payload)
    print('Checked and sent notifications')

    last_hour = cur_hour
    last_day = cur_day

    print('Finished On Message\n\n')

#######################################################################################################
#-----------------------------Main connections and actions on server startup--------------------------------------------------------
#######################################################################################################





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


client.loop_forever()
print("Done")

# upper_range = 27
# lower_range = 18
# yesterday = list_to_dict([20,21,20,21,20,21,20,21,20,21,20,21,20,21])
# today = list_to_dict([20,21,20,21,20,21,20,21,20,21,20,21,20,21])
# average_hour_graph_temp(last_hour, last_day, yesterday, today, upper_range, lower_range)
# average_hour_graph_hum(last_hour, last_day, yesterday, today, upper_range, lower_range)
