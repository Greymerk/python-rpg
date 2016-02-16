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
	 
	def __init__(self, player, ability):
		self.player = player
		self.projectile = None
		self.spell = ability
		
		leader = self.player.party.getLeader()	
		last = self.player.lastTarget

		if self.player.lastTarget is not None:
			if leader.canHit(last.position, self.spell.range) and last.isAlive():
				self.player.reticle = Vector2(self.player.lastTarget.position)
				self.player.reticle -= self.player.avatar.position
		else:
			self.player.reticle = (0,0)

		self.player.target = None
		
	def nextStep(self):
		
		last = self.player.lastTarget
		leader = self.player.avatar

		
		
		if self.player.target is not None:
			if not self.inRange(self.player.target):
				self.player.log.append('Too far away!')
				self.player.target = None
				return False

			entity = self.player.world.getEntityFromLocation(self.player.target)
			if entity is None:
				self.player.log.append('Nothing hit!')

			self.player.lastTarget = entity
			leader.action = self.spell(leader, self.player.target, self.spell)
			return True


		for e in pygame.event.get():

			if e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEMOTION:
				self.player.mouse_event(e)

			if e is None:
				return False

			if e.type != KEYDOWN:
				return False
		
			if e.key in [K_ESCAPE]:
				self.player.log.append('Cancelled')
				return True
		
			finish = [K_RETURN, K_c, K_SPACE, self.player.ABILITY_KEYS[self.player.avatar.abilities.index(self.spell)]]
			if e.key in finish:
				target = Vector2(leader.position)
				target += self.player.reticle
				leader.action = self.spell(leader, target, self.spell)
				entity = self.player.world.getEntityFromLocation(target)
				if entity is not None:
					if self.spell.validTarget(leader, entity):
						self.player.lastTarget = entity
					else:
						return False
				self.player.target = target
				return False
		
			if e.key in Cardinal.key_map.keys():
				pos = leader.position
				direction = Cardinal.values[Cardinal.key_map[e.key]]
				newLocation = Vector2(pos)
				newLocation += self.player.reticle
				newLocation += direction
				if not self.inRange(newLocation):
					return False
				self.player.reticle = Vector2(self.player.reticle)
				self.player.reticle += direction
				return False
			
		return False

	def inRange(self, pos):
		if not self.player.avatar.canHit(pos, self.spell.range):
			return False
		return True

