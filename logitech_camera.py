import os  
import time
import cv2 






class Camera: 
    def __init__(self):  
        self.camId = "/dev/v4l/by-id/usb-046d_Logitech_BRIO_FAB94572-video-index0"
        
        
        self.device = cv2.VideoCapture(self.camId)
        self.device.set(3,1280)
        self.device.set(4,720)
        self.setParams()
        
    
    def fetchImage(self):
        ret_value,frame = self.device.read()
        if ret_value == True:
            # frame = cv2.resize(frame,(200,200))
            return frame
            # cv2.imwrite(os.getcwd() + "/temp/" + "live_image.jpg",frame)
        else:
            print("error")

        return frame

    

    def setParams(self):
        os.system("v4l2-ctl --device "+str(self.camId)+" --set-ctrl=exposure_auto=1 ")
        os.system("v4l2-ctl --device  "+str(self.camId)+" --set-ctrl=exposure_absolute=3 ")
        os.system("v4l2-ctl --device  "+str(self.camId)+" --set-ctrl=focus_auto=0 ")
        os.system("v4l2-ctl --device  "+str(self.camId)+" --set-ctrl=focus_absolute=100 ")
        os.system("v4l2-ctl --device  "+str(self.camId)+" --set-ctrl=white_balance_temperature_auto=0 ")
        os.system("v4l2-ctl --device  "+str(self.camId)+" --set-ctrl=white_balance_temperature=5500 ")
        os.system("v4l2-ctl --device  "+str(self.camId)+" --set-ctrl=gain=255 ")
        
        time.sleep(1)
        self.device.set(3,1280)
        self.device.set(4,720)



        

if __name__ == "__main__":
    cam = Camera()
    

    while True:
        t = time.time()
        image = cam.fetchImage()
        print("Time taken to fetch image",1/(time.time() - t))
        cv2.imshow("video",image)
        cv2.waitKey(1)

                 

        