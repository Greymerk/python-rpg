'''
Created on 2013-06-04

@author: brian
'''
from pygame.color import THECOLORS

from item import Item

from abilities import *

class Weapon(Item):

	def __init__(self, name="None", damage=(1, 2), range=1, ability=Attack, colour=(255,255,255)):
		self.name = name
		self.damage = damage
		self.range = range
		self.ability = ability
		self.colour = colour

	def save(self):
		data = {}
		data["type"] = self.__class__.__name__
		data["name"] = self.name
		data["damage"] = self.damage
		data["range"] = self.range
		data["colour"] = self.colour
		data["ability"] = self.ability.__name__
		return data
		
	def load(self, data):
		self.name = data["name"]
		self.damage = data["damage"]
		self.range = data["range"]
		self.colour = data["colour"]
		self.ability = lookup[data["ability"]]
		
	def getAbility(self):
		return self.ability

	@staticmethod
	def getBow():
		return Weapon("Bow", (2, 5), 6, BowShot, THECOLORS['chocolate'])
		
	@staticmethod	
	def getSword():
		return Weapon("Sword", (2, 5), 1, Attack)
	
	@staticmethod
	def getStaff():
		return Weapon("Staff of Fireball", (2, 5), 6, MagicMissile, THECOLORS['orange'])
