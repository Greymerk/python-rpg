'''
Created on 2013-05-16

@author: brian
'''

import pygame
from entity import Entity

from ai import task

class Snake(Entity):

	living = "snake.png"
	dead = "gore.png"


	def __init__(self, world):
		Entity.__init__(self, world)

		
		self.world = world
		self.hostile = True
		self.health = self.maxHealth = 15
		
		self.ai.addAI(task.Flee(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
		self.singular = 'a snake'
		
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()