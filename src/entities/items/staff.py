'''
Created on 2013-06-01

@author: brian
'''

from weapon import Weapon

from entities.abilities import Fireball

class Staff(Weapon):

    def __init__(self):
        self.ability = Fireball
        self.range = 6
        self.damage = 2, 5

        