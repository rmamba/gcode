# coding=utf-8
#!/usr/bin/env python

import spidev
import time
import RPi.GPIO as GPIO

class MCP23S17:
	_spi = None
	_cs = None

	def __init__(self, spi, cs):
		self._spi = spi
		self._cs = cs
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self._cs, GPIO.OUT)
		GPIO.output(self._cs, True)

	def close(self):
		GPIO.setup(self._cs, GPIO.IN)
		GPIO.output(self._cs, False)

	def writeByte1(self, address, data):
		GPIO.output(self._cs, False)
		ret = self._spi.xfer2([0x40, address, data])
		GPIO.output(self._cs, True)
#		print 'setup1: ', ret
		return

	def readByte1(self, address):
		GPIO.output(self._cs, False)
		ret = self._spi.xfer2([0x41, address, 0x00])
		GPIO.output(self._cs, True)
#		print 'read1: ', ret
		return ret[2]

	def writeByte2(self, address, data):
		GPIO.output(self._cs, False)
		ret = self._spi.xfer2([0x42, address, data])
		GPIO.output(self._cs, True)
#		print 'setup2: ', ret
		return

	def readByte2(self, address):
		GPIO.output(self._cs, False)
		ret = self._spi.xfer2([0x43, address, 0x00])
		GPIO.output(self._cs, True)
#		print 'read1: ', ret
		return ret[2]

	def reverseBits(self, val):
		val = ((val & 0xF0) >> 4) | ((val & 0x0F) << 4)
		val = ((val & 0xCC) >> 2) | ((val & 0x33) << 2)
		val = ((val & 0xAA) >> 1) | ((val & 0x55) << 1)
		return val

	def initialise(self):
		self.writeByte1(0x0a, 0x08)
		self.writeByte2(0x0a, 0x08)

		self.writeByte1(0x00, 0x00)
		self.writeByte1(0x03, 0xff)
		self.writeByte1(0x0d, 0xff)
		self.writeByte1(0x12, 0x00)
		self.writeByte1(0x13, 0x00)

		self.writeByte2(0x00, 0x00)
		self.writeByte2(0x03, 0xff)
		self.writeByte2(0x0d, 0xff)
		self.writeByte2(0x12, 0x00)
		self.writeByte2(0x13, 0xff)
		return

	def readSwitches(self):
		sw0 = self.readByte1(0x13)
#		print 'SW0: ', sw0
#		time.sleep(0.1)
		sw1 = self.readByte2(0x13)
#		print 'SW1: ', sw1
		return sw1 * 256 + sw0
