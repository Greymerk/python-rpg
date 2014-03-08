'''
Created on 2013-05-28

@author: brian
'''
from entity import Entity
import pygame
from ai import *

from items import LongBow

class Bard(Entity):

	living = "bard.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a bard'
		self.inventory.weapon = LongBow()
		
		self.ai.addAI(Flee(self))
		self.ai.addAI(Attack(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Follow(self))
		self.ai.addAI(Wander(self))
		self.sight = 7
