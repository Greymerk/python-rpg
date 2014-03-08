'''
Created on 2013-05-16

@author: brian
'''

from entities.ai import *

import pygame
from entity import Entity


class Headless(Entity):

	living = "headless.png"
	dead = "gore.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		
		self.ai.addAI(Flee(self))
		self.ai.addAI(Attack(self))
		self.ai.addAI(Pursue(self))
		self.ai.addAI(Follow(self))
		self.ai.addAI(Wander(self))
		self.hostile = True
		
		self.singular = 'a headless'		
