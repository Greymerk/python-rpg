'''
Created on 2013-06-04

@author: brian
'''

from item import Item
from items.abilities import Attack

class Weapon(Item):

    def __init__(self):
        self.ability = Attack
        self.range = 1
        self.damage = 1, 2
        
    def getAbility(self):
        return self.ability

