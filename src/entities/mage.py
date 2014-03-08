'''
Created on 2013-05-27

@author: brian
'''

from entity import Entity
import pygame
from random import randint
from ai import *
from avatar import Avatar
from items import Staff
from items import Spellbook

class Mage(Entity):

	living = "mage.png"
	dead = "body.png"

	def __init__(self, world):
		Entity.__init__(self, world)
		self.singular = 'a mage'
		self.inventory.weapon = Staff()
		self.inventory.offhand = Spellbook()
		
		self.ai.addAI(Fallback(self))
		self.ai.addAI(Cast(self))
		self.ai.addAI(Attack(self))
		self.ai.addAI(Follow(self))
		self.ai.addAI(Wander(self))
		
		
   
		
		
