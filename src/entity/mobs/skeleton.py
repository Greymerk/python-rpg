'''
Created on 2013-05-28

@author: brian
'''

import pygame
from random import randint
from random import choice

from entity import Entity
from src.ai import task
from src.abilities import Ability

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
		pass
		
class SkeletalArcher(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		self.ai.addAI(task.Fallback(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
		
	def equip(self):
		self.abilities = [Ability(self, Ability.lookup["BowShot"])]
			
			
class SkeletalMage(Skeleton):
	
	def __init__(self, world):
		Skeleton.__init__(self, world)
		self.ai.addAI(task.Fallback(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Wander(self))
		
	def equip(self):
		if randint(0, 5) == 0:
			self.abilities = [Ability(self, Ability.lookup["Explosion"]), Ability(self, Ability.lookup["FireBall"])]
			return
		self.abilities = [Ability(self, Ability.lookup["ChainBolt"]), Ability(self, Ability.lookup["MagicMissile"])]
