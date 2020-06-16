import cv2 as cv2
from src import AffineTransform, circlerecognizer
import time

class ObjectRecognizer():
	def __init__(self):
		self.matrix_transformator = AffineTransform.AffineTransform()
		self.circlerecognizer = circlerecognizer.Circlerecognizer()

	def __del__(self):
		cv2.destroyAllWindows()



	def start_recognition(self, iterations = 0, cameraTestMode=True):
		circle_rating = {}

		if cameraTestMode:
			img = cv2.imread('pics/e2.jpg')
			if iterations:
				for _ in range(iterations):
					frame = img
					circle_rating, outer = self.circlerecognizer.circle_recognise(frame)  # распознавание кругов
					cv2.imshow('Recognition process...', outer)
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
		else:
			cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

			if iterations:
				for _ in range(iterations):
					if (cap.isOpened()):
						ret, frame = cap.read()
						ret = True
						if ret:
							circle_rating, outer = self.circlerecognizer.circle_recognise(frame) # распознавание кругов
							cv2.imshow('Recognition process...', outer)
						else:
							break
						if cv2.waitKey(1) & 0xFF == ord('q'):
							break

			cap.release()
		if circle_rating:
			return circle_rating
		else:
			print('No objects detected')
			raise ValueError

	def get_defined_circles(self, circles_rating, n: int):
		defined_circles = []
		for k, v in circles_rating.items():
			if v > n/2:
				defined_circles.append(k.split(', ')[:2])
		print(f'Finally there are {len(defined_circles)} objects:')
		print(defined_circles)
		return defined_circles

	def get_objects_in_right_order(self, defined_circles: list):
		if len(defined_circles) == 1:
			return defined_circles
		else:
			for i in range(len(defined_circles)-1):
				if defined_circles[i][1] > defined_circles[i+1][1]:
					defined_circles[i], defined_circles[i+1] = defined_circles[i+1], defined_circles[i]
			return defined_circles

	def get_objects_coordinates(self, cameraTestMode=True):
		t = time.time()
		scan_frames_number: int = 50 # scan_frames_number is times of circle scan
		circles = self.start_recognition(scan_frames_number, cameraTestMode)
		def_circles = self.get_defined_circles(circles, scan_frames_number)
		ordered_circles = self.get_objects_in_right_order(def_circles)
		converted_circles = self.matrix_transformator.convert_to_absolute_coordinates(ordered_circles)
		print(f'Recognition process took {round(time.time() - t, 2)} seconds')
		return converted_circles, ordered_circles
