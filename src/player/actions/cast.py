'''
Created on 2013-05-26

@author: brian
'''

import string

from cardinals import cardinals
import pygame

from pygame.locals import *

class Cast(object):
	 
	def __init__(self, player):
		self.player = player
		self.projectile = None
		self.casting = False
		self.targetLocation = None
		self.spell = None
		self.location = None
		
		self.spellList = {}
		self.options = {}
		
		leader = self.player.party.getLeader()
		
		for i in range(len(leader.inventory.bar)):
			if leader.inventory.bar[i] is None:
				continue
			
			self.options[i + 1] = leader.inventory.bar[i].ability.__name__
			self.spellList[i + 1] = leader.inventory.bar[i]
		
	def nextStep(self):
		
		if len(self.options) == 0:
			return True
		
		if self.casting:
			if self.player.party.getLeader().action is None:
				entity = self.player.world.getEntityFromLocation(self.targetLocation)
				if entity is None:
					self.player.log.append('Nothing hit!')
				return True   
			return False
		
		e = pygame.event.poll()

		if e is None:
			return False

		if e.type != KEYDOWN:
			return False
		
		if e.key in [K_ESCAPE, K_SPACE]:
			self.player.log.append('Cancelled')
			return True

		if self.spell is None:
			i = e.key - 47
			if not (i - 1) in self.spellList.keys():
				return False
			
			self.spell = self.spellList[i - 1]
			self.location = (0,0)
			
			if self.player.lastTarget is not None:
				if self.player.party.getLeader().canHit(self.player.lastTarget.position, self.spell.range) and self.player.lastTarget.isAlive():
					self.location = self.player.lastTarget.position[0] - self.player.party.getLeader().position[0], self.player.lastTarget.position[1] - self.player.party.getLeader().position[1]	
			return False
		

		if self.location != (0,0) and e.key in [K_RETURN, K_c]:
			pos = self.player.party.getLeader().position
			target = (pos[0] + self.location[0], pos[1] + self.location[1])
			actor = self.player.party.getLeader()
			actor.action = self.spell.ability(actor, target, self.spell)
			self.targetLocation = target
			entity = self.player.world.getEntityFromLocation(target)
			if entity is not None:
				self.player.lastTarget = entity
			self.casting = True
			return False
		
		if e.key in cardinals.keys():
			pos = self.player.party.getLeader().position
			direction = cardinals[e.key]
			newLocation = pos[0] + self.location[0] + direction[0], pos[1] + self.location[1] + direction[1]
			if not self.player.party.getLeader().canHit(newLocation, self.spell.range):
				return False
			self.location = self.location[0] + direction[0], self.location[1] + direction[1]
			return False
			
		return False
	
	
