from chiplotle.hpgl.compound.hpglcompoundshape import _HPGLCompoundShape
from chiplotle.hpgl.commands import PU, PA, PD, PR
from chiplotle.tools.mathtools import polar_to_xy
import math
import random


class RandomWalk(_HPGLCompoundShape):
   '''Random Walk.'''
   def __init__(self, xy, steps, step_size=500):
      _HPGLCompoundShape.__init__(self, xy) 
      self.steps = steps
      self.step_size = step_size

   @property
   def _subcommands(self):
      result = _HPGLCompoundShape._subcommands.fget(self)
      result += [PD( )]
      for i in range(self.steps):
        A = random.random() * math.pi * 2
        r = self.step_size
        xy = polar_to_xy(r,A)
        result.append( PR(xy) )
      result.append( PU() )
      return result


