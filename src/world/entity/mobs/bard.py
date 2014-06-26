'''
Created on 2013-05-28

@author: brian
'''
from entity import Entity
import pygame

class Bard(Entity):

	living = "bard.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a bard'

		self.ai.addAI(self.ai.tasks.Flee(self))
		self.ai.addAI(self.ai.tasks.Cast(self))
		self.ai.addAI(self.ai.tasks.Pursue(self))
		self.ai.addAI(self.ai.tasks.Follow(self))
		self.ai.addAI(self.ai.tasks.Wander(self))
		self.sight = 7

	def equip(self):
		self.inventory.bar[0] = self.world.items.weapons.getBow()
		
	@classmethod
	def onDamage(cls, sounds):
		sounds.get("damage.wav").play()