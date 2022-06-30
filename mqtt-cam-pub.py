from time import time
import paho.mqtt.client as mqtt
import time
import cv2
import numpy as np
from logitech_camera import Camera
import queue
import threading
from multiprocessing import Process, Queue
from numba import njit
import base64


cam = Camera()





# frameQueue = queue.Queue(maxsize=100)
frameQueue1 = Queue()
frameQueue2 = Queue()





def frameSender1(frameQueue1):
    import json
    mqttc = mqtt.Client()

    mqttc.connect("192.168.0.103", 1883, 60)
    mqttc.loop_start()
    # @njit(nopython=False)
    def imageEncoder(image):
        refTime = time.time()
        ret, encodedImage = cv2.imencode('.jpg', image)
        encodedImage = encodedImage.flatten()
        bytesImage = base64.encodebytes(encodedImage).decode('utf-8')
        # print("time take for encode and utf convrsion ",time.time()-refTime)
        # exit()
        return bytesImage
    while True:
        # print("queue size",frameQueue.qsize())
        if frameQueue1.empty() != True:
            # print("q 1 sending data")
            encodingTime = time.time()
            q1Data = frameQueue1.get()
            # print("sending data from q1",q1Data["count"])
            q1Data["image"] = imageEncoder(q1Data["image"])
            # print("time taken for encoding",time.time()-encodingTime)
            refTime = time.time()
            payload = json.dumps(q1Data)
            # print("time take for json encoding",time.time()-refTime)
            mqttc.publish("video",payload )
            
        time.sleep(0.001)


def frameSender2(frameQueue2):
    import json
    mqttc = mqtt.Client()

    mqttc.connect("192.168.0.103", 1883, 60)
    mqttc.loop_start()

    def imageEncoder(image):
        
        ret, encodedImage = cv2.imencode('.jpg', image)
        encodedImage = encodedImage.flatten()
        bytesImage = base64.encodebytes(encodedImage).decode('utf-8')
        
        return bytesImage
    
    while True:
        # print("queue size from b",frameQueue.qsize())
        # print("q 2 sending data")
        if frameQueue2.empty() != True:
            # print("k")
            encodingTime = time.time()
            q2Data = frameQueue2.get()
            # print("sending data from q2",q2Data["count"])
            bytesImage = imageEncoder(q2Data["image"])
            # print("time taken for encoding",time.time()-encodingTime)
            q2Data["image"]  = bytesImage
            # print(type(bytesImage),str(bytesImage[:4]))
            # exit()
            mqttc.publish("video", json.dumps(q2Data))
        time.sleep(0.002)

def frameSender3(frameQueue):
    import json
    mqttc = mqtt.Client()

    mqttc.connect("192.168.0.103", 1883, 60)
    mqttc.loop_start()

    def imageEncoder(image):
        ret, encodedImage = cv2.imencode('.jpg', image)
        encodedImage = encodedImage.flatten()
        bytesImage = base64.encodebytes(encodedImage).decode('utf-8')
        return bytesImage
    
    while True:
        # print("queue size",frameQueue.qsize())
        if frameQueue.qsize() > 3:
            encodingTime = time.time()
            data = frameQueue.get()
            print("sending data",data["count"])
            bytesImage = imageEncoder(data["image"])
            print("time taken for encoding",time.time()-encodingTime)
            data["image"]  = bytesImage
            # print(type(bytesImage),str(bytesImage[:4]))
            # exit()
            mqttc.publish("video", json.dumps(data))


# threading.Thread(target=frameSender,args=(frameQueue,mqttc,),daemon=False).start()

Process(target=frameSender1,args=(frameQueue1,),daemon=False).start()
Process(target=frameSender2,args=(frameQueue2,),daemon=False).start()
# Process(target=frameSender3,args=(frameQueue,),daemon=False).start()
data = {}
count = 0 
while True:
    print("queue A size",frameQueue1.qsize(),"queue B size",frameQueue2.qsize())
    relativeTime = time.time()
    frame = cam.fetchImage()
    print("fps:",1/(time.time()-relativeTime))
    data = {}
    data["image"] = frame
    data["count"] = count
    if count % 2 == 0:
        frameQueue1.put(data)
    else:
        frameQueue2.put(data)

    
    # print(frame.shape)
    count = count+1
    time.sleep(0.001)
    
    
  