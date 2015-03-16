'''
Created on 2013-05-28

@author: brian
'''

import pygame
from random import randint
from random import choice

from entity import Entity
from ai import task

class Skeleton(Entity):

	living = "skeleton"
	dead = "gore"


	def __init__(self, world):
		Entity.__init__(self, world)
		self.world = world
		self.health = self.maxHealth = 20
		self.hostile = True
		self.singular = 'a skeleton'
	

class SkeletalWarrior(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		

		
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
	
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()
		
class SkeletalArcher(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		self.ai.addAI(task.Fallback(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
		
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getBow()
			
			
class SkeletalMage(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		self.ai.addAI(task.Fallback(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
		
	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getDamageStaff()