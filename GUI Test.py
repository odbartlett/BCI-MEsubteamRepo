#BCI test
from paho.mqtt import client as mqtt_client
import tkinter as tk
from random import random

broker = '3.138.202.174'
port = 1883
topic = "test"
client_id = 'ba65a9d7-0107-465b-8909-23819238'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, char):
    msg = f"messages: {char}"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{char}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def key_press(event, client):
    key = event.char
    if key in ['w','a','s','d']:
        label.config(text = f'Key Pressed: {key}')
    publish(client, key)
    

client = connect_mqtt()
client.loop_start()
print('Hello!')

window = tk.Tk()
window.geometry("1200x700")
window.title("Brain Computer Interface GUI")
window.bind('<Key>', lambda event: key_press(event, client))
client.loop_stop()
label = tk.Label(window, text = "Hello World!", font = ('Arial', 30))
label.pack()
window.mainloop()
