# coding=utf-8
#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

class LCD12864R:
	SD = -1
	CLK = -1
	CS = -1
	_delay = -1

	def __init__(self, sd, cs, clk, delay = 0.001):
		self._SD = sd
		self._CS = cs
		self._CLK = clk
		self._delay = delay
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self._SD, GPIO.IN)
		GPIO.setup(self._CLK, GPIO.OUT)
		GPIO.setup(self._CS, GPIO.OUT)
		self._clearIO(self._CS)
		self._clearIO(self._CLK)

	def close(self):
		GPIO.setup(self._SD, GPIO.IN)
		GPIO.setup(self._CLK, GPIO.IN)
		GPIO.setup(self._CS, GPIO.IN)
		self._clearIO(self._SD)
		self._clearIO(self._CLK)
		self._clearIO(self._CS)

	def _setIO(self, io):
		GPIO.setup(io, True)

	def _clearIO(self, io):
		GPIO.setup(io, False)

	def _shiftOut(self, val):
		GPIO.setup(self._SD, GPIO.OUT)
		time.sleep(self._delay)
		for i in range(0, 8):
			if val & 0x80:
				self._setIO(self._SD)
			else:
				self._clearIO(self._SD)
			GPIO.output(self._CLK, True)
			time.sleep(self._delay)
			GPIO.output(self._CLK, False)
			time.sleep(self._delay)
			val <<= 1
		GPIO.setup(self._SD, GPIO.IN)
#		time.sleep(self._delay)

	def writeByte(self, val):
		self._setIO(self._CS)
		self._shiftOut(val)
		self._clearIO(self._CS)

	def writeCommand(self, cmd):
		h = cmd & 0xf0
		l = cmd & 0x0f
		l <<= 4
		self.writeByte(0xf8)
		self.writeByte(h)
		self.writeByte(l)

	def writeData(self, cmd):
		if not isinstance(cmd, (int, long)):
			cmd = ord(cmd)
		h = cmd & 0xf0
		l = cmd & 0x0f
		l <<= 4
		self.writeByte(0xfa)
		self.writeByte(h)
		self.writeByte(l)

	def initDisplay(self):
		self.writeCommand(0x30)
		self.writeCommand(0x0c)
		self.writeCommand(0x01)
		self.writeCommand(0x06)

	def clear(self):
		self.writeCommand(0x30)
		self.writeCommand(0x01)

	def displayString(self, x, y, str):
		if x == 0:
			y |= 0x80
		elif x == 1:
			y |= 0x90
		elif x == 2:
			y |= 0x88
		elif x == 3:
			y |= 0x98
		elif x == 1:
			y |= 0x90
		self.writeCommand(y)
		for i in range(0, len(str)):
			self.writeData(str[i])

	def displayChar(self, x, y, ch):
		if x == 0:
			y |= 0x80
		elif x == 1:
			y |= 0x90
		elif x == 2:
			y |= 0x88
		elif x == 3:
			y |= 0x98
		elif x == 1:
			y |= 0x90
		self.writeCommand(y)
		self.writeData(ch)

	def drawFullScreen(self, data):
		for ygroup in range(0, 64):
			x = 0x88
			y = ygroup + 0x80
			if ygroup>=32:
				y -= 32
		self.writeCommand(0x34)
		self.writeCommand(y)
		self.writeCommand(x)
		self.writeCommand(0x30)
		tmp = ygroup * 16
		for i in range(0, 16):
			self.writeData(data[tmp+i])
		self.writeCommand(0x34)
		self.writeCommand(0x36)

	def img1(self, img):
		for page in range(0xb0, 0xb4):
			self.writeCommand(page)
			self.writeCommand(0x10)
			self.writeCommand(0x04)
			i = (0xb3 - page) * 0x80
			for col in range(0, 0x80):
				self.writeData(img[i+col])
		self.writeCommand(0x34)
		self.writeCommand(0x36)

	def img2(self, img):
		for page in range(0xb4, 0xb8):
			self.writeCommand(page)
			self.writeCommand(0x10)
			self.writeCommand(0x04)
			i = (0xb7 - page) * 0x80
			for col in range(0, 0x80):
				self.writeData(img[i+col])
		self.writeCommand(0x34)
		self.writeCommand(0x36)
