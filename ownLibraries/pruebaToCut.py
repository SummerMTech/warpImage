import numpy as np
import cv2
from cutImage import Transform
import timeit
from backProve import Detector
lista=[]

boxes=[]
datos=np.load('/home/pi/trafficFlow/prototipo/installationFiles/sar.npy')
listaFile=datos[1]
listaFile1=datos[0]
listaFile2=datos[2]

print(datos)
def get_BigRectangle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        lista.append((x,y))
        if len(lista)!=0:
            cv2.circle(frame, (x,y),3,(0,255,0),-1)
            cv2.imshow('First_Frame',frame)

def draw(matches,frame_resized):
		for (i, match) in enumerate(matches):
			contour, centroid = match[0], match[1]
			x,y,w,h = contour
			cv2.rectangle(frame_resized, (x,y),(x+w-1, y+h-1),(0,0,255),1)
			cv2.circle(frame_resized, centroid,2,(0,255,0),-1)
			
		
    
try:
		#cap=cv2.VideoCapture(directorioDeVideos+nameSourceVideo)
		cap=cv2.VideoCapture(0)
		for i in range (50):
			ret, frame=cap.read()
		frame=cv2.resize(frame,(320,240))
		overlay=frame.copy() 
except:
	print('Error Al cargar la camara de flujo')
cv2.namedWindow('First_Frame')
cv2.setMouseCallback('First_Frame', get_BigRectangle)

while True:
	#print('press ESC to not accept and -y- to accept')
	cv2.imshow('First_Frame',frame)
	keyPress = cv2.waitKey()
	if keyPress == ord('y'):
		print('_____Data accept..')
		vrx=np.array([[lista]],np.int32)
		pts=vrx.reshape((-1,1,2))
		cv2.polylines(frame,[pts],True,(0,255,255))
		cv2.imshow('First_Frame',frame)
		#np.save('D:/mine/raspberry/python/officialTrialVideos/sar.npy',lista)
		#print('lista: '+str(lista))
		overlay=frame.copy()
	if keyPress == 27:
		#print('_____Data not accept..')
		#print('*Select two points next press -a- to obtain Angle')
		#print('lista no appended: '+str(lista))
		lista=[]
		frame=overlay.copy()
		cv2.imshow('First_Frame',frame)
	
	if keyPress&0xFF==ord('q'):
		break
cv2.destroyAllWindows()
backSub=Detector()
cutting=Transform(lista)
#cutting=Transform(listaFile)
cap=cv2.VideoCapture(0)
while(1):
	start=timeit.default_timer()	
	ret, frame=cap.read()
	##draw
	frame=cv2.resize(frame,(320,240))
	#cutIma,listaNew=cutting.cutRegion(frame)
	cutIma,ListaNew=cutting.cutRegion(frame)

	vrx=np.array([[ListaNew]],np.int32)
	pts=vrx.reshape((-1,1,2))
	cv2.polylines(frame,[pts],True,(255,0,0),2)

	#vrx=np.array([[listaFile]],np.int32)
	#pts=vrx.reshape((-1,1,2))
	#cv2.polylines(frame,[pts],True,(0,0,255),2)
	
	Boxes=backSub.findBackSubs(cutIma)
	Real_Boxes=cutting.real_Points(Boxes)
	lapso=timeit.default_timer()
	tim=lapso-start
	print(tim)
	draw(Boxes,cutIma)
	draw(Real_Boxes,frame)
	#print('puntos')
	#print(Boxes)
	#print('puntosReales')
	#print(Real_Boxes)
	#f=np.vstack((frame,cutIma))
	cv2.imshow('original',frame)
	cv2.imshow('cutting',cutIma)
	#print('data:...'+str(boxes))
	lapso=timeit.default_timer()
	tim=lapso-start
	print(tim)
	if cv2.waitKey(1)&0xFF==ord('q'):
		# file2.write("\n".listFinal)         
		print('saved!!')
		break
cv2.destroyAllWindows()
