class MySerialRobot():
	def __init__(self):
		self._port = "COM3"
		self.name = "COM3"
		self._timeout = 100
		self._baudrate = 9600
		self._rtscts = True
		self._parity = 'PARITY_EVEN'
		self._stopbits = 1
		self.status = True
		self.isHandOpen = False
		self.xCoord = 0
		self.yCoord = 0
		self.zCoord = 0

	def resetRobot(self):
		self.status = True

	def write(self, cmd):
		return(cmd + 'done!')

	def isOpen(self):
		return self.status

	def openHand(self):
		self.isHandOpen = True
		return('Hand is open')

	def closeHand(self):
		self.isHandOpen = False
		return('Hand is closed')

	def moveToSavedPoint(self, p):
		print(f'Moved to point {p}')
		return(f'Moved to {p} point')

	def moveBy3Coordinates(self, x, y, z):
		self.xCoord = x
		self.yCoord = y
		self.zCoord = z
		return(f'Hand moved to x:{x}, y:{y}, z:{z}')

