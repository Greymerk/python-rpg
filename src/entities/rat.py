'''
Created on 2013-05-16

@author: brian
'''

from entities import ai

import pygame
from entity import Entity

class Rat(Entity):

	living = "rat.png"
	dead = "gore.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.world = world
		
		self.ai.addAI(ai.Flee(self))
		self.ai.addAI(ai.Attack(self))
		self.ai.addAI(ai.Pursue(self))
		self.ai.addAI(ai.Wander(self))
		self.hostile = True

		self.singular = 'a rat'
