'''
Created on 2013-06-01

@author: brian
'''

from weapon import Weapon
from entities.abilities.bowshot import BowShot
from entities.abilities.bowshot import MagicBowShot

class Bow(Weapon):

    def __init__(self):
        Weapon.__init__(self)
        self.ability = BowShot
        
    
class ShortBow(Bow):

    def __init__(self):
        Bow.__init__(self)
        
        self.range = 4
        self.damage = 1, 4

class LongBow(Bow):
    
    def __init__(self):
        Bow.__init__(self)
        
        self.range = 6
        self.damage = 2, 6
        
class MagicBow(Bow):
    
    def __init__(self):
        Bow.__init__(self)
        self.ability = MagicBowShot
        
        self.range = 7
        self.damage = 3, 9