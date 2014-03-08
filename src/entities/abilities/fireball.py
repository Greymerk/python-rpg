'''
Created on 2013-05-26

@author: brian
'''

from pygame.color import THECOLORS

from magicmissile import MagicMissile

class Fireball(MagicMissile):
    
    color = THECOLORS['orangered']
    damage = 3, 7