'''
Created on 2013-05-26

@author: brian
'''
from entity import Entity
import pygame
from random import randint
from random import choice


class Fighter(Entity):

	living = "fighter.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a fighter'

		
		self.ai.addAI(self.ai.tasks.Flee(self))
		self.ai.addAI(self.ai.tasks.Cast(self))
		self.ai.addAI(self.ai.tasks.Pursue(self))
		self.ai.addAI(self.ai.tasks.Follow(self))
		self.ai.addAI(self.ai.tasks.Wander(self))

	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getSword()
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()

