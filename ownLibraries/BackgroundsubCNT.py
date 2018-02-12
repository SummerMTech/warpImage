import cv2
import bgsubcnt
from multiprocessing import Process, Queue, Pool



class CreateBGCNT():

	"""
	CLASS used to create BGCNT for purposes of extract the rectangle where the 
	car is in the screen, inputs: cls.visual(frame), outputs: list((rectanglex, rectangley)) positions.
	"""
	def __init__(self):
		# Define the parameters needed for motion detection

		self.fgbg = bgsubcnt.createBackgroundSubtractor(3, False, 3*60)
		self.k = 31
		self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
		self.min_contour_width=30
		self.min_contour_height=30

		self.input_q = Queue(maxsize=5)
		self.output_q = Queue(maxsize=5)

		self.process = Process(target= self.worker, args=(self.input_q, self.output_q))
		self.process.daemon = True

		pool = Pool(2,self.worker, (self.input_q, self.output_q))

		self.matches = None

	def alimentar(self, current_frame):
		self.frame_resized = current_frame
		self.input_q.put(self.frame_resized)
		matches = self.output_q.get()
		self.matches = matches

	def worker(self, input_q, output_q):

		while True:

			matches = []

			gray = cv2.cvtColor(input_q.get(), cv2.COLOR_BGR2GRAY)

			smooth_frame = cv2.GaussianBlur(gray, (self.k,self.k), 1.5)
			#smooth_frame = cv2.bilateralFilter(gray,4,75,75)
			#smooth_frame =cv2.bilateralFilter(smooth_frame,15,75,75)
			self.fgmask = self.fgbg.apply(smooth_frame, self.kernel, 0.1)

			im2, contours, hierarchy = cv2.findContours(self.fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
			for (i, contour) in enumerate(contours):
			    (x, y, w, h) = cv2.boundingRect(contour)
			    contour_valid = (w >= self.min_contour_width) and (h >= self.min_contour_height)
			    if not contour_valid:
			        continue
			    centroid = CreateBGCNT.get_centroid(x, y, w, h)

			    matches.append(((x, y, w, h), centroid))
			output_q.put(matches)


	@staticmethod
	def distance(x, y, type='euclidian', x_weight=1.0, y_weight=1.0):

		if type == 'euclidian':
			return math.sqrt(float((x[0] - y[0])**2) / x_weight + float((x[1] - y[1])**2) / y_weight)

	@staticmethod
	def get_centroid(x, y, w, h):
		x1 = int(w / 2)
		y1 = int(h / 2)

		cx = x + x1
		cy = y + y1

		return (cx, cy)
		
	def draw(self):
		for (i, match) in enumerate(self.matches):
			contour, centroid = match[0], match[1]
			x,y,w,h = contour
			cv2.rectangle(self.frame_resized, (x,y),(x+w-1, y+h-1),(0,0,255),1)
			cv2.circle(self.frame_resized, centroid,2,(0,255,0),-1)
		#cv2.imshow('boxes', self.frame_resized)



if __name__=='__main__':


	from videostream import VideoStream
	from videostream import FPS


	fuente = ['../installationFiles/mySquare.mp4', 0]

	# Create  BG object and get source input
	bg = CreateBGCNT()
	vs = VideoStream(src = fuente[0], resolution = (640, 480)).start() # 0.5 pmx

	fps = FPS().start()

	while True:
		frame, frame_resized = vs.read()
		# Feed frames
		bg.alimentar(frame_resized)

		# You want the matches?
		#print(bg.matches)

		# Want to see?, put the next two lines
		bg.draw()
		cv2.imshow('frame', frame_resized)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	 
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()