# coding=utf-8
#!/usr/bin/env python

#import spidev
#import time
import RPi.GPIO as GPIO

class MAX31855:
	_spi = None
	_cs0 = None
	_cs1 = None

	_pos = 0
	_temp00 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	_temp01 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	_temp10 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	_temp11 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	def __init__(self, spi, cs0, cs1):
		self._spi = spi
		self._cs0 = cs0
		self._cs1 = cs1
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self._cs0, GPIO.OUT)
		GPIO.output(self._cs0, True)
		GPIO.setup(self._cs1, GPIO.OUT)
		GPIO.output(self._cs1, True)

	def _setCS(self, temp):
		cs = self._cs0
		if temp == 1:
			cs = self._cs1
		GPIO.output(cs, True)

	def _clrCS(self, temp):
		cs = self._cs0
		if temp == 1:
			cs = self._cs1
		GPIO.output(cs, False)

	def readT(self, temp):
		self._clrCS(temp)
#		raw = spi.xfer2([0x00, 0x00, 0x00, 0x00])
		raw = self._spi.readbytes(4)
		self._setCS(temp)
#		print "{0:08b} {1:08b} {2:08b} {3:08b}".format(raw[0], raw[1], raw[2], raw[3])
		val = raw[0] << 24 | raw[1] << 16 | raw[2] << 8 | raw[3]
#		if val & 0x10000:
#			T = float('NaN')
#		else:
		T = val >> 18
		if val & 0x80000000:
			T -= 16384
		val >>= 4
		internal = val & 0x7FF
		if val & 0x800:
			internal -= 4096
		return T * 0.25, internal * 0.0625

	def reverseBits(self, val):
		val = ((val & 0xF0) >> 4) | ((val & 0x0F) << 4)
		val = ((val & 0xCC) >> 2) | ((val & 0x33) << 2)
		val = ((val & 0xAA) >> 1) | ((val & 0x55) << 1)
		return val

