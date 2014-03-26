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
		self.ability = Fireball
		self.range = 6
		self.damage = 2, 5

class MageStaff(Staff):
	
	def __init__(self):
		Staff.__init__(self)
		self.ability = MagicMissile
		
class FireStaff(Staff):
	
	def __init__(self):
		Staff.__init__(self)
		self.ability = Fireball
		
class HealStaff(Staff):
	
	def __init__(self):
		Staff.__init__(self)
		self.ability = HealBolt
		
class ResurrectionStaff(Staff):
	
	def __init__(self):
		Staff.__init__(self)
		self.ability = Resurrection