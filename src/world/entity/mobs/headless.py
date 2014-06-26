'''
Created on 2013-05-16

@author: brian
'''

import pygame
from entity import Entity


class Headless(Entity):

	living = "headless.png"
	dead = "gore.png"


	def __init__(self, world):
		Entity.__init__(self, world)
		self.health = self.maxHealth = 20
		
		
		self.ai.addAI(self.ai.tasks.Flee(self))
		self.ai.addAI(self.ai.tasks.Cast(self))
		self.ai.addAI(self.ai.tasks.Pursue(self))
		self.ai.addAI(self.ai.tasks.Follow(self))
		self.ai.addAI(self.ai.tasks.Wander(self))
		self.hostile = True
		
		self.singular = 'a headless'		

	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()