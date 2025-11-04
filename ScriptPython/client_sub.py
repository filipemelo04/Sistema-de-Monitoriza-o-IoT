import paho.mqtt.client as mqtt
import time
from influxdb import InfluxDBClient
from datetime import datetime


def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   client_subscriptions(client)
   print("Connected to MQTT server")

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected from MQTT server")
   
   
# a callback functions 
def callback_esp32_temp_external(client, userdata, msg):
    print(datetime.now())
    print('ESP External Temperature: ', msg.payload.decode('utf-8'))
    
    client = InfluxDBClient(host='localhost', port='8086')
    url = 'https://us-west-2-1.aws.cloud2.influxdata.com'
    lista = client.get_list_database()
    client.switch_database('FilipeFarm')
    
    json_payload = []

    data = {
        "measurement": "internal_farm",
        "tags": {
            "plant": "external"
        },
        "time": datetime.now(),
        "fields": {
            'temperature': float(msg.payload.decode('utf-8')),
        }
    }    
    json_payload.append(data)
    client.write_points(json_payload)       
    
def callback_esp32_hum_external(client, userdata, msg):
    print('ESP External Humidity: ', str(msg.payload.decode('utf-8')))
    
    client = InfluxDBClient(host='localhost', port='8086')
    url = 'https://us-west-2-1.aws.cloud2.influxdata.com'
    lista = client.get_list_database()
    client.switch_database('FilipeFarm')
    
    json_payload = []

    data = {
        "measurement": "internal_farm",
        "tags": {
            "plant": "external"
        },
        "time": datetime.now(),
        "fields": {
            'humidity': float(msg.payload.decode('utf-8')),
        }
    }    
    json_payload.append(data)
    client.write_points(json_payload) 
    
def callback_esp32_temp_tomatos(client, userdata, msg):
    print('ESP Tomatos Temperature: ', str(msg.payload.decode('utf-8')))
    
    client = InfluxDBClient(host='localhost', port='8086')
    url = 'https://us-west-2-1.aws.cloud2.influxdata.com'
    lista = client.get_list_database()
    client.switch_database('FilipeFarm')
    
    json_payload = []

    data = {
        "measurement": "internal_farm",
        "tags": {
            "plant": "tomatos"
        },
        "time": datetime.now(),
        "fields": {
            'temperature': float(msg.payload.decode('utf-8')),
        }
    }    
    json_payload.append(data)
    client.write_points(json_payload) 
    
def callback_esp32_hum_tomatos(client, userdata, msg):
    print('ESP Tomatos Humidity: ', str(msg.payload.decode('utf-8')))
    
    client = InfluxDBClient(host='localhost', port='8086')
    url = 'https://us-west-2-1.aws.cloud2.influxdata.com'
    lista = client.get_list_database()
    client.switch_database('FilipeFarm')
    
    json_payload = []

    data = {
        "measurement": "internal_farm",
        "tags": {
            "plant": "tomatos"
        },
        "time": datetime.now(),
        "fields": {
            'humidity': float(msg.payload.decode('utf-8')),
        }
    }    
    json_payload.append(data)
    client.write_points(json_payload) 

def callback_rpi_broadcast(client, userdata, msg):
    print('RPi Broadcast message:  ', str(msg.payload.decode('utf-8')))

def client_subscriptions(client):
    client.subscribe("esp32/#")
    client.subscribe("rpi/broadcast")
    
def day_average(plant):
    
    client = InfluxDBClient(host='localhost', port='8086')
    url = 'https://us-west-2-1.aws.cloud2.influxdata.com'
    lista = client.get_list_database()
    client.switch_database('FilipeFarm')
    
    result_temp= client.query("".join(['''select "temperature" from "internal_farm" where "plant"=''',"'", plant, "'",''' AND time > now() - 1d;''']))
    dataPoints_temp = list(result_temp.get_points())
        
    result_hum= client.query("".join(['''select "humidity" from "internal_farm" where "plant"=''',"'", plant, "'",''' AND time > now() - 1d;''']))
    dataPoints_hum = list(result_hum.get_points())
    
    if len(dataPoints_temp) != 0:            
        somador = 0
        for d in dataPoints_temp:
            somador += d['temperature']
        media_temp = somador / len(dataPoints_temp)
    else: media_temp = 0
    
    if len(dataPoints_hum) != 0:
        somador = 0
        for d in dataPoints_hum:
            somador += d['humidity']
        media_hum = somador / len(dataPoints_hum)
    else: media_hum = 0
            
    client = InfluxDBClient(host='localhost', port='8086')
    url = 'https://us-west-2-1.aws.cloud2.influxdata.com'
    lista = client.get_list_database()
    client.switch_database('FilipeFarm')
                
    json_payload = []

    data = {
        "measurement": "Average_Data",
        "tags": {
            "plant": plant,
            "frequency": "day"
        },
        "time": datetime.now(),
        "fields": {
            'temperature': round(media_temp, 2),
            'humidity': round(media_hum, 2),
        }
    }    
    json_payload.append(data)
    client.write_points(json_payload) 
    
    
client = InfluxDBClient(host='localhost', port='8086')
url = 'https://us-west-2-1.aws.cloud2.influxdata.com'
lista = client.get_list_database()
client.switch_database('FilipeFarm')

client = mqtt.Client("rpi_client1") #this should be a unique name
flag_connected = 0

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.message_callback_add('esp32/temperature/external', callback_esp32_temp_external) 
client.message_callback_add('esp32/humidity/external', callback_esp32_hum_external)
client.message_callback_add('esp32/temperature/tomatos', callback_esp32_temp_tomatos)
client.message_callback_add('esp32/humidity/tomatos', callback_esp32_hum_tomatos)
client.message_callback_add('rpi/broadcast', callback_rpi_broadcast)
client.connect('127.0.0.1',1883) 
# start a new thread
client.loop_start()
client_subscriptions(client)
print("......client setup complete............")

condicao = True

while True:
    time.sleep(0.5)
    
    if (flag_connected != 1):
        print("trying to connect MQTT server..")
        
    if ("00:00:00" in str(datetime.now())):
        if condicao:
            day_average('external')
            day_average('tomatos')
            condicao = False
    else:
        condicao = True
        
        
        
