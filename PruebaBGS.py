import numpy as np
import cv2
from cutImage import Transform
import timeit
from backProve import Detector
lista=[]

boxes=[]
datos=np.load('/home/pi/trafficFlow/prototipo/installationFiles/datos.npy')
listaFile=datos[1]
listaFile1=datos[0]
listaFile2=datos[2]
print(datos)
def draw(matches,frame_resized):
		for (i, match) in enumerate(matches):
			contour, centroid = match[0], match[1]
			x,y,w,h = contour
			cv2.rectangle(frame_resized, (x,y),(x+w-1, y+h-1),(0,0,255),1)
			cv2.circle(frame_resized, centroid,2,(0,255,0),-1)
			
backSub=Detector()
cutting=Transform(listaFile)
#cutting=Transform(listaFile)
cap=cv2.VideoCapture(0)
while(1):
		
	ret, frame=cap.read()
	##draw
	frame=cv2.resize(frame,(320,240))
	#cutIma,listaNew=cutting.cutRegion(frame)
	start=timeit.default_timer()
	cutIma,ListaNew=cutting.cutRegion(frame)
##        vrx=np.array([[ListaNew]],np.int32)
##        pts=vrx.reshape((-1,1,2))
##        cv2.polylines(frame,[pts],True,(255,0,0),2)
	#vrx=np.array([[listaFile]],np.int32)
	#pts=vrx.reshape((-1,1,2))
	#cv2.polylines(frame,[pts],True,(0,0,255),2)
	
	Boxes,movimiento=backSub.findBackSubs(cutIma)
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
	print(movimiento)
	if cv2.waitKey(1)&0xFF==ord('q'):
		# file2.write("\n".listFinal)         
		print('saved!!')
		break
cv2.destroyAll
			
