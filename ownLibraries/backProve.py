import numpy as np
import cv2

class Detector():
    """this class need begin the user with the polygon data, and have two methods, both methods need the frame 
       and are called "cutRegion" and "findCar", the first return a image cut in basis to polygon and the second
       return the coordinates of the box from the car detected"""

    def __init__(self):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
    
    def findCar(self,frame):
        #Cortado = Perspective(np.array(lista))
        #cortar = Cortado._warpOp(frame)
        gris=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detect=self.car.detectMultiScale(gris, 1.1, 2)
        #rectangle.append((detect))

        return detect
    def get_centroid(x, y, w, h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        cx = x + x1
        cy = y + y1
        return (cx, cy)
    def findBackSubs(self,frame):
        movimiento=0
        matches=[]
        fgmask = self.fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        #cv2.imshow('frame',fgmask)
        im2, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        for (i, contour) in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(contour)
            centroid = Detector.get_centroid(x, y, w, h)####looking for the best way
            matches.append(((x, y, w, h), centroid))
            if cv2.contourArea(contour)>=10:
                movimiento=1
            else:
                movimiento=0
            
        #print(len(matches))    
        return matches,movimiento


