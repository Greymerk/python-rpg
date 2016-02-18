'''
Created on 2013-05-28

@author: brian
'''
from entity import Entity
import pygame
from src.ai import task
from src.abilities import *

class Bard(Entity):

	living = "bard"
	dead = "body"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a bard'

		self.ai.addAI(task.Flee(self))
		self.ai.addAI(task.Cast(self))
		self.ai.addAI(task.Pursue(self))
		self.ai.addAI(task.Follow(self))
		self.ai.addAI(task.Wander(self))
		self.sight = 7

	def equip(self):
		self.abilities = [Ability(self, BowShot), Ability(self, HealBolt)]
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()
