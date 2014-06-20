'''
Created on 2013-05-16

@author: brian
'''

import ai

import pygame
from entity import Entity
from random import choice

class Ettin(Entity):

	living = "ettin.png"
	dead = "gore.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.world = world
		self.hostile = True
		
		self.ai.addAI(ai.Flee(self))
		self.ai.addAI(ai.Fallback(self))
		self.ai.addAI(ai.Cast(self))
		self.ai.addAI(ai.Pursue(self))
		self.ai.addAI(ai.Wander(self))
		
		self.singular = 'an ettin'

	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getDamageStaff()