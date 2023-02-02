

import RPi.GPIO as gpio
import numpy as np
import time
import matplotlib.pyplot as plt

class Encoder():
	def __init__(self, signalFL, signalBR, forward, reverse):
		self.signalFL = signalFL
		self.signalBR = signalBR
		self.forward = forward
		self. reverse = reverse

		gpio.setmode(gpio.BOARD)
		gpio.setup(7,gpio.IN,pull_up_down=gpio.PUD_UP)
		gpio.setup(12,gpio.IN,pull_up_down=gpio.PUD_UP)

		gpio.setup(37, gpio.OUT)
		gpio.setup(31, gpio.OUT)
		gpio.setup(33, gpio.OUT)
		gpio.setup(35, gpio.OUT)

	def main(self):
		counter=np.uint64(0)
		button=int(0)

		while True:

			if int(gpio.input(self.signalFL))!=int(button):
				button = int(gpio.input(self.signalFL))
				counter+=1
				print(counter)

			if counter>=960:
				gpio.cleanup()
				print("DONE")
				break

	def drive(self,meters,speed=14,backwards = 0): 
		left_val = []
		right_val = []
		#ticks = meters * 2720
		ticks = meters * 3510
		self.counterFL=np.uint64(0)
		self.counterBR=np.uint64(0)
		buttonFL=int(0)
		buttonBR=int(0)
		if backwards == 0:
			pwmL = gpio.PWM(31,50)
			pwmR = gpio.PWM(37,50)
		else:
			pwmL = gpio.PWM(33,50)
			pwmR = gpio.PWM(35,50)
		time.sleep(1)
		pwmL.start(speed)
		#pwmR = gpio.PWM(37,50)
		pwmR.start(speed*1)

		time.sleep(0.1)

		for i in range(0,1000000):
			print(f"counterFL =  {self.counterFL} ,counterBR = {self.counterBR}")
				# GPIO state: {gpio.input(self.signalFL)}")
			
			left_val.append(gpio.input(self.signalFL))
			right_val.append(gpio.input(self.signalBR))
			
			if int(gpio.input(self.signalFL)) != int(buttonFL):
				buttonFL = int(gpio.input(self.signalFL))
				self.counterFL += 1
			if int(gpio.input(self.signalBR)) != int(buttonBR):
				buttonBR = int(gpio.input(self.signalBR))
				self.counterBR += 1

			if self.counterFL >= ticks or self.counterBR >= ticks:
				pwmL.stop()
				pwmR.stop()
				print("Thanks for playing")
				break
		return left_val,right_val

	def motor(self):
		pwm = gpio.PWM(31,50)
		pwm.start(14)
		for i in range(0,1000000):
			print(gpio.input(self.signalFL))
		pwm.stop()

	def turn(self,degrees,speed,left = 0):
		left_val = []
		right_val = []
		#ticks = meters * 2720
		ticks = degrees * 8
		#ticks = degrees *  
		self.counterFL=np.uint64(0)
		self.counterBR=np.uint64(0)
		buttonFL=int(0)
		buttonBR=int(0)
		if left == 0:
			pwmL = gpio.PWM(31,50)
			pwmR = gpio.PWM(35,50)
		else:
			pwmL = gpio.PWM(33,50)
			pwmR = gpio.PWM(37,50)
		time.sleep(1)
		pwmL.start(speed)
		#pwmR = gpio.PWM(37,50)
		pwmR.start(speed*1)

		

		for i in range(0,1000000):
			print(f"counterFL =  {self.counterFL} ,counterBR = {self.counterBR}")
				# GPIO state: {gpio.input(self.signalFL)}")
			
			left_val.append(gpio.input(self.signalFL))
			right_val.append(gpio.input(self.signalBR))
			
			if int(gpio.input(self.signalFL)) != int(buttonFL):
				buttonFL = int(gpio.input(self.signalFL))
				self.counterFL += 1
			if int(gpio.input(self.signalBR)) != int(buttonBR):
				buttonBR = int(gpio.input(self.signalBR))
				self.counterBR += 1

			if self.counterFL >= ticks or self.counterBR >= ticks:
				pwmL.stop()
				pwmR.stop()
				print("Thanks for playing")
				break
		return left_val,right_val
if __name__=="__main__":
	en=Encoder(12,7,31,33)
	#en.main()
	left_val, right_val = en.drive(1,30,1)
	left_val, right_val = en.turn(90,50,1)
	left_val, right_val = en.turn(180,50,0)
	left_val, right_val = en.turn(90,50,1)
	left_val, right_val = en.drive(1,30,0)

	# plt.subplot(211)
	# plt.title('Motor Encoder Analysis')
	# plt.ylabel('Front Left Encoder')
	# plt.plot(range(10000),left_val[:10000],color='b',label='fl')
	# plt.subplot(212)
	# plt.ylabel('Back Right Encoder')
	# plt.plot(range(10000),right_val[:10000],color='r',label='br')
	# plt.show()
	# en.motor()

