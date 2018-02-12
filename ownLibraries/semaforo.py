#!/usr/bin/env python
# semaforoFinal.py

import cv2
import numpy as np
import os
import pickle
import time
import threading

from abc import ABCMeta, abstractmethod

class Semaforo(object):
	"""
	Semaforo object

	Attributes:

		self.numericValue : Integer like, values: 1 for red
										   0 for Green
										   -1 for Not found
		self.flanco : Integer like, values: -1 for Red to Green
											1 for Green to Yellow or Red
		self.state : String like, values : Green, Yellow, Red

		self.previous_state : self.state like

	"""

	__metaclass__ = ABCMeta


	def __init__(self):
		print('HELLO FROM SEMAFORO PARENT')
		self.flanco = 0
		self.state = 'verde'
		self.previous_state = 'rojo'
		self.numericValue = -1
		self.counter = 0

	
	def correrCronometro(self, periodoSemaforo, sleeptime):
		# Run chronometer and reset self.flanco to 0 once that the
		# pulse has been send.
		print('Returning pulse ..flanco:', self.flanco)
		#
		# After pulse has been send, self.flanco set to 0 again
		#
		self.flanco = 0
		if self.state == 'amarillo':
			# Default peridoSemaforo for amarillo set to 3 seconds.
			periodoSemaforo = 3
		else:
			pass
		for number in range(periodoSemaforo):
			time.sleep(sleeptime)
			self.counter = number
			self.counter += 1
	
	def comparation(self, periodoSemaforo, sleeptime):

		# RED
		if self.state == 'rojo':
			self.numericValue = 1
			self.kroneckerlike(current= self.state, passt=self.previous_state)
			# Run cronometro
			self.correrCronometro(periodoSemaforo, sleeptime)
			self.previous_state = self.state
			self.state = 'verde'
			self.counter = 0
		# Green
		if self.state == 'verde':
			self.numericValue = 0
			self.kroneckerlike(current= self.state, passt=self.previous_state)
			# Run Cronometro
			self.correrCronometro(periodoSemaforo, sleeptime)		
			self.previous_state = self.state
			self.state = 'amarillo'
			self.counter = 0

		# Yellow
		if self.state =='amarillo':
			self.numericValue = 2
			self.kroneckerlike(current= self.state, passt=self.previous_state)
			# Run cronometro
			self.correrCronometro(periodoSemaforo, sleeptime)
			self.previous_state = self.state
			self.state = 'rojo'
			self.counter = 0



	def kroneckerlike(self, current=None, passt=None):
		#
		# Compare the current and pass colors to set self.flanco value 
		#
		if current == passt:
			#print('{},{} are the same, ...passing flanco:{}'.format(i,j,0))
			self.flanco = 0
			return self.flanco
		elif current == 'rojo' and passt == 'amarillo':
			#print('from {} to {} ...passing flanco:{}'.format(passt, current, 1))
			self.flanco = 1
			return self.flanco
		
		elif current == 'verde' and passt == 'rojo':
			#print('from {} to {} ...passing flanco:{}'.format(passt, current, -1))
			self.flanco = -1
			return self.flanco

		elif current == 'amarillo' and passt == 'verde':
			#print('from {} to {} ...passing flanco:{}'.format(passt, current, 1))
			self.flanco = 1
			return self.flanco

		else:
			print('No match found {}, {}, returning 0',format(current, passt))
			return 0
	
	# Method to be _heredado_ to childs.
	@abstractmethod
	def encontrarSemaforoObtenerColor(self, poligono = None, imagen = None):
		return self.numericValue, self.state, self.flanco


class Simulado(Semaforo):

	""" Simulated Semaforo that runs forever in the Background once that this object
	is created

	Attributes:
		self.periodoSemaforo = Tiempo entre colores, por default amarillo es 3 segundos
		self.sleeptime = 1, es el tiempo por defecto para el cronometro interno
		super().__init__(), es para iniciar los atributos de la clase parent.
		thread, es el proceso paralelo que se crea para que el programa corra 
				de forma continua en el Background
		Simulado.run(), es el progreso que se mantiene constante en el thread
	"""

	def __init__(self, periodoSemaforo = 10 ):
		print( 'STARTING .... SEMAFORO SIMULADO')
		self.periodoSemaforo = periodoSemaforo
		self.sleeptime = 1

		# Init parent class attributes
		super().__init__()
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True                            # Daemonize thread
		thread.start()                                  # Start the execution

	def run(self):
		Semaforo.comparation(self, self.periodoSemaforo, self.sleeptime)
		# Runing again the run() method.
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True                            # Daemonize thread
		thread.start() 

	
	def encontrarSemaforoObtenerColor(self, poligono = None, imagen = None):
		# Parent method 
		return self.numericValue, self.state, self.flanco




