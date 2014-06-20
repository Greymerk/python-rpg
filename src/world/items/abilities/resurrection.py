'''
Created on 2013-06-04

@author: brian
'''

from pygame.color import THECOLORS
from projectiles import Star
from random import randint

class Resurrection(object):
	
	color = THECOLORS['palegoldenrod']
	heal = True
	range = 6
	damage = 1, 2
	
	def __init__(self, caster, location, item):
		self.range = item.range
		self.caster = caster
		self.target = location
		self.done = False
		self.entityHit = self.caster.world.getEntityFromLocation(self.target, False)
		self.projectile = Star(caster.position, location, self.__class__.color, self.entityHit)
		casterName = self.caster.getName()
		if not self.entityHit is None:
			targetName = self.entityHit.getName()
			self.caster.world.log.append(casterName + ' cast resurrection on ' + targetName)
		else:
			self.caster.world.log.append(casterName + ' cast resurrection on nothing!')
	 
	def update(self):
		self.projectile.update()
		if self.projectile.done:
			if not self.entityHit is None:
				self.entityHit.revive(self.caster)
			self.done = True
			return True
		return False
		
	def draw(self, surface, position):
		if not self.done:
			self.projectile.draw(surface, position)
	
	@classmethod
	def validTarget(cls, actor, target):

		if not target in actor.getFriends():
			return False

		if target.isAlive():
			return False

		if not actor.canSee(target.position):
			return False

		return True
