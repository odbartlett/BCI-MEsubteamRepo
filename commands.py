import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

#  reference section. no need to worry about these. just here for a log 
#  git clone http://www.github.com/DexterInd/GoPiGo3.git /home/pi/Dexter/GoPiGo3
#  bash /home/pi/Dexter/GoPiGo3/Install/update_gopigo3.sh
#  /usr/local/opt/mosquitto/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf


#function executes everytime a message is recieved by listening_client 
def on_message(client, userdata, message):
  print("received message: " , str(message.payload.decode("utf-8")))
  if(str(message.payload.decode("utf-8")) == "2"):
    print("found 2")

def main():
  # mqttBroker ="3.138.202.174" 
  mqttBroker = "3.138.202.174"
  
	#important note: clients must have unique names
	#if names are duplicated, the one first connected will be disconnected
  client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "test_brady_sender")
  client.connect(mqttBroker) 
  
  #creates client to listen on test topic
  #used to ensure messages are being recieved and sent out
  listening_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "test_listenter")
  listening_client.connect(mqttBroker) 
  listening_client.loop_start()
  listening_client.subscribe("test")
  listening_client.on_message=on_message 
  time.sleep(1)
  

  command = ""
  command = input("enter command: ")


  while(command != "q"):
    client.publish("test", command)
    time.sleep(1)
    command = input("enter command: ")
    



  # while count < 5:
  # 	client.publish("test", count)
  # 	print("Just published " + str(count) + " to topic test")
  # 	time.sleep(3)
  # 	count += 1
 
 
  time.sleep(1)
  listening_client.loop_stop()



      

main()