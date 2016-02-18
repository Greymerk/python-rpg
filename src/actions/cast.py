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
		
		leader = self.player.avatar	
		last = leader.lastTarget
		self.player.reticle = (0,0)

		if last is not None:
			if self.spell.valid(last):
				self.player.reticle = Vector2(last.position)
				self.player.reticle -= leader.position
			else:
				leader.lastTarget = None
		
			

		self.player.target = None
		
	def nextStep(self):
		
		leader = self.player.avatar

		if self.player.target is not None:
			if not self.inRange(self.player.target):
				self.player.log.append('Too far away!')
				self.player.target = None
				return False

			entity = self.player.world.getEntityFromLocation(self.player.target)
			if entity is None:
				self.player.log.append('Nothing hit!')

			leader.lastTarget = entity
			leader.action = self.spell.cast(self.player.target)
			return True


		for e in pygame.event.get():

			if e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEMOTION:
				self.player.mouse_event(e)

			if e.type != KEYDOWN:
				continue
		
			if e.key in [K_ESCAPE]:
				self.player.log.append('Cancelled')
				return True
		
			finish = [K_SPACE]
			if e.key in finish:
				target = Vector2(leader.position)
				target += self.player.reticle
				self.player.target = target
				return False
		
			if e.key in Cardinal.key_map.keys():
				pos = leader.position
				direction = Cardinal.values[Cardinal.key_map[e.key]]
				newLocation = Vector2(pos)
				newLocation += self.player.reticle
				newLocation += direction
				if not self.spell.inRange(newLocation):
					return False
				self.player.reticle = Vector2(self.player.reticle)
				self.player.reticle += direction
				return False
			
		return False
		
	def inRange(self, target):
		return self.spell.inRange(target)


