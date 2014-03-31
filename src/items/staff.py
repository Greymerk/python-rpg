'''
Created on 2013-06-01

@author: brian
'''

from weapon import Weapon
from items.abilities import Fireball
from items.abilities import MagicMissile
from items.abilities import HealBolt
from items.abilities import Resurrection

class Staff(Weapon):

	def __init__(self):
		self.ability = MagicMissile
		self.range = 7
		self.damage = 2, 6

