# coding=utf-8
#!/usr/bin/env python

import spidev
import time
import RPi.GPIO as GPIO

class MCP23S17:
	_spi = None
	_cs = None

	MOTOR_X = 0x01
	MOTOR_Y = 0x02
	MOTOR_Z = 0x03
	MOTOR_Z1 = 0x04
	EXTRUDOR_0 = 0x10
	EXTRUDOR_1 = 0x20
	EXTRUDOR_2 = 0x40
	EXTRUDOR_3 = 0x80

#Motor step signals
#Chip0 Bank0
	_X = MOTOR_X
	_Y = MOTOR_Y
	_Z = MOTOR_Z
	_Z1 = MOTOR_Z1
	_E0 = EXTRUDOR_0
	_E1 = EXTRUDOR_1
	_E2 = EXTRUDOR_2
	_E3 = EXTRUDOR_3

#Motor Dir signals
#Chip1 Bank0
	_DirX = MOTOR_X
	_DirY = MOTOR_Y
	_DirZ = MOTOR_Z
	_DirZ1 = MOTOR_Z1
	_DirE0 = EXTRUDOR_0
	_DirE1 = EXTRUDOR_1
	_DirE2 = EXTRUDOR_2
	_DirE3 = EXTRUDOR_3

#Motor enable signals
#Chip1 Bank 1
	_EnX = MOTOR_X
	_EnY = MOTOR_Y
	_EnZ = MOTOR_Z
	_EnZ1 = MOTOR_Z1
	_EnE0 = EXTRUDOR_0
	_EnE1 = EXTRUDOR_1
	_EnE2 = EXTRUDOR_2
	_EnE3 = EXTRUDOR_3

#Output bytes
	_B0 = 0x00		#BANK0 PA
	_B1 = 0x00		#BANK1 PA
	_B2 = 0x00		#BANK1 PB

#Invert bits before byte is send to Chip
	_InvB0 = 0x00	#BANK0 PA
	_InvB1 = 0x00	#BANK1 PB
	_InvB2 = 0x00	#BANK1 PB

	def __init__(self, spi, cs):
		self._spi = spi
		self._cs = cs
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self._cs, GPIO.OUT)
		GPIO.output(self._cs, True)

	def close(self):
		GPIO.setup(self._cs, GPIO.IN)

	#BANK0 = CHIP1
	def writeCH0(self, address, data):
		GPIO.output(self._cs, False)
		ret = self._spi.xfer2([0x40, address, data])
		GPIO.output(self._cs, True)
#		print 'setup1: ', ret
		return

	def readCH0(self, address):
		GPIO.output(self._cs, False)
		ret = self._spi.xfer2([0x41, address, 0x00])
		GPIO.output(self._cs, True)
#		print 'read1: ', ret
		return ret[2]

	#BANK1 = CHIP2
	def writeCH1(self, address, data):
		GPIO.output(self._cs, False)
		ret = self._spi.xfer2([0x42, address, data])
		GPIO.output(self._cs, True)
#		print 'setup2: ', ret
		return

	def readCH1(self, address):
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
		self.writeCH0(0x0a, 0x08)	#enable hardware address
		self.writeCH1(0x0a, 0x08)	#enable hardware address

		#Bank0
		self.writeCH0(0x00, 0x00)	#output PA
		self.writeCH0(0x01, 0xff)	#input PB
		self.writeCH0(0x03, 0xff)	#input polarity PB; 1 = inverted
		self.writeCH0(0x0d, 0xff)	#pullups PB
		self.writeCH0(0x12, 0x00)	#PA
		self.writeCH0(0x13, 0x00)	#PB

		#Bank1
		self.writeCH1(0x00, 0x00)	#output PA
		self.writeCH1(0x01, 0x00)	#output PB
		self.writeCH1(0x12, 0x00)	#PA
		self.writeCH1(0x13, 0x00)	#PB

	def readSwitches(self):
		return self.readCH0(0x13)

	def motorsOFF(self):
		self._B2 = 0x00
		send ^= self._InvB2
		self.writeCH1(0x13, send)

	def motorsON(self):
		self._B2 = 0xff
		send ^= self._InvB2
		self.writeCH1(0x13, send)

	def motorsEN(self, motor):
		self._B2 |= motor
		send ^= self._InvB2
		self.writeCH1(0x13, send)

	def motorsDIS(self, motor):
		self._B2 &= (motor ^ 0xff)
		send ^= self._InvB2
		self.writeCH1(0x13, send)

	def motorsSTEP(self, motor):
		self._B0 = motor
		send ^= self._InvB0
		self.writeCH1(0x12, send)
		self._B0 = 0x00
		send ^= self._InvB0
		self.writeCH1(0x12, send)

	def motorsDIR(self, motor):
		self._B1 = motor
		send ^= self._InvB1
		self.writeCH1(0x12, send)

	def stepMotor(self, motor, dir):
		self.writeByte1(0x01)
