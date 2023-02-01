

import numpy as np
import RPi.GPIO as gpio

def init():
	gpio.setmode(gpio.BOARD)
	gpio.setup(31,gpio.OUT)
	gpio.setup(33,gpio.OUT)
	gpio.setup(35,gpio.OUT)
	gpio.setup(37,gpio.OUT)
	

def game_over():
	gpio.output(31,False)	#left 
	gpio.output(33,False)	#left
	gpio.output(35,False)	#right
	gpio.output(37,False)	#right

	gpio.cleanup()


init()
game_over()