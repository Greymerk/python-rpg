'''
Created on 2013-05-16

@author: brian
'''
from random import choice
import pygame

from entity import Entity
from src.ai import task
from src.abilities import *

class Ettin(Entity):

	living = "ettin"
	dead = "gore"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.world = world
		self.hostile = True
		
		self.health = self.maxHealth = 40
		
		self.ai.addAI(task.Flee(self))
		self.ai.addAI(task.Fallback(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
		
		self.singular = 'an ettin'

	def equip(self):
		self.abilities = [Ability(self, MagicMissile)]
