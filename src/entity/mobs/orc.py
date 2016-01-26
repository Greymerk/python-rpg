'''
Created on 2013-05-12

@author: brian
'''

import pygame
from entity import Entity
from src.ai import task
from src.abilities import *

class Orc(Entity):

	living = "orc"
	dead = "gore"


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
		pass
