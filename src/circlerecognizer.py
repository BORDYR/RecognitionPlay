import numpy as np
import collections
import cv2
import time


class Circlerecognizer():
	def __init__(self):
		self.circles_rating = collections.defaultdict(int)

	def viewImage(self, image, window : str):
		cv2.namedWindow(window, cv2.WINDOW_NORMAL)
		cv2.imshow(window, image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def circle_recognise(self, image):
		output = image.copy()
		circles = self.get_circles(image)
		if (circles is not None) :
			circles = np.round(circles[0, :]).astype("int")
			for (x, y, r) in circles:
				x, y, r = x.item(), y.item(), r.item()
				cv2.circle(output, (x, y), r, (0, 255, 0), 4)
				print(f'Circle has been detected! x = {x}p, y = {y}p, r = {r}p')
				cir = f'{x}, {y}, {r}'
				self.circles_rating[cir] += 1
		else:
			print('Circles haven\'t been found')
		return dict(self.circles_rating), output

	def get_circles(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5, 5), 0)
		circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=2, minDist=52, minRadius=25, maxRadius=32)
		return circles

	def showOneCircle(self, x, y, r=29):
		img = cv2.imread('pics/e2.jpg')
		img = img.copy()
		cv2.circle(img, (int(x), int(y)), r, (0, 0, 255), 4)
		cv2.imshow('Moving...', img)
		cv2.waitKey(1)
		time.sleep(1)
