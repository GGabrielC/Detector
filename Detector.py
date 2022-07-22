import numpy as np 
import cv2 
import pyautogui 
import time
import os
import copy
import datetime
import ctypes
from VideoCapture import Device

def takeScreenshot():
    image = pyautogui.screenshot() 
    image = cv2.cvtColor(np.array(image), 
					cv2.COLOR_RGB2BGR) 
    return image

def showImage(image, callback, windowName):
    cv2.destroyWindow(windowName)
    cv2.imshow(windowName, image)
    if callback:
        cv2.setMouseCallback(windowName, callback, windowName)
    cv2.waitKey()

def topLeft(rectangle):
    x = min(rectangle[0][0], rectangle[1][0])
    y = min(rectangle[0][1], rectangle[1][1])
    return (x,y)
def topRight(rectangle):
    x = max(rectangle[0][0], rectangle[1][0])
    y = min(rectangle[0][1], rectangle[1][1])
    return (x,y)
def botLeft(rectangle):
    x = min(rectangle[0][0], rectangle[1][0])
    y = max(rectangle[0][1], rectangle[1][1])
    return (x,y)
def botRight(rectangle):
    x = max(rectangle[0][0], rectangle[1][0])
    y = max(rectangle[0][1], rectangle[1][1])
    return (x,y)

class Detector:
    def __init__(self, callbacks, withAutoLock=False):
        self.windowName = 'screenshot'
        self.currentImage = None
        self.priorImage = None
        self.rectangles = []
        self.callbacks = callbacks
        self.refPt = None
        self.crop = None
        self.withAutoLock = withAutoLock
        self.timesChecked = 0
        
    def run(self):
        self.currentImage = takeScreenshot()
        showImage(self.currentImage, self.click, self.windowName)   
        
        while(True):
            time.sleep(10)
            self.priorImage = self.currentImage
            self.currentImage = takeScreenshot()
            self.checkActivity()
            
            #showImage(self.currentImage)
    
    def click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.rectangles.append([(x,y)])
            self.cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.rectangles[-1].append((x,y))
            self.refPt.append((x, y))
            self.cropping = False
            cv2.rectangle(self.currentImage, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
            showImage(self.currentImage, self.click, self.windowName)
    
    def getTime(self):
        now = datetime.datetime.now()
        #now.year, now.month, now.day, now.hour, now.minute, now.second
        return "{0}:{1}:{2}".format(now.hour, now.minute, now.second)
         
    def getNotifyMessage(self, outcome):
        return "[{0}] {1} Detected !".format(self.getTime(), outcome)

    def checkActivity(self):
        for rect in self.rectangles:
            h = botLeft(rect)[1] - topLeft(rect)[1]
            w = topRight(rect)[0] - topLeft(rect)[0]
            x = topLeft(rect)[0]
            y = topLeft(rect)[1]
            
            base_dir = os.getcwd()                                                                                                            
            filename = r'proof.jpg'
            filePath = os.path.join(base_dir, filename)
            
            rectImgCurr = self.currentImage[y:y+h, x:x+w]
            rectImgPrior = self.priorImage[y:y+h, x:x+w]
			
            self.timesChecked += 1
            if self.timesChecked == 1:
                return
			
            if (rectImgCurr == rectImgPrior).all():
                info = self.getNotifyMessage("Inactivity")
                print(info)
                if self.withAutoLock and rect == self.rectangles[-1]:
                    pass
                else:
                    cv2.imwrite(filePath, self.currentImage)
                    for callback in self.callbacks:
                        callback({info:info, filePath:filePath})
                
            else:
                info = self.getNotifyMessage("Activity")
                print(info)
                #cam = Device()
                #cam.saveSnapshot('image.jpg')
                #showImage('image.jpg', self.click, 'image.jpg')
                #time.sleep(1)
                if self.withAutoLock and rect == self.rectangles[-1]:
                    ctypes.windll.user32.LockWorkStation()
                    for callback in self.callbacks:
                        callback({info:info, filePath:filePath})

            #showImage(rectImgPrior, None, "2")
            #showImage(rectImgCurr, None, "1")




