'''
Created on 2013-05-16

@author: brian
'''

import pygame
from entity import Entity

class Rat(Entity):

	living = "rat.png"
	dead = "gore.png"


	def __init__(self, world):
		Entity.__init__(self, world)
		self.world = world
		self.health = self.maxHealth = 15

		
		self.ai.addAI(self.ai.tasks.Flee(self))
		self.ai.addAI(self.ai.tasks.Cast(self))
		self.ai.addAI(self.ai.tasks.Pursue(self))
		self.ai.addAI(self.ai.tasks.Wander(self))
		self.hostile = True

		self.singular = 'a rat'

	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()