class Real(Semaforo):
	"""
	Real Method,  use a SVM classifier to find color in some input ROI imagen, ouputs are:
	colorPrediction, literalColour, flanco

	Attributes:
		self.svm: 	load the Machine Learning, Support Vector Machine model trained on Red, Green, Black images 

		self.lower_yellow and so on... are range of colors where the SVM  where trained and
										the input image of the semaforo is thressholded.

	"""

	def __init__(self):

		# LOAD THE TRAINED SVM MODEL ... INTO THE MEMORY????
		print( 'WILLKOMEN TO  REAL REAL REAL SEMAFORO')
		print( 'checking for model....')
		if os.path.isfile("./model/svm_model.pkl"):
			print("Model Found!!!!")
			print ("Using previous model... svm_model.pkl")
			self.svm = pickle.load(open("./model/svm_model.pkl", "rb"))
		else:
			print ("No model, retrain DUde!!")

		# Init parent class attributes
		super().__init__()
		#
		# SOME COLORS
		#
		# YELLOW /(Orangen) range
		self.lower_yellow = np.array([18,40,190], dtype=np.uint8)
		self.upper_yellow = np.array([27,255,255], dtype=np.uint8)

		# RED range
		self.lower_red = np.array([140,100,0], dtype=np.uint8)
		self.upper_red = np.array([180,255,255], dtype=np.uint8)

		# GREEN range
		self.lower_green = np.array([70,120,0], dtype=np.uint8)
		self.upper_green = np.array([90,180,255], dtype=np.uint8)

		# SOME VARIABLES for SVM, if retrain the SVM in another
		# resolution, change this val to this resolution.
		self.SHAPE = (30,30)

		# SOME AUXILIAR VARIABLES:
		self.ultimoColorValido = - 1
		self.tiempoAbsoluto = time.time()
		self.periodoSemaforo = time.time()
		self.porcentajeExitoEncontrarColor = 0
		self.exitoColor = 0
		self.fracasoColor = 0

	def find_color(self, imagen):

		"""
		Load some semaforo Image and find color on it using svm_model
		"""
		# Load image and some magic	
		img = imagen
		#cv2.imshow('semaforo', cv2.resize(img,(img.shape[1]*5,img.shape[0]*5)))
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		
		# SOME MASKS
		mask_red = cv2.inRange(hsv, self.lower_red, self.upper_red)
		mask_yellow = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
		mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)

		full_mask = mask_red + mask_yellow + mask_green

		# Put the mask and filter the R, Y , G colors in _imagen_
		res = cv2.bitwise_and(img,img, mask= full_mask)



		#res = cv2.GaussianBlur(res,(15,15),2)

		#res = cv2.medianBlur(res,15)

		#res = cv2.bilateralFilter(res,30,75,75,75/2)
		res = cv2.bilateralFilter(res,35,75,75)




		#cv2.imshow('res', cv2.resize(res,(res.shape[1]*5,res.shape[0]*5)))
		###########################
		# SVM PART (CLASSIFICATION) ML PROCESS
		###########################
		img = cv2.resize(res, self.SHAPE, interpolation = cv2.INTER_CUBIC)

		#cv2.imshow('res2', cv2.resize(img,(img.shape[1]*5,img.shape[0]*5)))
		# LitleDebug for see what is the SVM seeing
		#cv2.imwrite('red2.jpg', img)

		img = img.flatten()

		# Some numerical corrections
		feature_img = img/(np.mean(img)+0.0001)
		x = np.asarray(feature_img)
  
		x = x.reshape(1, -1)
		prediction = self.svm.predict(x)[0]
		###########################
		# END SVM PART (CLASSIFICATION) ML PROCESS
		###########################

		# Return prediction from SVM
		if prediction == 'green':
			return 0
		elif prediction == 'red':
			return 1
		elif prediction == 'black':
			return -1
		else:
			pass

	def encontrarSemaforoObtenerColor(self,poligono, imagen):
		# Find the color in this piece of poligono and
		# return colorPrediction, literalColour, self.flanco

		literalColour = 'error?'

		ignore_mask_color = (255,) * 3
		# find MAX, MIN values  in poligono
		maxinX = max([x[0] for x in poligono])
		maxinY = max([y[1] for y in poligono])

		mininX = min([x[0] for x in poligono])
		mininY = min([y[1] for y in poligono])

		x0 = mininX
		x1 = maxinX

		y0 = mininY
		y1 = maxinY

		# Create mask of Zeros with shape iqual to image input shape.
		mask =  np.zeros((imagen.shape[0], imagen.shape[1],imagen.shape[2]), np.uint8)

		# Adjust poligono to mask
		fillPolyImage = cv2.fillPoly(mask, np.array([poligono]), ignore_mask_color)

		# All zeros except the poligon region in image input
		masked_image = cv2.bitwise_and(imagen,mask)

		# Feed to the SMV with cuted masked_image using max and min points (rectangle like)
		# again, all zeros except poligion region of interest.

		colorPrediction = self.find_color(masked_image[y0:y1,x0:x1])

		if colorPrediction == 1:
			literalColour = 'ROJO'
			Semaforo.state = 'rojo'
		elif colorPrediction == 0:
			literalColour = 'VERDE'
			Semaforo.state = 'verde'
		else:
			literalColour = 'No hay Semaforo'
			Semaforo.state = None

		
		if (colorPrediction == 0) | (colorPrediction == 1):
			self.exitoColor +=1
			if (colorPrediction != self.ultimoColorValido)&(colorPrediction == 0):	# Si el semaforo cambia de estado, a VERDE, se guarda el tiempo de duración del último periodo
				Semaforo.flanco = -1
				self.periodoSemaforo = time.time() - self.tiempoAbsoluto
				self.tiempoAbsoluto = time.time()
				self.porcentajeExitoEncontrarColor = self.exitoColor/(self.exitoColor+self.fracasoColor)
				self.exitoColor = 0
				self.fracasoColor = 0
			if (colorPrediction != self.ultimoColorValido)&(colorPrediction == 1):	# Si el semaforo cambia de estado, a ROJO,
				Semaforo.flanco = 1
			self.ultimoColorValido = colorPrediction
			
		else:
			colorPrediction = self.ultimoColorValido
			self.fracasoColor +=1	
		
		# Si el numero de fracasos asciende a 150 el semaforo vuelve a condiciones iniciales parciales
		if self.fracasoColor > 150:		# A 200 ms, 150 representa semaforo perdido por 50 segundos
			colorPrediction = -1
			self.ultimoColorValido = -1
    		
		return colorPrediction, literalColour, self.flanco
	

