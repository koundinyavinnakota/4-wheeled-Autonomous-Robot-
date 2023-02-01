

import numpy as np
import RPi.GPIO as gpio
import time

class motor_control():
	def __init__(self):
		gpio.setmode(gpio.BOARD)
		gpio.setup(31,gpio.OUT)
		gpio.setup(33,gpio.OUT)
		gpio.setup(35,gpio.OUT)
		gpio.setup(37,gpio.OUT)
		gpio.setwarnings(False)
		print("Running motor controls...")

	def game_over(self,reset=False):
		gpio.output(31,False)	#left 
		gpio.output(33,False)	#left
		gpio.output(35,False)	#right
		gpio.output(37,False)	#right
		if reset==True:
			gpio.cleanup()

	def forward(self,tf):
		gpio.output(31,True)	#left 
		gpio.output(33,False)	#left 

		gpio.output(35,False)	#right
		gpio.output(37,True)	#right

		time.sleep(tf)

	def backward(self,tf):
		gpio.output(31,False)	#left 
		gpio.output(33,True)	#left 

		gpio.output(35,True)	#right
		gpio.output(37,False)	#right

		time.sleep(tf)

	def left(self,tf):
		gpio.output(31,True)	#left 
		gpio.output(33,False)	#left 

		gpio.output(35,True)	#right
		gpio.output(37,False)	#right

		time.sleep(tf)

	def right(self,tf):
		gpio.output(31,False)	#left 
		gpio.output(33,True)	#left 

		gpio.output(35,False)	#right
		gpio.output(37,True)	#right

		time.sleep(tf)


	def test_motors(self,tf):

		self.forward(tf)
		self.backward(tf)
		self.left(tf)
		self.right(tf)
		self.game_over()

	def print_controls(self):
		print('CONTROLS')
		print(f'\tw')
		print(f'a\t\t d')
		print(f'\ts')
		print(f'stop = e')
		print(f'quit = q')
	def type_inp(self):
		while True:
			self.print_controls()
			key_press=input("push button: ")
			out=self.key_inp(key_press)
			if out=='e':
				print('STOP')
				self.game_over()
			if out=='q':
				print('QUITTING...')
				self.game_over(True)
				break


	def key_inp(self,event):
		print(f"Key: {event}")
		tf=1
		if event.lower() == "w":
			self.forward(tf)
			print('UP')
		elif event.lower() == "s":
			self.backward(tf)
			print('DOWN')
		elif event.lower() == "a":
			self.left(tf)
			print('LEFT')
		elif event.lower() == "d":
			self.right(tf)
			print('RIGHT')
		elif event.lower() == "q":
			return 'q'
		elif event.lower() == "e":
			return 'e'
		else:
			print('invalid')

if __name__=="__main__":

	mc=motor_control()
	mc.type_inp()


	


