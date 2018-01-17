import time
import RPi.GPIO as IO



class Light(object):
	def __init__(self, port):
		self.port = port
		IO.setwarnings(False)
		IO.setmode(IO.BCM)
		IO.setup(self.port, IO.OUT)
		self.on = IO.HIGH
		self.off = IO.LOW

	def turn_on(self):
		IO.output(self.port, self.on)

	def turn_off(self):
		IO.output(self.port, self.off)

	def is_on(self):
		return IO.input(self.port) == self.on

	def is_off(self):
		return IO.input(self.port) == self.off

	def party(self, t=0.5):

		#while True:
		IO.output(self.port, self.on)
		time.sleep(t)
		IO.output(self.port, self.off)
		time.sleep(t)
		IO.output(self.port, self.on)
		time.sleep(t)
		IO.output(self.port, self.off)
		time.sleep(t)
		IO.output(self.port, self.on)
		time.sleep(t)
		IO.output(self.port, self.off)
		time.sleep(t)

	def switch(self):
		if self.is_on():
			self.turn_off()
		else:
			self.turn_on()


if __name__ == "__main__":
	light = Light(18)
	while True:
		light.party()
		time.sleep(0.5)