class CreateSemaforo(Semaforo):
	"""
	Create the requested semaforo according the the periodoSemaforo values,
	Attributes:
		periodoSemaforo == 0 for Real semoforo creation
		periodoSemaforo != for Simulated Semaforo
		self.blueprint_semaforo, is the interface for parent and childs classes attributes 
								and methods sharing.
	"""
	def __init__(self, periodoSemaforo=30):
		self.periodoSemaforo = periodoSemaforo
		#
		# Init parent attributes and methods
		#
		super().__init__()
		self.littleFilter = [0,0,0,0,0]
		self.blueprint_semaforo = None
		self.numericoAuxiliar = 0
		if self.periodoSemaforo > 0 :
			self.blueprint_semaforo =  Simulado(periodoSemaforo = self.periodoSemaforo)
		else:
			self.blueprint_semaforo = Real()
	
	def obtenerColorEnSemaforo(self, img, poligono):
		numerico, literal, flancoErrado = self.blueprint_semaforo.encontrarSemaforoObtenerColor(poligono = poligono, imagen = img )
		if self.periodoSemaforo == 0 :
			self.littleFilter[4] = self.littleFilter[3]
			self.littleFilter[3] = self.littleFilter[2]
			self.littleFilter[2] = self.littleFilter[1]
			self.littleFilter[1] = self.littleFilter[0]
			self.littleFilter[0] = numerico
			numeroDeVerdes = 0
			numeroDeRojos = 0
			for colorNumeral in self.littleFilter:
				if colorNumeral==0:
					numeroDeVerdes+=1
				if colorNumeral==1:
					numeroDeRojos+=1
			if numeroDeRojos>=3:
				numerico = 1
			if numeroDeVerdes>=3:
				numerico = 0


		flancoCorrecto = 0
		# Si llegue a un valor valido entonces es posible generar flanco
		if (numerico==0)|(numerico==1)|(numerico==2):
			#Si hay cambio entonces genero flanco:
			if numerico != self.numericoAuxiliar:
				if numerico == 0:
					flancoCorrecto = -1
				elif numerico >= 1:
					flancoCorrecto = 1
				if (self.numericoAuxiliar == 2)&(numerico==1):		# Si el valor anterior es amarillo se descarta el flanco
					flancoCorrecto = 0
				self.numericoAuxiliar = numerico
		else: # Si no llego a un valor valido repito
			numerico = self.numericoAuxiliar
		return numerico, literal, flancoCorrecto


if __name__ == '__main__':
	cap = cv2.VideoCapture('./installationFiles/sar.mp4')
	data = np.load('./installationFiles/sar.npy')
	print(data)
	semaforo = CreateSemaforo(periodoSemaforo = 0)
	poligono  = data[0]
	print(data[0])
	while True:
		_, img = cap.read()

		print(semaforo.obtenerColorEnSemaforo(imagen = img, poligono = poligono))
		
		#cv2.imshow('mask_image',img)

		ch = 0xFF & cv2.waitKey(5)
		if ch == 27:
			break
	cv2.destroyAllWindows()
	c = cv2.waitKey(0)