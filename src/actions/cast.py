'''
Created on 2013-05-26

@author: brian
'''

import string

from src.util import Cardinal
from src.util import Vector2
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
		
		leader = self.player.party.getLeader()	
		last = self.player.lastTarget

		if self.spell is not None and self.player.lastTarget is not None:
			if leader.canHit(last.position, self.spell.range) and last.isAlive():
				self.location = Vector2(self.player.lastTarget.position)
				self.location -= self.player.avatar.position	

		self.spellList = {}
		self.options = {}
		
		for i in range(len(leader.abilities)):
			if leader.abilities is None:
				continue
			
			self.options[i + 1] = leader.abilities[i].name
			self.spellList[i + 1] = leader.abilities[i]
			
		if self.spell is not None:
			self.options = None
			self.player.log.append('Select target for ' + self.spell.name + '.')
		
	def nextStep(self):
		
		last = self.player.lastTarget
		leader = self.player.avatar

		if self.options is not None and len(self.options) == 0:
			return True
		
		if self.casting:
			if leader.action is None:
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
			
			if last is not None:
				if leader.canHit(last.position, self.spell.range) and last.isAlive():
					self.location = Vector2(last.position)
					self.location -= leader.position

			return False
		
		finish = [K_RETURN, K_c, K_SPACE, self.player.ABILITY_KEYS[self.player.avatar.abilities.index(self.spell)]]
		if self.location != (0,0) and e.key in finish:
			target = Vector2(leader.position)
			target += self.location
			leader.action = self.spell(leader, target, self.spell)
			self.targetLocation = target
			entity = self.player.world.getEntityFromLocation(target)
			if entity is not None:
				self.player.lastTarget = entity
			self.casting = True
			return False
		
		if e.key in Cardinal.key_map.keys():
			pos = leader.position
			direction = Cardinal.values[Cardinal.key_map[e.key]]
			newLocation = Vector2(pos)
			newLocation += self.location
			newLocation += direction
			if not self.player.party.getLeader().canHit(newLocation, self.spell.range):
				return False
			self.location = Vector2(self.location)
			self.location += direction
			return False
			
		return False

