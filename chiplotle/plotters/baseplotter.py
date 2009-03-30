'''
 *  This file is part of chiplotle.
 *
 *  http://music.columbia.edu/cmc/chiplotle
'''
from __future__ import division
from chiplotle.hpgl import commands 
from chiplotle.plotters import margin
import math
import serial
import time
import types


class _BasePlotter(object):
   def __init__(self, serialPort):
      self.type = 'Generic'
      self.memory = []
      self._serialPort = serialPort
      self._hpgl = commands
      self.bufferSize = self._bufferSpace

      ## Only these commands will be sent to the plotter. 
      self.allowedHPGLCommands = tuple([
      '(', ')', 'AA','AR','CA','CI','CP','CS','DC','DF','DI','DP',
      'DR','DT','EA','ER','EW','FT','IM','IN','IP','IW','LB','LT',
      'OA','OC','OD','OE','OF','OH','OI','OO','OP','OS','OW','PA',
      'PD','PR','PS','PT','PU','RA','RO','RR','SA','SC','SI','SL',
      'SM','SP', 'SR','SS','TL','UC','VS','WG','XT','YT'])

      self.marginHard = margin._MarginsHard(self)
      self.marginSoft = margin._MarginsSoft(self)

      self.initializePlotter()


   ### PUBLIC METHODS ###

   def initializePlotter(self):
      self._serialPort.flushInput()
      self._serialPort.flushOutput()
      self.write(self._hpgl.On())
      self.write(self._hpgl.IN())


   def write(self, data):
      '''Public access for writing to serial port. 
         data can be an iterator, a string or an _HPGLCommand. '''
      if type(data) in (list, tuple, types.GeneratorType):
         for c in data:
            self.write(c) 
      elif hasattr(data, 'format'):
         self._writeStringToPort(data.format)
      elif isinstance(data, str):
         self._writeStringToPort(data)
      else:
         raise ValueError('Invalid value. \
         Must be str, iterator or _HPLGCommand.')


   ### PRIVATE METHODS ###

   def _sleepWhileBufferFull(self):
      '''
         sleeps until the buffer has some room in it.
      '''
      if self._bufferSpace < self.bufferSize:
         #print 'Buffer getting full, sleeping...'
         while self._bufferSpace < self.bufferSize:
            time.sleep(1)
         #print 'Okay, now buffer has room...'


   def _sliceStringToBufferSize(self, data):
         result = [ ]
         count = int(math.ceil(len(data) / self.bufferSize))
         for i in range(count):
            result.append(data[i * self.bufferSize: (i+1) * self.bufferSize])
         return result


   def _writeStringToPort(self, data):
      ''' Write data to serial port.
      -data- is expected to be of type string.'''
      assert type(data) is str
      data = self._sliceStringToBufferSize(data)
      for chunk in data:
         self._sleepWhileBufferFull( )
         self._serialPort.write(chunk)
      

   ### PRIVATE QUERIES ###


   def _readPort(self):
      '''Read data from serial port.'''
      while self._serialPort.inWaiting( ) == 0:
         time.sleep(1.0 / 64)
      result = self._serialPort.readline(eol='\r')
      #print repr(result)
      return result
   

   @property
   def _bufferSpace(self):
      #print "getting _bufferSpace..."
      self._serialPort.flushInput()
      self._serialPort.write(self._hpgl.B().format)
      bs = self._readPort()
      #print "buffer space: ", bs
      return int(bs)


   def _isCommandKnown(self, hpglCommand):
      '''Filter out unknown command and tell us about it.'''
      if hpglCommand._name in self.allowedHPGLCommands:
         return True
      else:
         print "*** WARNING: Command [%s] not understood by %s plotter." \
         % (hpglCommand._name, self.type)
         return False


   ### PUBLIC QUERIES (PROPERTIES) ###

   @property
   def id(self):
      '''Get id of plotter.'''
      self._serialPort.flushInput()
      self.write(self._hpgl.OI())
      
      id = self._readPort()
      return id.strip('\r')

   @property
   def actualPosition(self):
      '''Output the actual position of the plotter pen.'''
      self.write(self._hpgl.OA())
      return self._readPort()

   @property
   def carouselType(self):
      command = self._hpgl.OT( )
      if self._isCommandKnown(command):
         self.write(command)
         return self._readPort()

   @property
   def commandedPosition(self):
      self.write(self._hpgl.OC())
      return self._readPort()
          
   @property
   def digitizedPoint(self):
      self.write(self._hpgl.OD())
      return self._readPort()

   @property
   def outputError(self):
      self.write(self._hpgl.OE())
      return self._readPort()

   @property
   def hardClipLimits(self):
      '''Output hard clip limits. Same as marginHard.'''
      self.write(self._hpgl.OH())
      return self._readPort()

   @property
   def outputKey(self):
      command = self._hpgl.OK( )
      if self._isCommandKnown(command):
         self.write(command)
         return self._readPort()

   @property
   def labelLength(self):
      command = self._hpgl.OL( )
      if self._isCommandKnown(command):
         self.write(command)
         return self._readPort()

   @property
   def options(self):
      self.write(self._hpgl.OO())
      return self._readPort()

   @property
   def outputP1P2(self):
      self.write(self._hpgl.OP())
      return self._readPort()

   @property
   def status(self):
      self.write(self._hpgl.OS())
      return self._readPort()

   @property
   def window(self):
      '''Output window. Same as marginSoft.'''
      self.write(self._hpgl.OW())
      return self._readPort()


   ### DCI (Device Control Instructions) Escape commands ###

   def escapePlotterOn(self):
      self.write( self._hpgl.On() )
