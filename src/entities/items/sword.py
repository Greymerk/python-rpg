'''
Created on 2013-06-02

@author: brian
'''

from entities.abilities import Attack
from weapon import Weapon


class Sword(Weapon):

    def __init__(self):
        Weapon.__init__(self)

        
class ShortSword(Sword):
    
    def __init__(self):
        Weapon.__init__(self)
        self.damage = 2, 4
        
class LongSword(Sword):
    
    def __init__(self):
        Weapon.__init__(self)
        self.damage = 3, 6
        
class MagicSword(Sword):
    
    def __init__(self):
        Weapon.__init__(self)
        self.damage = 4, 8