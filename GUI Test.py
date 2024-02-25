#BCI test
from paho.mqtt import client as mqtt_client
import tkinter as tk
from random import random
import time

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
    result = client.publish(topic, char)
    status = result[0]
    if status == 0:
        print(f"Sent `{char}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def key_press(event, client):
    key = event.char
    if key in ['w','a','s','d']:
        label.config(text = f'Key Pressed: {key}')
    
    match key:
        case 'w':
            canvas.itemconfig(rectangle_up, fill="red")
            window.after(1000, lambda: canvas.itemconfig(rectangle_up, fill="white"))
            publish(client, '1')
        case 'a':
            canvas.itemconfig(rectangle_left, fill="red")
            window.after(1000, lambda: canvas.itemconfig(rectangle_left, fill="white"))
            publish(client, '2')
        case 's':
            canvas.itemconfig(rectangle_down, fill="red")
            window.after(1000, lambda: canvas.itemconfig(rectangle_down, fill="white"))
            publish(client, '0')
        case 'd':
            canvas.itemconfig(rectangle_right, fill="red")
            window.after(1000, lambda: canvas.itemconfig(rectangle_right, fill="white"))
            publish(client, '3')
        


    
    

client = connect_mqtt()
client.loop_start()
print('Hello!')

window = tk.Tk()
canvas = tk.Canvas(window, width = 1200, height = 800)
window.geometry("1200x800")
window.configure(bg='grey')
canvas.configure(bg = 'grey')
window.title("Brain Computer Interface GUI")
window.bind('<Key>', lambda event: key_press(event, client))
client.loop_stop()
label = tk.Label(window, text = "Hello World!", font = ('Arial', 30))
label.pack()
# Create a rectangle for the 'up' key
rectangle_up = canvas.create_rectangle(200, 100, 400, 300, outline="black", fill="white", width=2)
text1 = canvas.create_text(300,150, text = "Forward", font=("Arial", 20))
# Create a rectangle for the 'down' key
rectangle_down = canvas.create_rectangle(200, 500, 400, 700, outline="black", fill="white", width=2)
text2 = canvas.create_text(300,580, text = "Stop", font=("Arial", 20))
# Create a rectangle for the 'left' key
rectangle_left = canvas.create_rectangle(50, 300, 250, 500, outline="black", fill="white", width=2)
text3 = canvas.create_text(100, 350, text = "Left", font=("Arial", 20))
# Create a rectangle for the 'right' key
rectangle_right = canvas.create_rectangle(350, 300, 550, 500, outline="black", fill="white", width=2)
text4 = canvas.create_text(400,350, text = "Right",font=("Arial", 20))
canvas.pack()

window.mainloop()
