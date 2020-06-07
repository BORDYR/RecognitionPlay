import serial as serial
from tkinter import *
from src import ObjectRecognizer, MySerialRobot, circlerecognizer


class RobotConnection(serial.Serial):
	def __init__(self):
		super().__init__()
		self._port = "COM3"
		self.name = "COM3"
		self._timeout = 100
		self._baudrate = 9600
		self._rtscts = True
		self._parity = serial.PARITY_EVEN
		self.status = False
		self.ending = b'\r'
		print(self.isOpen())

	def open_conection(self):
		self.open()

	def reset_robot(self):
		self.write('RS'.encode()+self.ending)
		self.status = not self.status

	def move_to_point(self, x, y, z):
		message = f'DW {x},{y},{z}'
		self.write(message.encode()+self.ending)

	def move_to_absolute_point(self, x, y, z=353.36, a=0, b=90):
		message = f'MP {x},{y},{z},{a},{b}'
		if self.is_open:
			self.write(message.encode()+self.ending)
			print('command move_to_absolute_point sent')
		else:
			print('port is not open')

	def hand_open(self):
		self.write('GO'.encode()+self.ending)

	def hand_close(self):
		self.write('GC'.encode('utf-16')+self.ending)

	def move(self, p):
		self.write(f'MO {p}'.encode()+self.ending)


class RobotGui():
	def __init__(self, master):
		self.detectedObjects = []
		self.robot = MySerialRobot.MySerialRobot()
		self.frame = master
		self.frame.title('Robot Control Unit')
		self.frame.iconbitmap('pics\pepe.ico')
		self.set_labels()
		self.set_buttons()
		self.e = Entry(self.frame, width=25, borderwidth=5, )
		self.e.grid(row=2, column=0, padx=(10,10))
		self.circlerecognizer = circlerecognizer.Circlerecognizer()

	def set_labels(self):
		Label(self.frame, text=f'''
Using robot spec:
port name: {self.robot.name}
timeout: {self.robot._timeout}
rtscts: {self.robot._rtscts}
parity: {self.robot._parity}
baudrate: {self.robot._baudrate}
stopbits: {self.robot._stopbits}''').grid(row=0, column=0)
		Label(self.frame, text=f'Status: {self.robot.status}')

	def set_buttons(self):
		Button(self.frame, text='Close', command=self.frame.destroy, padx=50).grid(row=5, column=2, padx=(10,10))
		Button(self.frame, text='Reset robot', command=self.reset).grid(row=0, column=2)
		Button(self.frame, text='Move', command=self.move).grid(row=2, column=1)
		Button(self.frame, text='Open Hand', command=self.open_hand).grid(row=4, column=0, pady=(10,10))
		Button(self.frame, text='Close Hand', command=self.close_hand).grid(row=5, column=0, pady=(10,10))
		Button(self.frame, text='Grab objects', command=self.grab_objects).grid(row=1, column=2)

	def reset(self):
		self.robot.resetRobot()
		Label(self.frame, text=f'Status: {self.robot.status}').grid(row=0, column=1)

	def open_hand(self):
		self.robot.openHand()

	def close_hand(self):
		self.robot.closeHand()

	def move(self):
		point = self.e.get()
		if point.isdigit():
			self.robot.moveToSavedPoint(int(point))
		else:
			print("Enter the correct point")

	def start_recognition_process(self):
		recognizer = ObjectRecognizer.ObjectRecognizer()
		self.detectedObjects, self.detectedCircles = recognizer.get_objects_coordinates()

	def grab_objects(self):
		if not self.detectedObjects:
			self.start_recognition_process()
			obj_avail = '\n'.join([str(x) for x in self.detectedObjects])
			Label(self.frame, text=f'{len(self.detectedObjects)} objects available:\n {obj_avail}').grid(row=2, column=2)
		while self.detectedObjects:

			x, y = self.detectedObjects[0]
			xsc, ysc = self.detectedCircles[0]
			self.robot.moveBy3Coordinates(x=x, y=y, z=RobotPositions.upperZ)
			self.robot.moveBy3Coordinates(x=x, y=y, z=RobotPositions.lowerZ)

			self.robot.closeHand()

			self.robot.moveBy3Coordinates(x=x, y=y, z=RobotPositions.upperZ)
			self.robot.moveBy3Coordinates(x=RobotPositions.safeX, y=RobotPositions.safeY, z=RobotPositions.upperZ)
			self.robot.moveBy3Coordinates(x=RobotPositions.safeX, y=RobotPositions.safeY, z=RobotPositions.lowerZ)
			self.robot.openHand()
			self.robot.moveBy3Coordinates(x=RobotPositions.safeX, y=RobotPositions.safeY, z=RobotPositions.upperZ)
			self.circlerecognizer.showOneCircle(x =xsc, y = ysc)

			self.detectedObjects = self.detectedObjects[1:]
			self.detectedCircles = self.detectedCircles[1:]
			print(f'{len(self.detectedObjects)} objects left to move')


class RobotPositions():
	safeX = 64
	safeY = -358
	lowerZ = 306.98
	upperZ = 353.36


if '__main__' == __name__:
	root = Tk()
	app = RobotGui(root)
	root.mainloop()


