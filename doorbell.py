#!/usr/bin/python3
import json
import os

from paho.mqtt import client as mqtt_client

broker = '127.0.0.1'
port = 1883

button_id = 'DoorbellButton'
volume = 70

soundfile = os.path.join(os.path.dirname(__file__), "door_bell_1.mp3")
client_id = 'local-doorbell'
topic = f"zigbee2mqtt/{button_id}"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

#    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    try:
        payload = json.loads(msg.payload.decode())
        if payload.get('action', None) in ('single', 'hold', 'double'):
            os.system(f'mpg123 {soundfile}')
    except:
        pass

os.system(f'amixer set Master {volume}%')

client = mqtt_client.Client(client_id)
client.on_connect = on_connect
client.connect(broker, port)
client.subscribe(topic)
client.on_message = on_message

client.loop_forever()
