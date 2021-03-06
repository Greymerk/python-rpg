'''
Created on 2013-05-16

@author: brian
'''

import pygame
from entity import Entity
from src.ai import task
from src.abilities import *

class Headless(Entity):

	living = "headless"
	dead = "gore"


	def __init__(self, world):
		Entity.__init__(self, world)
		self.health = self.maxHealth = 20
		
		
		self.ai.addAI(task.Flee(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Follow(self))
		self.ai.addAI(task.Wander(self))
		self.hostile = True
		
		self.singular = 'a headless'

	def equip(self):
		pass
