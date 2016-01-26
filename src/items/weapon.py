'''
Created on 2013-06-04

@author: brian
'''

from random import randint
from random import choice

from pygame.color import THECOLORS

from item import Item
from src.abilities import *

class Weapon(Item):

	def __init__(self, name="None", damage=(1, 2), range=1):
		self.name = name
		self.damage = damage
		self.range = range

	def save(self):
		data = {}
		data["type"] = self.__class__.__name__
		data["name"] = self.name
		data["damage"] = self.damage
		data["range"] = self.range
		return data
		
	def load(self, data):
		self.name = data["name"]
		self.damage = data["damage"]
		self.range = data["range"]
		
