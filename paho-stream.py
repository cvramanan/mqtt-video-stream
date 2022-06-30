from itertools import count
from turtle import shape
import paho.mqtt.client as mqtt
import time
import numpy as np
import cv2
import json
import base64
relativeTime = time.time()
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("video")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global relativeTime
    # print(msg.topic+" "+str(msg.payload))
    print(msg.topic,str(time.time()))
    data = msg.payload
    data = json.loads(data)
    image = bytes(data["image"], encoding="utf-8")

    print(type(image))
    print(image[0:5])
    image = base64.decodebytes(image)
    image = np.frombuffer(image,dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print("fps:",1/(time.time()-relativeTime))
    relativeTime = time.time()
    print(image.shape)
    
    cv2.imwrite("./test/"+str(data["count"])+"_image.jpg",image)
 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()