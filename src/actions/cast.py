'''
Created on 2013-05-26

@author: brian
'''

import string

from cardinals import cardinals
import pygame

from pygame.locals import *

class Cast(object):
	 
	def __init__(self, player, ability=None):
		self.player = player
		self.projectile = None
		self.casting = False
		self.targetLocation = None
		self.spell = ability
		self.location = None
		if self.spell is not None:
			self.location = (0,0)
			
		if self.spell is not None and self.player.lastTarget is not None:
			if self.player.party.getLeader().canHit(self.player.lastTarget.position, self.spell.range) and self.player.lastTarget.isAlive():
				self.location = self.player.lastTarget.position[0] - self.player.party.getLeader().position[0], self.player.lastTarget.position[1] - self.player.party.getLeader().position[1]	

		self.spellList = {}
		self.options = {}
		
		leader = self.player.party.getLeader()
		
		for i in range(len(leader.abilities)):
			if leader.abilities is None:
				continue
			
			self.options[i + 1] = leader.abilities[i].name
			self.spellList[i + 1] = leader.abilities[i]
			
		if self.spell is not None:
			self.options = None
			self.player.log.append('Select target for ' + self.spell.name + '.')
		
	def nextStep(self):
		
		if self.options is not None and len(self.options) == 0:
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
		
		if e.key in [K_ESCAPE]:
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
		

		if self.location != (0,0) and e.key in [K_RETURN, K_c, K_SPACE, self.player.ABILITY_KEYS[self.player.avatar.abilities.index(self.spell)]]:
			pos = self.player.party.getLeader().position
			target = (pos[0] + self.location[0], pos[1] + self.location[1])
			actor = self.player.party.getLeader()
			actor.action = self.spell(actor, target, self.spell)
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
	
	
