import numpy as np
import cv2
import math

class Transform():
    def __init__(self,poly):
        self.src = poly # Expected something like srcPol = [[pt1],[pt2],[pt3],[pt4]]
        x1=self.src[0][0]
        y1=self.src[0][1]
        x2=self.src[1][0]
        y2=self.src[1][1]
        x3=self.src[2][0]
        y3=self.src[2][1]
        x4=self.src[3][0]
        y4=self.src[3][1]

        X1=0
        Y1=(y2-y1)*(X1-x1)//(x2-x1)+y1
        if Y1<0:
            Y1=0
            X1=(Y1-y1)*(x2-x1)//(y2-y1)+x1
        
        X4=0
        Y4=(X4-x3)*(y4-y3)//(x4-x3)+y3
        if Y4<0:
            Y4=0
            X4=(Y4-y3)*(x4-x3)//(y4-y3)+x3

        self.src_point1 = (X1,Y1)
        self.src_point2 = self.src[1]
        self.src_point3 = self.src[2]
        self.src_point4 = (X4,Y4)
        self.angulo=0
        self.NewLista=[]

    def cutRegion(self,frame):
        a=math.sqrt((self.src_point1[0]-self.src_point2[0])**2+(self.src_point1[1]-self.src_point2[1])**2)
        b=math.sqrt((self.src_point2[0]-self.src_point3[0])**2+(self.src_point2[1]-self.src_point3[1])**2)
        c=math.sqrt((self.src_point3[0]-self.src_point4[0])**2+(self.src_point3[1]-self.src_point4[1])**2)
        d=math.sqrt((self.src_point4[0]-self.src_point1[0])**2+(self.src_point4[1]-self.src_point1[1])**2)
        self.angulo=math.asin((self.src_point2[1])/a)
        self.angulo=self.angulo*180/(math.pi)
        #print(a)
        #print(b)
        #print(c)
        #print(d)
        if a>c:
            lado1 = int(a)
        else:
            lado1 = int(c)
        if b>d:
            lado2 = int(b)
        else:
            lado2 = int(d)
        if lado1 < lado2:
        	img_size = (lado2, lado1)
        else:
        	img_size = (lado1, lado2)
        dst = np.float32([[0,0], [img_size[0],0], [img_size[0],img_size[1]], [0,img_size[1]]])
        # For source points I'm grabbing the outer four detected corners
        src = np.float32([self.src_point4, self.src_point3, self.src_point2, self.src_point1])
        # Given src and dst points, calculate the perspective transform matrix
        M = cv2.getPerspectiveTransform(src, dst)
        # Warp the image using OpenCV warpPerspective()
        warped = cv2.warpPerspective(frame, M, img_size)
        # Just comment the vizualization
        #cv2.imshow("original",image)
        #cv2.imshow("perspective",warped)
        #cv2.waitKey(0)
        return warped

    def real_Points(self,points):
        X_add=abs((0)*math.cos(-self.angulo)+(lado2)*math.sin(-self.angulo))
        for i in range(len(points)):
            x=points[i][0]
            y=points[i][1]
            new_vector=(X_add+(x)*math.cos(-self.angulo)+(y)*math.sin(-self.angulo),(-math.sin(-self.angulo)*(x)+(y)*math.cos(-self.angulo)))
            self.NewLista.append(new_vector)
        return self.NewLista
