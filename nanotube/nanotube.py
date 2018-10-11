import mbuild as mb
import numpy as np
from copy import deepcopy
from math import *

__all__ = ['SWCNT']

# define repeatable row units for the different chiralities
class armchair(mb.Compound):
    def __init__(self):
        super(armchair,self).__init__()
        
        for i in range(0,4):
            self.add(C())

        self[1].translate((.071,.071*np.sqrt(3),0))
        self[2].translate((.213,.071*np.sqrt(3),0))
        self[3].translate((.284,0,0))

class zigzag(mb.Compound):
    def __init__(self,orientation=1):
        super(zigzag,self).__init__()

        if orientation == 0:
            raise ValueError("Orientation must either be set to some positive value or some negative value")
        
        for i in range(0,3):
            self.add(C())

        self[1].translate((.071*np.sqrt(3),.071*orientation,0))
        self[2].translate((2*.071*np.sqrt(3),0,0))

class SWCNT(mb.Compound):
""" A single-walled Carbon nanotube recipe
radius: radius of nanotube in nm
chirality : If using radius instead of n and m, the type of chirality desired
    either "armchair" or "zigzag". "armchair" by defualt

n,m : chirality parameters, if only n is defined armchair is assumed
length : length of nanotube in nm

note: either the radius or the chiraity parameters must be defined but not both. (Should let radius override and provide warning message)
"""
    def __init__(self,radius=None,chirality="armchair",n=None,m=None,length):
        super(SWCNT, self).__init__()

        # define Carbon atom
        class C(mb.Compound):
            def __init__(self):
                super(C,self).__init__()
                
                self.add(mb.Particle(name='C'))

        #Checking validity of input values
        if radius is None and n is None:
            raise ValueError("Either the radius or the chiraity parameters must be defined")
        elif radius is not None and n is not None:
            raise RuntimeWarning("Both radius and chirality parameters defined,radius overriding (n,m) values")
        elif radius < 0.19:
            raise ValueError("The smallest possible radius is 0.19 nm. Your radius was " + str(radius) + " nm."

        #Sets implied chirality from the n,m values if nessecary
        if n is not None and m is 0 and radius is None:
            chirality = "zigzag"

        # Next calculate real radius and find the sheet dimensions in terms of
        # different row units. Change armchair and zigzag classes to just 
        # record carbon positions and perform calculations on that. Do not
        # populate with actual Compound objects until final positions are
        # recorded.
        # 
        # Armchair/zigzag unit cell -> full rows -> full sheets -> folded tubes 
        # -> insert C atoms
        