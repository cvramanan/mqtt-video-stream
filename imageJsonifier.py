import cv2
import numpy as np 
import json
import base64

def imageEncoder(image):
    ret, encodedImage = cv2.imencode('.jpg', image)
    # bytesImage = encodedImage.tobytes()
    bytesImage = base64.encodebytes(encodedImage).decode('utf-8')
    return bytesImage



testImage = np.zeros((3,3,3),dtype = "uint8")

encodedImage = imageEncoder(testImage)

print(encodedImage)

payload = {}


print("tyep of data",type(encodedImage))
payload["image"] = encodedImage

jsonData = json.dumps(payload)

# print(jsonData)

jsonData = json.loads(jsonData)


recoveredImage = jsonData["image"]



recoveredImage = bytes(recoveredImage,encoding="utf-8")

print(recoveredImage)

recoveredImage = base64.decodebytes(recoveredImage)

print(recoveredImage)

recoveredImage = np.frombuffer(recoveredImage,dtype="uint8")

recoveredImage = cv2.imdecode(recoveredImage, cv2.IMREAD_COLOR)

print(recoveredImage)



