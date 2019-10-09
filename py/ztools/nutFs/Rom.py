from binascii import hexlify as hx, unhexlify as uhx
from struct import pack as pk, unpack as upk
from nutFs.File import File
from nutFs.File import MemoryFile
import os
import re
import pathlib
import Keys
import Print
from nutFs.BaseFs import BaseFs
from nutFs.Ivfc import Ivfc
import Hex
from nutFs import Bktr

MEDIA_SIZE = 0x200
		
class Rom(BaseFs):
	def __init__(self, buffer, path = None, mode = None, cryptoType = -1, cryptoKey = -1, cryptoCounter = -1):
		super(Rom, self).__init__(buffer, path, mode, cryptoType, cryptoKey, cryptoCounter)
		if buffer:
			self.ivfc = Ivfc(MemoryFile(buffer[0x8:]), 'rb')
			self.magic = buffer[0x8:0xC]
			self.bktr1 = Bktr.Header(MemoryFile(buffer[0x100:0x120]), 'rb')
			self.bktr2 = Bktr.Header(MemoryFile(buffer[0x120:0x140]), 'rb')
			#Hex.dump(buffer)
			#self.sectionStart = self.ivfc.levels[5].offset
		else:
			self.ivfc = None
			self.bktr1 = None
			self.bktr2 = None

	def open(self, path = None, mode = 'rb', cryptoType = -1, cryptoKey = -1, cryptoCounter = -1):
		r = super(Rom, self).open(path, mode, cryptoType, cryptoKey, cryptoCounter)


	def printInfo(self, maxDepth = 3, indent = 0):
		tabs = '\t' * indent
		Print.info('\n%sRom' % (tabs))
		if self.ivfc:
			Print.info('%sMagic = %s' % (tabs, self.ivfc.magic))
			Print.info('%sLevels = %d' % (tabs, self.ivfc.numberLevels))
			Print.info('%sHash = %s' % (tabs, hx(self.ivfc.hash).decode()))
			if self.ivfc.numberLevels < 16:
				for i,level in enumerate(self.ivfc.levels):
					Print.info('%sLevel%d offset = %d' % (tabs, i, level.offset))
					Print.info('%sLevel%d size = %d' % (tabs, i, level.size))
					Print.info('%sLevel%d blockSize = %d' % (tabs, i, level.blockSize))

		self.bktr1.printInfo(maxDepth, indent)
		self.bktr2.printInfo(maxDepth, indent)
		'''
		self.seek(0)
		level1 = self.read(0x4000)
		Print.info('%ssha = %s' % (tabs, sha256(level1).hexdigest()))
		Hex.dump(level1)
		'''
		super(Rom, self).printInfo(maxDepth, indent)


