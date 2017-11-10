import numpy as np
import cv2
from cutImage import Transform
import timeit
lista=[]

def get_BigRectangle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        lista.append((x,y))
        if len(lista)!=0:
            cv2.circle(frame, (x,y),3,(0,255,0),-1)
            cv2.imshow('First_Frame',frame)
    
try:
		#cap=cv2.VideoCapture(directorioDeVideos+nameSourceVideo)
		cap=cv2.VideoCapture('officialTrialVideos/sar.mp4')
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
		#print('lista: '+str(lista))
		#print('ListaAux Removed...'+ str(listaAux))
		overlay=frame.copy()
	if keyPress == 27:
		print('_____Data not accept..')
		print('*Select two points next press -a- to obtain Angle')
		#print('lista no append: '+str(lista))
		lista=[]
		#print('ListaAux Removed...'+ str(listaAux))
		frame=overlay.copy()
		cv2.imshow('First_Frame',frame)
	
	if keyPress&0xFF==ord('q'):
		# file2.write("\n".listFinal)         
		print('saved!!')
		break
cv2.destroyAllWindows()

cutting=Transform(lista)
cap=cv2.VideoCapture('officialTrialVideos/sar.mp4')
while(1):
	ret, frame=cap.read()
	frame=cv2.resize(frame,(320,240))
	start=timeit.default_timer()	
	cutIma=cutting.cutRegion(frame)
	lapso=timeit.default_timer()
	tim=lapso-start
	print(tim)
	cv2.imshow('original',frame)
	cv2.imshow('cutting',cutIma)
	if cv2.waitKey(1)&0xFF==ord('q'):
		# file2.write("\n".listFinal)         
		print('saved!!')
		break
cv2.destroyAllWindows()
