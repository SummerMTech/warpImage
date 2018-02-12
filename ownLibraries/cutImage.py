import numpy as np
import cv2
import math

class Transform():
    def __init__(self,poly):
        self.src = poly # Expected something like srcPol = [[pt1],[pt2],[pt3],[pt4]]
        print(self.src)
        x1=self.src[0][0]
        y1=self.src[0][1]
        x2=self.src[1][0]
        y2=self.src[1][1]
        x3=self.src[2][0]
        y3=self.src[2][1]
        x4=self.src[3][0]
        y4=self.src[3][1]
        self.lado1=0
        self.lado2=0
        self.size=0
        ##Angulo::
        self.anguloInicial=math.atan((y2-y1)/(x2-x1))
        self.anguloInicialGrados=self.anguloInicial*180/(math.pi)
        ##distancia puntos dos y tres
        #print('real x3 and y3:.. '+str(x3)+'--'+str(y3))
        distancia=math.sqrt((x2-x3)**2+(y2-y3)**2)
        x3=distancia*math.cos(math.pi-math.pi/2-self.anguloInicial)+x2
        y3=y2-distancia*math.sin(math.pi-math.pi/2-self.anguloInicial)
        #print('90 degrees x3 and y3:.. '+str(x3)+'--'+str(y3))

        d1=x3-x2
        d2=y2-y3

        X1=0
        Y1=(y2-y1)*(X1-x1)//(x2-x1)+y1
        if Y1<0:
            Y4=0
            Y1=d2
            X1=(Y1-y1)*(x2-x1)//(y2-y1)+x1
            X4=X1+d1
            ##second point
        if Y1==0:
            Y4=0
            Y1=d2
            X1=(Y1-y1)*(x2-x1)//(y2-y1)+x1
            X4=X1+d1
        if Y1>0:
            if d2>Y1:
                Y4=0
                Y1=d2
                X1=(Y1-y1)*(x2-x1)//(y2-y1)+x1
                X4=X1+d1
            else:
                X4=d1
                Y4=Y1-d2
            


        #
        #X4=0
        #Y4=(X4-x3)*(y4-y3)//(x4-x3)+y3
        #if Y4<0:
        #    Y4=0
        #    X4=(Y4-y3)*(x4-x3)//(y4-y3)+x3

        self.src_point1 = (X1,Y1)
        self.src_point2 = self.src[1]
        self.src_point3 = (x3,y3)
        self.src_point4 = (X4,Y4)
        print('Final Points:.. '+str(self.src_point1)+'--'+str(self.src_point2)+str(self.src_point3)+str(self.src_point4))
        self.angulo=0
        self.angle=0
        self.NewLista=[]
        
    def cutRegion(self,frame):
        a=math.sqrt((self.src_point1[0]-self.src_point2[0])**2+(self.src_point1[1]-self.src_point2[1])**2)
        b=math.sqrt((self.src_point2[0]-self.src_point3[0])**2+(self.src_point2[1]-self.src_point3[1])**2)
        c=math.sqrt((self.src_point3[0]-self.src_point4[0])**2+(self.src_point3[1]-self.src_point4[1])**2)
        d=math.sqrt((self.src_point4[0]-self.src_point1[0])**2+(self.src_point4[1]-self.src_point1[1])**2)
        #print('Division'+str(self.src_point2[1])+'/'+str(a))       
        #print('punto uno:..'+str(self.src_point1)+'--'+'Punto dos:..'+str(self.src_point2))
        #self.angulo=math.asin((self.src_point2[1]-self.src_point1[1])/a)
        self.angulo=self.anguloInicial
        #print('Angulo en Radianes'+str(self.angulo))
        self.angle=self.angulo*180/(math.pi)
        #print('AnguloInicial Grados'+str(self.anguloInicialGrados))
        #print('Angulo Grados'+str(self.angle))
        
        #print(a)
        #print(b)
        #print(c)
        #print(d)
        if a>c:
            self.lado1 = int(a)
        else:
            self.lado1 = int(c)
        if b>d:
            self.lado2 = int(b)
        else:
            self.lado2 = int(d)
        if self.lado1 < self.lado2:
        	img_size = (self.lado2, self.lado1)
        else:
        	img_size = (self.lado1, self.lado2)
        self.size=img_size
        #print('size_New_Image..'+ str(img_size))
        dst = np.float32([[0,0], [img_size[0],0], [img_size[0],img_size[1]], [0,img_size[1]]])
        # For source points I'm grabbing the outer four detected corners
        src = np.float32([self.src_point4, self.src_point3, self.src_point2, self.src_point1])
        # Given src and dst points, calculate the perspective transform matrix
        M = cv2.getPerspectiveTransform(src, dst)
        # Warp the image using OpenCV warpPerspective()
        warped = cv2.warpPerspective(frame, M, img_size)
        pointsNew=[(self.src_point1),(self.src_point2),(self.src_point3),(self.src_point4)]
     
        return warped, pointsNew

    def real_Points(self,points):
        
        #print('angulo:..'+str(self.angle))
        #print('Punto OrigenX1:...'+str(self.src_point1))
        #print('Punto OrigenX1:...'+str(self.src_point4))
        #print('Punto OrigenX1:...'+str(self.src_point2))
        #print('tamaño en Y'+str(self.size[1]))
        x_add=(0)*math.cos(-self.angulo)+(self.size[1])*math.sin(-self.angulo)
        X_add=abs(x_add)
        #print('x_add:...'+str(x_add))
        #print('X_add:...'+str(X_add))

        if self.src_point1[0]==0 and self.src_point4[1]==0:
            #print('caso1 X=0 and y=0')
            #print('X:--'+str(self.src_point1[0])+'--Y:--'+str(self.src_point4[1]))     
            for i in range(len(points)):
                for j in range(2):
                    #print('caso1 X=0 and y=0')
                    #print('X_add:...'+str(X_add))
                    #print('points en i Iniciales:--'+str(points[i]))
                    x=points[i][j][0]
                    y=points[i][j][1]
                    #print('X and Y :...'+str(x)+ '-'+str(y))
                    points=list(points)
                    box=list(points[i])
                    change=list(box[j])
                    change[0]=int(X_add+((x)*math.cos(-self.angulo)+(y)*math.sin(-self.angulo)))
                    #print('change X:..'+ str(change[0]))
                    change[1]=int(-math.sin(-self.angulo)*(x)+(y)*math.cos(-self.angulo))
                    #print('change Y:..'+ str(change[1]))
                    box[j]=tuple(change)
                    points[i]=tuple(box)
                    points=tuple(points)
                    #print('points en i:--'+str(points[i]))
                    #points=tuple(newpoints)
        if self.src_point4[1]!=0 and self.src_point1[0]==0 :
            
            #print('caso2 X=0 and y!=0')
            #print('X:--'+str(self.src_point1[0])+'--Y:--'+str(self.src_point4[1]))
            for i in range(len(points)):
                for j in range(2):
                    #print('caso2 X=0 and y!=0')
                    #print('points en i Iniciales:--'+str(points[i]))
                    x=points[i][j][0]
                    y=points[i][j][1]
                    #print('X and Y :...'+str(x)+ '-'+str(y))
                    points=list(points)
                    box=list(points[i])
                    change=list(box[j])
                    change[0]=int(X_add+((x)*math.cos(-self.angulo)+(y)*math.sin(-self.angulo)))
                    #print('change X:..'+ str(change[0]))
                    change[1]=int(self.src_point4[1]+(-math.sin(-self.angulo)*(x)+(y)*math.cos(-self.angulo)))
                    #print('change Y:..'+ str(change[1]))
                    box[j]=tuple(change)
                    points[i]=tuple(box)
                    points=tuple(points)
                    #print('points en i:--'+str(points[i]))
        if self.src_point1[0]!=0  and self.src_point4[1]==0:
            #print('caso3 X!=0 and y=0')
            #print('X:--'+str(self.src_point1[0])+'--Y:--'+str(self.src_point4[1]))
            for i in range(len(points)):
                for j in range(2):
                    #print('points en i Iniciales:--'+str(points[i]))
                    x=points[i][j][0]
                    y=points[i][j][1]
                    #print('X and Y :...'+str(x)+ '-'+str(y))
                    points=list(points)
                    box=list(points[i])
                    change=list(box[j])
                    change[0]=int(self.src_point4[0]+X_add+((x)*math.cos(-self.angulo)+(y)*math.sin(-self.angulo)))
                    #print('change X:..'+ str(change[0]))
                    change[1]=int(-math.sin(-self.angulo)*(x)+(y)*math.cos(-self.angulo))
                    #print('change Y:..'+ str(change[1]))
                    box[j]=tuple(change)
                    points[i]=tuple(box)
                    points=tuple(points)
                    #print('points en i:--'+str(points[i]))
        return points
