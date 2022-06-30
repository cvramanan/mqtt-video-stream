from time import time
import paho.mqtt.client as mqtt
import time
import cv2
import numpy as np
from logitech_camera import Camera
import queue
import threading
from multiprocessing import Process, Queue

cam = Camera()





# frameQueue = queue.Queue(maxsize=100)
frameQueue = Queue()


def frameSender(frameQueue):
    mqttc = mqtt.Client()

    mqttc.connect("127.0.0.1", 1883, 60)
    mqttc.loop_start()
    
    while True:
        print("queue size",frameQueue.qsize())
        if frameQueue.empty() != True:
            print("hi")
            frame = frameQueue.get()
            ret, encodedImage = cv2.imencode('.png', frame)
            bytesImage = encodedImage.tobytes()
            mqttc.publish("video", bytesImage)
        time.sleep(0.001)

# threading.Thread(target=frameSender,args=(frameQueue,mqttc,),daemon=False).start()
Process(target=frameSender,args=(frameQueue,),daemon=False).start()

while True:
    relativeTime = time.time()
    frame = cam.fetchImage()
    print("fps:",1/(time.time()-relativeTime))
    frameQueue.put(frame)
    # print(frame.shape)
    # time.sleep(0.001)
    
    
  