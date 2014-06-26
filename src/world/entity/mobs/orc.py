'''
Created on 2013-05-12

@author: brian
'''

import pygame
from entity import Entity
from ai import task

class Orc(Entity):

	living = "orc.png"
	dead = "gore.png"


	def __init__(self, world):
		Entity.__init__(self, world)
		self.world = world
		self.health = self.maxHealth = 20

		self.ai.addAI(task.Flee(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
		
		self.singular = 'an orc'
		
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()